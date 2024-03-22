import random
from models import GeneratorData

class Generator:
    def __init__(self, generator_id):
        self.generator_id = generator_id
        
    def generate_data(self):
        power_output = random.uniform(-10, 100)
        return GeneratorData(
            generator_id=self.generator_id, 
            power_output=power_output, 
        )