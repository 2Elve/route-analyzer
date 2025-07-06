from datetime import datetime
from typing import List

from infrastructure.external.weather_client import WeatherClient

from interfaces.gateways.weather_gateway import IWeatherDataGateway

from domains.entities import WeatherConditions


class WeatherAdapter(IWeatherDataGateway):
    def __init__(self, weather_client: WeatherClient):
        self.client = weather_client

    def get_weather_data(
        self, 
        latitude: str,
        longitude: str
    ):

        response = self.client.get_weather_conditions(latitude, longitude)

        weather = WeatherConditions(
            weather_type = response['weather'][0]['main'],
            weather_description= response['weather'][0]['description'],
            temperature = response['main']['temp'],
            feels_like = response['main']['feels_like'],
            pressure = response['main']['pressure'],
            visibility = response['visibility'],
            wind_speed = response['wind']['speed'],
            humidity = response['main']['humidity'],
            timestamp = datetime.now()
        )

        return weather




