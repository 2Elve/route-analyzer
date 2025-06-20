from datetime import datetime
from dependency_injector import containers, providers

from config.settings import Settings

from infrastructure.database.repositories import SQLiteTrafficRepository
from infrastructure.external.google_client import GoogleMapsClient

from interfaces.gateways.traffic_gateway import ITrafficDataGateway
from interfaces.adapters.google_maps import GoogleMapsTrafficAdapter

from use_cases.data_collection.collect_traffic_data import CollectTrafficDataUseCase


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    settings = providers.Singleton(Settings)

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
    origin: str, destination: str
) -> bool:

    print(f"🔍 Collecting Route Data: {origin} → {destination}")
    
    try:
        success = use_case.execute(origin, destination)
        
        if success:
            print("✅ Data saved succesfully")
        else:
            print("⚠️ Collecting successfull! Error on saving data")
        return success
    except Exception as e:
        print(f"❌ Error while collecting data: {str(e)}")
        return False


def main():

    HOME_ID = 'ChIJYcUBb5Uf0oUR3yCLWrs9jSM'
    GTBC_ID = 'ChIJsyuN_YAD0oUR_m4u3bj6SvQ'
    #PERI_SUR_ID = 'ChIJBeT2ewD_zYURkEcbmfayHZ4'

    # Initialize Container
    container = Container()

    # Resolve collect_traffic_use_case
    use_case = container.collect_traffic_use_case()

    collect_and_store_route_data(
        use_case=use_case,
        origin=HOME_ID,
        destination=GTBC_ID
    )





if __name__ == "__main__":
    main()