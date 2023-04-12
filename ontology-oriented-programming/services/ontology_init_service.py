from owlready2 import *
from services.concept_service import ConceptService
from services.individual_service import IndividualService
from services.property_service import PropertyService
from services.equivalency_service import EquivalencyService
import os, io

class OntologyInitService:
    
    def __init__(self, base_uri, ontology_id):
        self.base_uri = base_uri
        self.ontology_id = ontology_id
        
        onto_path.append(os.getcwd() + "/repository")
        
        self.owl_file = io.BytesIO()
        
        self.ontology = get_ontology(self.base_uri + self.ontology_id + "_onto.owl")
        self.__initialize__()
        
    def __initialize__(self):
        print(f"Initializing {self.ontology_id} ontology...")
        
        print("Building class heirarchy...")
        concept_service = ConceptService(self.ontology)
        concept_service.create_concepts()
        
        print("Creating individuals...")
        individual_service = IndividualService(self.ontology)
        individual_service.create_individuals()
        
        print("Creating properties...")
        property_service = PropertyService(self.ontology)
        property_service.create_object_property()
        
        print("Creating equivalencies...")
        equivalency_service = EquivalencyService(self.ontology)
        equivalency_service.create_equivalency()
        
        self.save()
        print("Initialized.")
    
    def get_owl_string(self):
        with open(os.getcwd() + "/repository/" + self.ontology_id + "_onto.owl") as file:
            return file.read()
        
    def reload(self):
        self.ontology.destroy()
        
    def save(self):
        self.ontology.save()
        
    def get_ontology(self):
        return self.ontology