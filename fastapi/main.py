from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import dictfier
import json
from fhir import *

with open('dictfier_query.json', 'r') as file:
	query = json.load(file)

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

# POST to create a patient using the Patient class from fhir.py
# writes to a json file
@app.post("/create/patient/")
def create_patient(payload: dict = Body(...)):
	with open('patients.json', 'r+') as file:
		file_data = json.load(file)

		patient = Patient(**payload)

		d = dictfier.dictfy(patient, query)
		
		file_data['patients'].append(d)
		print(patient.__dict__)
		file.seek(0)
		json.dump(file_data, file, indent=4, default=str)


@app.put("/update/patient/{patient_id}/")
def update_patient(patient_id: int, payload: dict = Body(...)):
	with open('patients.json', 'r+') as file:
		file_data = json.load(file)

		file_data = {'patients': [x for x in file_data['patients'] if x['identifier']['value'] != patient_id]}

		patient = Patient(**payload)

		d = dictfier.dictfy(patient, query)
		
		file_data['patients'].append(d)
		print(patient.__dict__)
		file.seek(0)
		json.dump(file_data, file, indent=4, default=str)

@app.get("/get/patient/")
def get_patient(patient_id: int = None):
	with open('patients.json', 'r') as file:
		file_data = json.load(file)['patients']

		# uery only using name
		if patient_id is not None:
			# get only the people with the specified name
			file_data = [x for x in file_data if x['identifier']['value'] == patient_id]

		return file_data



################################################################################


# POST to create a person using the Person class
# writes to a json file
@app.post("/create/person/")
def create_person(person: Person):
	with open('people.json', 'r+') as file:
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
	with open('people.json', 'r') as file:
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