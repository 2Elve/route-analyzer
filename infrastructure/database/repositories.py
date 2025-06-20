import sqlite3
from domains.entities import Route
from domains.repositories import ITrafficRepository


class SQLiteTrafficRepository(ITrafficRepository):
    def __init__(self, db_path: str = "traffic_data.db"):
        self.db_path = db_path
        self._create_table()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def _create_table(self):

         with self._get_connection() as conn: 
            conn.execute("""
                CREATE TABLE IF NOT EXISTS routes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    route_type TEXT NOT NULL,
                    origin TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    distance_meters REAL NOT NULL,
                    duration_seconds REAL NOT NULL,
                    static_duration_seconds REAL NOT NULL,
                    polyline TEXT,
                    timestamp TEXT NOT NULL        
                )
            """
            )
            conn.commit()
    
    def save_route(self, route: Route) -> bool:
        

        with self._get_connection() as conn:
            try:
                conn.execute("""
                    INSERT INTO routes (
                        route_type, origin, destination, distance_meters,
                        duration_seconds, static_duration_seconds,
                        polyline, timestamp
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    route.route_type.name,
                    route.origin,
                    route.destination,
                    route.distance_meters,
                    route.duration_seconds,
                    route.static_duration_seconds,
                    route.encoded_polyline,
                    route.timestamp.isoformat()
                ))
                conn.commit()
                return True
            except Exception as e:
                print(f"Error saving route: {e}")
            return False