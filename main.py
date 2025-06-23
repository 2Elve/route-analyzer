from datetime import datetime
from dependency_injector import containers, providers

from config.settings import Settings

from infrastructure.database.repositories import SQLiteTrafficRepository
from infrastructure.external.google_client import GoogleMapsClient
from infrastructure.scheduler import BackgroundScheduler

from interfaces.adapters.google_maps import GoogleMapsTrafficAdapter

from use_cases.data_collection.collect_traffic_data import CollectTrafficDataUseCase


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    settings = providers.Singleton(Settings)
    scheduler = providers.Singleton(BackgroundScheduler)

    # Clients
    google_client = providers.Factory(
        GoogleMapsClient,
        api_key=settings.provided.GOOGLE_MAPS_API_KEY
    )

    # Gateways
    traffic_gateway = providers.Factory(
        GoogleMapsTrafficAdapter,
        google_client=google_client
    )

    # Repositories
    traffic_repository = providers.Singleton(
        SQLiteTrafficRepository,
        db_path="traffic_data.db"
    )

    # Use Cases
    collect_traffic_use_case = providers.Factory(
        CollectTrafficDataUseCase,
        traffic_gateway=traffic_gateway,
        traffic_repo=traffic_repository
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
            print("✅ Data saved succesfully")
        else:
            print("⚠️ Collecting successfull! Error on saving data")
        return success
    except Exception as e:
        print(f"❌ Error while collecting data: {str(e)}")
        return False


def main():
    # Initialize Container
    container = Container()

    # Resolve Dependencies
    settings = container.settings()
    scheduler = container.scheduler()

    # Resolve collect_traffic_use_case
    use_case = container.collect_traffic_use_case()

    # Set Up Scheduler
    scheduler.schedule_hourly_job(
        collect_and_store_route_data,
        use_case=use_case,
        origin=settings.COORD1,
        destination=settings.COORD2
    )



if __name__ == "__main__":
    main()