from abc import ABC, abstractmethod
from interfaces.gateways.traffic_gateway import ITrafficDataGateway
from domains.repositories import ITrafficRepository
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
        destination: str
    ) -> bool:
        
        all_routes = self.traffic_gateway.get_route_data(origin, destination)

        results = []
        
        for route in all_routes:
            results.append(self.traffic_repo.save_route(route))


        return all(results)