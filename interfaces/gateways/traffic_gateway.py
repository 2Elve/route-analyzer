from abc import ABC, abstractmethod
from domains.entities import Route
from datetime import datetime
from typing import List

class ITrafficDataGateway(ABC):
    @abstractmethod
    def get_route_data(
        self, 
        origin: str, 
        destination: str
    ) -> List[Route]:
        pass