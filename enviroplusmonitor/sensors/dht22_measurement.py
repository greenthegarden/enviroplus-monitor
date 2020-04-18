from datetime import datetime
from typing import List
from pydantic import BaseModel

class Measurement(BaseModel):
  label: str
  value: float
  units: str

class Dht22Measurement(BaseModel):
  sensor = 'dht22'
  measurements: List[Measurement]

m = Measurement(label = 'temperature', value = 34.2, units = 'C')
print(m)
print(m.dict())
dm = Dht22Measurement(measurements=[m])
print(dm)
print(dm.dict())
