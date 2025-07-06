from abc import ABC, abstractmethod
from domains.entities import WeatherConditions
from datetime import datetime
from typing import List

class IWeatherDataGateway(ABC):
    @abstractmethod
    def get_weather_data(
        self, 
        latitude: str,
        longitude: str
    ) -> List[WeatherConditions]:
        pass