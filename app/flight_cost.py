import re
import heapq
from collections import defaultdict, deque

"""
Given a list of flights in "SRC:DST:Airline:Cost" format, and a source and destination, 
find the cheapest total cost (even if it requires connecting flights).
"""

class FlightFinder:   
    def __init__(self, flights_str):
        self.flights_str = flights_str
        self.flight_graph: dict[str:tuple[int, str]] = defaultdict(list)
        self.parse_flightlist()

    def parse_flightlist(self):
        pattern = r'([A-Z]+):([A-Z]+):[A-Za-z0-9]+:([0-9]+),?'
        flight_list = re.findall(pattern, self.flights_str)        
        # build graph in dictionary
        for source, dest, cost in flight_list:
            self.flight_graph[source].append((int(cost), dest))

    def find_cheapest_flight(
            self, source: str, 
            destination: str, 
            max_cost: float,
            max_stops: float
        ) -> tuple[int, str]:
        if source not in self.flights_str or destination not in self.flights_str:
            return None
        
        flights_found = self.find_all_flights(source, destination, max_cost, max_stops)
        return min(flights_found) if flights_found else None

    def find_all_flights_from(self, source: str):
        visited = set()
        queue = deque([source])

        while queue:
            current_location = queue.popleft()
            visited.add(current_location)
            for _, next_location in self.flight_graph[current_location]:
                queue.append(next_location)
                
        return sorted(list(filter(lambda location: location != source, visited)))   

    def find_all_flights(self, source: str, destination: str, max_cost: float, max_stops: float) -> tuple[int, str]:  
        visited = {}

        # (current cost, current stops, source, destination)
        queue: tuple[int, str, str] = [(0, 0, source, source)]
        heapq.heapify(queue)
        flights: list = []
        
        while queue:
            cost, stops, src, path = heapq.heappop(queue)
            if src == destination:
                flights.append((cost, path))
            if src in visited: 
                continue
        
            visited[src] = cost
            for next_cost, dest in self.flight_graph[src]:
                cost_sofar = cost + next_cost
                stops_sofar = stops + 1
                if cost_sofar <= max_cost and stops_sofar <= max_stops:
                    heapq.heappush(queue, (cost_sofar, stops_sofar, dest, path + f" -> {dest}"))
        return flights

    def add_new_edge(self, flight):
        self.flights_str += f",{flight['source']}:{flight['destination']}:{flight['airline']}:{flight['cost']}"
        self.flight_graph[flight["source"]].append((int(flight["cost"]), flight["destination"]))

    def direct_flights_from(self, source: str):
        print(re.findall(fr'{source}:([A-Z]+):([a-zA-Z0-9]+):([0-9]+)', self.flights_str))
        direct_flights = map(lambda flight: {
            "destination": flight[0],
            "airline": flight[1],
            "cost": flight[2]
        }, re.findall(fr'{source}:([A-Z]+):([a-zA-Z0-9]+):([0-9]+)', self.flights_str))
        return list(direct_flights)