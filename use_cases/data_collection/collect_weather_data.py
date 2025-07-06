from interfaces.gateways.weather_gateway import IWeatherDataGateway
from domains.repositories import IWeatherRepository
from typing import List, Tuple
from domains.entities import WeatherConditions


class CollectWeatherDataUseCase:
    def __init__(
        self, 
        weather_gateway: IWeatherDataGateway, 
        weather_repo: IWeatherRepository
    ):
        self.weather_gateway = weather_gateway
        self.weather_repo = weather_repo

    def execute(
        self,
        longitude: float,
        latitude: float
    ) -> bool:
        
        weather = self.weather_gateway.get_weather_data(longitude, latitude)
        return self.weather_repo.save_weather(weather)
        








