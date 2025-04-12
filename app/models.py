from pydantic import BaseModel

class Flight(BaseModel):
    airline: str
    cost: int
    source: str
    destination: str

class Cheapest(BaseModel):
    cost: int
    route: str

class Error(BaseModel):
    message: str  