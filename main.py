from datetime import datetime
import time
from dependency_injector import containers, providers

from config.settings import Settings

from infrastructure.database.repositories import (
    PostgresTrafficRepository, PostgresWeatherRepository,
    SQLiteTrafficRepository, SQLiteWeatherRepository
)

from infrastructure.external.google_client import GoogleMapsClient
from infrastructure.external.weather_client import WeatherClient
from infrastructure.scheduler import BackgroundScheduler

from interfaces.adapters.google_maps import GoogleMapsTrafficAdapter
from interfaces.adapters.open_weather import WeatherAdapter

from use_cases.data_collection.collect_traffic_data import CollectTrafficDataUseCase
from use_cases.data_collection.collect_weather_data import CollectWeatherDataUseCase


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    settings = providers.Singleton(Settings)
    scheduler = providers.Singleton(BackgroundScheduler)

    # Clients
    google_client = providers.Factory(
        GoogleMapsClient,
        api_key=settings.provided.GOOGLE_MAPS_API_KEY
    )

    weather_client = providers.Factory(
        WeatherClient,
        api_key=settings.provided.OPENWEATHER_API_KEY
    )

    # Gateways
    traffic_gateway = providers.Factory(
        GoogleMapsTrafficAdapter,
        google_client=google_client
    )

    weather_gateway = providers.Factory(
        WeatherAdapter,
        weather_client=weather_client
    )

    # Repositories - Production
    traffic_repository = providers.Singleton(
        PostgresTrafficRepository,
        db_config=settings.provided.db_config
    )

    weather_repository = providers.Singleton(
        PostgresWeatherRepository,
        db_config=settings.provided.db_config
    )

    # # Repositories - Development
    # traffic_repository = providers.Singleton(
    #     SQLiteTrafficRepository,
    #     db_path="traffic_data.db"
    # )

    # weather_repository = providers.Singleton(
    #     SQLiteWeatherRepository,
    #     db_path="traffic_data.db"
    # )

    # Use Cases
    collect_traffic_use_case = providers.Factory(
        CollectTrafficDataUseCase,
        traffic_gateway=traffic_gateway,
        traffic_repo=traffic_repository
    )

    collect_weather_use_case = providers.Factory(
        CollectWeatherDataUseCase,
        weather_gateway=weather_gateway,
        weather_repo=weather_repository
    )


def collect_and_store_route_data(
    use_case: CollectTrafficDataUseCase, 
    origin: str, 
    destination: str
) -> bool:

    print(f"🔍 Collecting Route Data: {origin} → {destination}")
    
    try:
        success = use_case.execute(origin, destination, round_trip=True)
        
        if success:
            print("✅ Traffic Data saved succesfully")
        else:
            print("⚠️ Traffic Data Collecting successfull! Error on saving data")
        return success
    except Exception as e:
        print(f"❌ Error while traffic collecting data: {str(e)}")
        return False
    
def collect_and_store_weather_data(
    use_case: CollectWeatherDataUseCase,
    longitude: float,
    latitude: float
) -> bool:
    print(f"🔍 Collecting Weather Data")
    try:
        success = use_case.execute(longitude, latitude)
        if success:
            print("✅ Weather Data saved succesfully")
        else:
            print("⚠️ Weather Collecting successfull! Error on saving data")
        return success
    except Exception as e:
        print(f"❌ Error while weather collecting data: {str(e)}")
        return False


def main():
    # Initialize Container
    container = Container()

    # Resolve Dependencies
    settings = container.settings()
    scheduler = container.scheduler()

    # Resolve use cases
    traffic_use_case = container.collect_traffic_use_case()
    weather_use_case = container.collect_weather_use_case()

    # Schedule - Traffic Data Collection
    scheduler.schedule_hourly_job(
        collect_and_store_route_data,
        use_case=traffic_use_case,
        origin=settings.COORD1,
        destination=settings.COORD2
    )

    # Schedule - Weather Data Collection
    scheduler.schedule_hourly_job(
        collect_and_store_weather_data,
        use_case=weather_use_case,
        longitude=settings.LONGITUDE,
        latitude=settings.LATITUDE
    )

    # Run script indefinitely 
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStoping Program...")


if __name__ == "__main__":
    main()