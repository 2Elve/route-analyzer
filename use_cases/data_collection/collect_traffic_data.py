from abc import ABC, abstractmethod
from interfaces.gateways.traffic_gateway import ITrafficDataGateway
from domains.repositories import ITrafficRepository
from typing import List, Tuple
from domains.entities import Route


class CollectTrafficDataUseCase:
    def __init__(
        self, 
        traffic_gateway: ITrafficDataGateway, 
        traffic_repo: ITrafficRepository
    ):
        self.traffic_gateway = traffic_gateway
        self.traffic_repo = traffic_repo
    
    def execute(
        self, 
        origin: str,
        destination: str,
        round_trip: bool = False
    ) -> bool:
        
        # Add round trip route to routes to process
        routes_to_process: List[Tuple[str, str]] = [(origin,destination)]
        if round_trip:
            routes_to_process.append((destination, origin))

        results = []

        for start, end in routes_to_process:
            
            # Fetch Data from Gateway
            routes = self.traffic_gateway.get_route_data(start, end)

            # Save all segments returned from Gateway
            for route in routes:
                results.append(self.traffic_repo.save_route(route))

        return all(results)