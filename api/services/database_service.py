import psycopg2
import psycopg2.extras
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import os
from typing import Optional, Dict, List, Any

load_dotenv()

POSTGRES_CONFIG = {
    "dbname": os.getenv("DB_NAME", "restoops"),
    "user": os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASS", "restoops123"),
    "host": os.getenv("DB_HOST", "postgres"),
    "port": os.getenv("DB_PORT", "5432")
}

class DatabaseService:
    def __init__(self):
        self.postgres_config = POSTGRES_CONFIG
    
    def get_postgres_connection(self):
        try:
            return psycopg2.connect(**self.postgres_config)
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            raise
    
    def fetch_from_postgres(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        conn = self.get_postgres_connection()
        try:
            df = pd.read_sql(query, conn, params=params)
            df = df.replace([np.nan, np.inf, -np.inf], None)
            return df.to_dict(orient="records")
        except Exception as e:
            print(f"❌ Query execution error: {e}")
            return {"error": str(e)}
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: tuple = None) -> bool:
        conn = self.get_postgres_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"❌ Query execution error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    def bulk_insert(self, table_name: str, data: List[Dict[str, Any]]) -> bool:
        if not data:
            return False
        
        conn = self.get_postgres_connection()
        cursor = conn.cursor()
        try:
            columns = list(data[0].keys())
            columns_str = ", ".join(columns)
            placeholders = ", ".join(["%s"] * len(columns))
            
            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            values = [tuple(record[col] for col in columns) for record in data]
            
            cursor.executemany(query, values)
            conn.commit()
            
            print(f"✅ Successfully inserted {len(data)} records into {table_name}")
            return True
        except Exception as e:
            conn.rollback()
            print(f"❌ Bulk insert error: {e}")
            return False
        finally:
            cursor.close()
            conn.close()

def fetch_table(table_name: str, order_by: str = None) -> List[Dict[str, Any]]:
    db_service = DatabaseService()
    query = f"SELECT * FROM {table_name}"
    
    if order_by:
        query += f" ORDER BY {order_by} DESC"
    
    return db_service.fetch_from_postgres(query)
