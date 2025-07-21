from datetime import datetime, timezone
from typing import List
import pytz

from infrastructure.external.google_client import GoogleMapsClient

from interfaces.gateways.traffic_gateway import ITrafficDataGateway

from domains.entities import Route, RouteType


class GoogleMapsTrafficAdapter(ITrafficDataGateway):
    def __init__(self, google_client: GoogleMapsClient):
        self.client = google_client
        self.cdmx_tz = pytz.timezone('America/Mexico_City')
    
    def get_route_data(
        self, 
        origin: str, 
        destination: str
    ) -> List[Route]:

        response = self.client.get_directions(origin, destination)

        # Obtain current cdmx time
        cdmx_time = datetime.now(self.cdmx_tz).replace(second=0, microsecond=0)
        utc_time = cdmx_time.astimezone(timezone.utc)

        routes = []

        for i, route in enumerate(response.get('routes', [])):
            leg = route['legs'][0]

            route_type = RouteType.PRIMARY if i == 0 else RouteType.ALTERNATIVE

            routes.append(
                Route(
                    route_type = route_type,
                    origin = origin,
                    destination = destination,
                    distance_meters = leg['distanceMeters'],
                    duration_seconds = float(leg['duration'].replace('s', '')),
                    static_duration_seconds = float(leg['staticDuration'].replace('s', '')),
                    encoded_polyline = leg["polyline"]["encodedPolyline"],
                    timestamp = utc_time
                )
            )

        return routes

