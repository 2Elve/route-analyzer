from datetime import datetime
from typing import List
import pytz

from infrastructure.external.weather_client import WeatherClient

from interfaces.gateways.weather_gateway import IWeatherDataGateway

from domains.entities import WeatherConditions


class WeatherAdapter(IWeatherDataGateway):
    def __init__(self, weather_client: WeatherClient):
        self.client = weather_client
        self.cdmx_tz = pytz.timezone('America/Mexico_City')

    def get_weather_data(
        self, 
        latitude: str,
        longitude: str
    ):

        response = self.client.get_weather_conditions(latitude, longitude)

        # Obtain current cdmx time
        cdmx_time = datetime.now(self.cdmx_tz).replace(second=0, microsecond=0)

        weather = WeatherConditions(
            weather_type = response['weather'][0]['main'],
            weather_description= response['weather'][0]['description'],
            temperature = response['main']['temp'],
            feels_like = response['main']['feels_like'],
            pressure = response['main']['pressure'],
            visibility = response['visibility'],
            wind_speed = response['wind']['speed'],
            humidity = response['main']['humidity'],
            timestamp = cdmx_time
        )

        return weather




