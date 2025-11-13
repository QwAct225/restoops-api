from fastapi import APIRouter
from services.database_service import DatabaseService
import pandas as pd
import os
import json

router = APIRouter(prefix="/sync", tags=["Data Sync"])

@router.post("/menu")
def sync_menu_data():
    try:
        csv_path = "/app/data/processed/menu_data.csv"
        
        if not os.path.exists(csv_path):
            return {
                "status": "error",
                "detail": f"File not found: {csv_path}"
            }
        
        df = pd.read_csv(csv_path)
        records = df.to_dict(orient="records")
        db_service = DatabaseService()
        db_service.execute_query("TRUNCATE TABLE menu_data CASCADE")
        success = db_service.bulk_insert("menu_data", records)
        
        if success:
            return {
                "status": "success",
                "message": "Menu data synced successfully",
                "records_synced": len(records)
            }
        else:
            return {
                "status": "error",
                "detail": "Failed to sync menu data"
            }
    except Exception as e:
        return {
            "status": "error",
            "detail": str(e)
        }

@router.post("/reservation")
def sync_reservation_data():
    try:
        csv_path = "/app/data/processed/reservation_data.csv"
        
        if not os.path.exists(csv_path):
            return {
                "status": "error",
                "detail": f"File not found: {csv_path}"
            }
        
        df = pd.read_csv(csv_path)
        records = df.to_dict(orient="records")
        db_service = DatabaseService()
        db_service.execute_query("TRUNCATE TABLE reservation_data CASCADE")
        success = db_service.bulk_insert("reservation_data", records)
        
        if success:
            return {
                "status": "success",
                "message": "Reservation data synced successfully",
                "records_synced": len(records)
            }
        else:
            return {
                "status": "error",
                "detail": "Failed to sync reservation data"
            }
    except Exception as e:
        return {
            "status": "error",
            "detail": str(e)
        }

@router.post("/all")
def sync_all_data():
    menu_result = sync_menu_data()
    reservation_result = sync_reservation_data()
    
    return {
        "menu": menu_result,
        "reservation": reservation_result
    }

@router.get("/status")
def get_sync_status():
    try:
        db_service = DatabaseService()
        
        menu_count_query = "SELECT COUNT(*) as count FROM menu_data"
        menu_result = db_service.fetch_from_postgres(menu_count_query)
        menu_count = menu_result[0]["count"] if menu_result else 0
        
        reservation_count_query = "SELECT COUNT(*) as count FROM reservation_data"
        reservation_result = db_service.fetch_from_postgres(reservation_count_query)
        reservation_count = reservation_result[0]["count"] if reservation_result else 0
        
        return {
            "status": "success",
            "data": {
                "menu_records": menu_count,
                "reservation_records": reservation_count,
                "total_records": menu_count + reservation_count
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "detail": str(e)
        }
