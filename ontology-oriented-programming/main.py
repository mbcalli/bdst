from typing import Union
from fastapi import FastAPI
from owlready2 import *
import os
from services.ontology_init_service import OntologyInitService
from services.concept_service import ConceptService

app = FastAPI()

@app.get("/execute")
def execute():
    
    ontology_init_service = OntologyInitService('https://fake-url.com/', 'pizza')
    owl_string = ontology_init_service.get_owl_string()
    
    onto = ontology_init_service.get_ontology()
    
    with onto:
        onto.non_veggie_pizza.has_topping.append(onto.pepperoni)
        
        sync_reasoner()
        
        onto.save()
    
    ontology_init_service.reload()
    return owl_string, "200"
