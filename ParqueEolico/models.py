from pydantic import BaseModel, validator
import random

class GeneratorData(BaseModel):
    generator_id: int
    power_output: float
    
    @validator('power_output', pre=True, always=True)
    def simulate_error(cls, v):
        if v < 0:
            raise ValueError('Data error occurred due to error probability.')
        return v


class AggregatedData(BaseModel):
    average_power_output: float
    timestamp: str