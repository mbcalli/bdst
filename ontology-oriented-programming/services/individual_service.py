class IndividualService:
    
    def __init__(self, ontology):
        self.ontology = ontology
        
    def create_individuals(self):
        with self.ontology:
            self.ontology.Pizza("non_veggie_pizza")
            self.ontology.MeatTopping("pepperoni")