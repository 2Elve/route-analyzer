from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto


class RouteType(Enum):
    PRIMARY = auto()
    ALTERNATIVE = auto()

@dataclass
class Route:
    route_type: RouteType
    origin: str
    destination: str
    distance_meters: float
    duration_seconds: float
    static_duration_seconds: float
    encoded_polyline: str
    timestamp: datetime

@dataclass
class WeatherConditions:
    weather_type: str
    weather_description: str
    temperature: float
    feels_like: float
    pressure: float
    visibility: int
    wind_speed: float
    humidity: float
    timestamp: datetime
