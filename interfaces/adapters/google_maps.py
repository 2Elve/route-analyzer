from datetime import datetime
from typing import List

from infrastructure.external.google_client import GoogleMapsClient

from interfaces.gateways.traffic_gateway import ITrafficDataGateway

from domains.entities import Route, RouteType


class GoogleMapsTrafficAdapter(ITrafficDataGateway):
    def __init__(self, google_client: GoogleMapsClient):
        self.client = google_client
    
    def get_route_data(
        self, 
        origin: str, 
        destination: str
    ) -> List[Route]:


        response = self.client.get_directions(origin, destination)

        # ToDo: Raise no response exception

        routes = []

        for i, route in enumerate(response.get('routes', [])):
            leg = route['legs'][i]

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
                    timestamp = datetime.now()
                )
            )

        return routes

