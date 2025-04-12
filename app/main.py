from typing import Annotated
from fastapi import FastAPI, Query, HTTPException
from app.flight_cost import FlightFinder
from app.models import Cheapest, Error, Flight

app = FastAPI()

FLIGHT_DATA = "US:UK:Delta:500,UK:FR:JetBlue:100,FR:DE:Lufthansa:90,US:DE:AirFrance:950"
flight_finder = FlightFinder(FLIGHT_DATA)

@app.get('/cheapest-flight')
async def get_cheapest_flight(
    from_: Annotated[str, Query(..., alias="from")], 
    to: Annotated[str, Query(..., alias="to")],
    max_cost: Annotated[float, Query(alias="max_cost")] = float('inf'),
    max_stops: Annotated[float, Query(alias="max_stops")] = float('inf')
) -> Cheapest | Error:

    result = flight_finder.find_cheapest_flight(from_, to, max_cost, max_stops)
    if not result:
        raise HTTPException(status_code=404, detail="No route found")
    
    cost, path = result
    return {"cost": cost,"route": path}

@app.post('/add-flight/')
async def add_flight(flight: Flight):
    try:
        flight_finder.add_new_edge(flight.model_dump_json())
        return {
            "response": f"Flight {flight.source} to {flight.destination} posted.",
            "status": 200,
            "error_message": ""        
        }
    except Exception as e:
        raise HTTPException(status=400, detail=str(e))


@app.get('/routes')
async def get_routes(from_: Annotated[str, Query(..., alias="from")]):
    result = flight_finder.find_all_flights_from(from_)
    return {
        "recheable": result
    }

@app.get('/flights/from')
async def flight_from(from_: Annotated[str, Query(..., alias="from")]):
    result = flight_finder.direct_flights_from(from_)
    return {f"flights_from_{from_}": result}