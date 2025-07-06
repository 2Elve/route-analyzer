from datetime import datetime, timedelta, timezone
import requests
import json



class GoogleMapsClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = 'https://routes.googleapis.com/directions/v2:computeRoutes'

    def get_directions(self, origin: str, destination: str) -> json:
        try:

            headers = {
                "Content-Type": "application/json",
                "X-Goog-Api-Key": self.api_key,
                "X-Goog-FieldMask": "routes.legs.distanceMeters,routes.legs.duration,routes.legs.staticDuration,routes.legs.polyline.encodedPolyline,routes.legs.startLocation.latLng.latitude,routes.legs.startLocation.latLng.longitude"
            }

            # Request information 2 minutes ahead of current time
            _departure_time = (datetime.now(timezone.utc) + timedelta(minutes=2)).isoformat()

            data = {
                "origin": {
                    "placeId": origin
                },
                "destination": {
                    "placeId": destination
                },
                "travelMode": "DRIVE",
                "routingPreference": "TRAFFIC_AWARE",
                "departureTime": _departure_time,
                "computeAlternativeRoutes": True,
                "routeModifiers": {
                        "avoidTolls": False,
                        "avoidHighways": False
                },
            }

            response = requests.post(
                self.base_url,
                headers=headers,
                data=json.dumps(data)
            )

            return response.json()

        except Exception as e:
            print("Error while fetching Google API Data")