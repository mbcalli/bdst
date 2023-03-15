from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import dictfier
import json
import requests
from fhir import *

with open('dictfier_queries/patient_dict_query.json', 'r') as file:
	patient_dict_query = json.load(file)

with open('dictfier_queries/condition_dict_query.json', 'r') as file:
	condition_dict_query = json.load(file)
 
with open('dictfier_queries/observation_dict_query.json', 'r') as file:
        observation_dict_query = json.load(file)

with open('keys.json', 'r') as file:
	API_KEY = json.load(file)['API_KEY']

ULMS_BASE_URL = 'https://uts-ws.nlm.nih.gov/rest'


# initialize the app
app = FastAPI()

# create a class for the person
class Person(BaseModel):
	id: int
	name: str
	research_focus: str
	hobbies: list
	spirit_animal: dict

	# return a dictionary of class's attributes
	def get_dictionary(self):
		return self.__dict__


# create a root endpoint
@app.get("/")
def read_root():
	return "This is an API created for BDSI 8020."

################################################################################
# OBSSERVATIONS
################################################################################

# POST to create a condition using the Condition class from fhir.py
# writes to a json file

def get_LOINC_lab_name_from_code(code: str):
	endpoint_url = '/content/current'
	query_params = f'/source/LNC/{code}?apiKey={API_KEY}'
	url = ULMS_BASE_URL + endpoint_url + query_params

	response = requests.get(url)

	if response.status_code != 200:
		return None
		
	name = response.json()['result']['name']

	return name



@app.post("/create/observation/{patient_id}")
def create_patient(patient_id: int, payload: dict = Body(...)):
	with open('databases/observations.json', 'r+') as file:
		file_data = json.load(file)

		observation = Observation(**payload)
		observation.subject = patient_id

		# Get the lab name from the LOINC code
		LOINC_code = observation.code.coding
		lab_name = get_LOINC_lab_name_from_code(LOINC_code)
		observation.code.text = lab_name

		print('a')
		d = dictfier.dictfy(observation, observation_dict_query)
		print('b')
		file_data['observations'].append(d)
		file.seek(0)
		json.dump(file_data, file, indent=4, default=str)

@app.put("/update/observation/{observation_id}/patient/{patient_id}")
def update_patient(observation_id: int, patient_id: int, payload: dict = Body(...)):
	with open('databases/observations.json', 'r+') as file:
		file_data = json.load(file)

		file_data = {'observations': [x for x in file_data['observations'] if x['identifier']['value'] != observation_id]}

		observation = Observation(**payload)
		observation.subject = patient_id

		# Get the lab name from the LOINC code
		LOINC_code = observation.code.coding
		lab_name = get_LOINC_lab_name_from_code(LOINC_code)
		observation.code.text = lab_name
  

		d = dictfier.dictfy(observation, observation_dict_query)
		
		file_data['observations'].append(d)
		file.seek(0)
		json.dump(file_data, file, indent=4, default=str)

@app.get("/get/observations/{patient_id}")
def get_patient(patient_id: int = None):
	with open('databases/observations.json', 'r') as file:
		file_data = json.load(file)['observations']

		file_data = [x for x in file_data if x['subject'] == patient_id]

		return file_data

################################################################################
# CONDITIONS
################################################################################

# POST to create a condition using the Condition class from fhir.py
# writes to a json file

def get_ICD10_code_from_diagnosis(diagnosis: str):
	endpoint_url = '/search/current'
	query_params = f'?string={diagnosis}&sabs=ICD10CM&returnIdType=code&apiKey={API_KEY}'
	url = ULMS_BASE_URL + endpoint_url + query_params

	response = requests.get(url)

	if response.status_code != 200:
		return None

	result = response.json()['result']['results']
	return result[0]['ui']



@app.post("/create/condition/{patient_id}")
def create_patient(patient_id: int, payload: dict = Body(...)):
	with open('databases/conditions.json', 'r+') as file:
		file_data = json.load(file)

		condition = Condition(**payload)
		condition.subject = patient_id

		# Get ICD10 code from diagnosis
		diagnosis = condition.code.text
		ICD10_code = get_ICD10_code_from_diagnosis(diagnosis)
		condition.code.coding = ICD10_code

		d = dictfier.dictfy(condition, condition_dict_query)
		
		file_data['conditions'].append(d)
		file.seek(0)
		json.dump(file_data, file, indent=4, default=str)

