from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import json

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
		return {
			"id": self.id,
			"name": self.name,
			"research-focus": self.research_focus,
			"hobbies": self.hobbies,
			"spirit-animal": self.spirit_animal
		}

# create a root endpoint
@app.get("/")
def read_root():
	return {"Hello": "World"}

# POST to create a person using the Person class
# writes to a json file
@app.post("/person/create")
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
@app.get("/people")
def get_people():
	with open('people.json', 'r') as file:
		file_data = json.load(file)['people']
		return file_data

# GET to retreive a specific person
@app.get("/person/{person_id}")
def get_person(person_id: int):
	with open('people.json', 'r') as file:
		file_data = json.load(file)['people']
		if person_id:
			# get only the people with the specified person_id
			# Note: should only be one person with a given id
			file_data = [x for x in file_data if x['id'] == person_id][0]
		return file_data