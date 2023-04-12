from owlready2 import *

class ConceptService:
    
    def __init__(self, ontology):
        self.ontology = ontology
        
    def create_concepts(self):
        with self.ontology:
            
            ## Base Classes
            class Pizza(Thing):
                pass
            
            class Topping(Thing):
                pass
            
            class MeatTopping(Topping):
                pass
            
            class FishTopping(MeatTopping):
                pass
            
            # ## Properties
            # class has_topping(ObjectProperty):
            #     domain = [Pizza]
            #     range = [Topping]
            
            # ## Equivalency Classes
            # class NonVegetarianPizza(Pizza):
            #     equivalent_to = [
            #         Pizza
            #         & ( has_topping.some(MeatTopping)
            #         | has_topping.some(FishTopping)
            #         ) ]
            #     pass
            
            