@app.put("/update/condition/{condition_id}/patient/{patient_id}")
def update_patient(condition_id: int, patient_id: int, payload: dict = Body(...)):
	with open('databases/conditions.json', 'r+') as file:
		file_data = json.load(file)

		file_data = {'conditions': [x for x in file_data['conditions'] if x['identifier']['value'] != condition_id]}

		condition = Condition(**payload)
		condition.subject = patient_id

		# Get ICD10 code from diagnosis
		diagnosis = condition.code.text
		ICD10_code = get_ICD10_code_from_diagnosis(diagnosis)
		condition.code.coding = ICD10_code

		diagnosis = condition.code.text
		ICD10_code = get_ICD10_code_from_diagnosis(diagnosis)
		condition.code.coding = ICD10_code

		d = dictfier.dictfy(condition, condition_dict_query)
		
		file_data['conditions'].append(d)
		file.seek(0)
		json.dump(file_data, file, indent=4, default=str)

@app.get("/get/conditions/{patient_id}")
def get_patient(patient_id: int = None):
	with open('databases/conditions.json', 'r') as file:
		file_data = json.load(file)['conditions']

		file_data = [x for x in file_data if x['subject'] == patient_id]

		return file_data

################################################################################
# PATIENTS
################################################################################

# POST to create a patient using the Patient class from fhir.py
# writes to a json file
@app.post("/create/patient/")
def create_patient(payload: dict = Body(...)):
	with open('databases/patients.json', 'r+') as file:
		file_data = json.load(file)

		patient = Patient(**payload)

		d = dictfier.dictfy(patient, patient_dict_query)
		
		file_data['patients'].append(d)
		print(patient.__dict__)
		file.seek(0)
		json.dump(file_data, file, indent=4, default=str)


@app.put("/update/patient/{patient_id}/")
def update_patient(patient_id: int, payload: dict = Body(...)):
	with open('databases/patients.json', 'r+') as file:
		file_data = json.load(file)

		file_data = {'patients': [x for x in file_data['patients'] if x['identifier']['value'] != patient_id]}

		patient = Patient(**payload)

		d = dictfier.dictfy(patient, patient_dict_query)
		
		file_data['patients'].append(d)
		print(patient.__dict__)
		file.seek(0)
		json.dump(file_data, file, indent=4, default=str)

@app.get("/get/patient/")
def get_patient(patient_id: int = None):
	with open('databases/patients.json', 'r') as file:
		file_data = json.load(file)['patients']

		# uery only using name
		if patient_id is not None:
			# get only the people with the specified name
			file_data = [x for x in file_data if x['identifier']['value'] == patient_id]

		return file_data



################################################################################
# PERSONS
################################################################################


# POST to create a person using the Person class
# writes to a json file
@app.post("/create/person/")
def create_person(person: Person):
	with open('databases/people.json', 'r+') as file:
		file_data = json.load(file)

		# check if the person_id already exists
		person_ids = [x['id'] for x in file_data['people']]
		if person.id in person_ids:
			raise HTTPException(status_code=400, detail="Person id already exists")
			return 
		
		file_data['people'].append(person.get_dictionary())
		file.seek(0)
		json.dump(file_data, file, indent=4)

# GET to retreive all people
@app.get("/get/person/")
def get_people(person_name: str = None, person_id: int = None):
	with open('databases/people.json', 'r') as file:
		file_data = json.load(file)['people']

		# uery only using name
		if person_name and person_id is None:
			# get only the people with the specified name
			file_data = [x for x in file_data if x['name'] == person_name]

		# query only using id
		elif person_id and person_name is None:
			# get only the people with the specified person_id
			# Note: should only be one person with a given id
			file_data = [x for x in file_data if x['id'] == person_id][0]

		# query using both name and id
		elif person_name and person_id:
			# get only the people with the specified name and person_id
			file_data = [x for x in file_data if x['name'] == person_name and x['id'] == person_id]

		# query using neither name nor id
		else:
			# get all people
			pass

		return file_data