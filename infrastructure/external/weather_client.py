import requests
import json


class WeatherClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = 'https://api.openweathermap.org/data/2.5/weather'

    def get_weather_conditions(
        self,
        latitude: str,
        longitude: str
    ) -> json:
        
        params = f"?lat={latitude}&lon={longitude}&appid={self.api_key}&units=metric"

        response = requests.get(self.base_url + params)

        if response.status_code == 200:
            return response.json()

        return None