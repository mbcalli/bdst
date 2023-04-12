class EquivalencyService:
    
    def __init__(self, ontology):
        self.ontology = ontology
    
    def create_equivalency(self):
        with self.ontology:
            
            class NonVegetarianPizza(self.ontology.Pizza):
                equivalent_to = [
                    self.ontology.Pizza
                    & ( self.ontology.has_topping.some(self.ontology.MeatTopping) | self.ontology.has_topping.some(self.ontology.FishTopping)) ]
                pass