from owlready2 import *

class PropertyService:
    
    def __init__(self, ontology):
        self.ontology = ontology
        
    def create_object_property(self):
        with self.ontology:
            class has_topping(ObjectProperty):
                domain = [self.ontology.Pizza]
                range = [self.ontology.Topping]
    
    def create_data_property(self):
        pass
    
    def create_annotation_property(self):
        pass