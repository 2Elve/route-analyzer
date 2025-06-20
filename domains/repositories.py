from abc import ABC, abstractmethod
from domains.entities import Route

class ITrafficRepository(ABC):
    @abstractmethod
    def save_route(self, route: Route) -> bool:
        pass

class IWeatherRepository(ABC):
    @abstractmethod
    def save_weather(self, route: Route) -> bool:
        pass