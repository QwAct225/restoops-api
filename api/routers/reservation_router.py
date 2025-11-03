from fastapi import APIRouter, Query
from typing import Optional
from services.database_service import fetch_table
import psycopg2
import psycopg2.extras
import os

router = APIRouter(prefix="/reservation", tags=["Reservation"])

@router.get("/")
def get_all_reservations(
    limit: Optional[int] = Query(None, description="Limit hasil (default: semua)"),
    min_duration: Optional[int] = Query(None, description="Minimum durasi reservasi (dalam jam)")
):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "postgres"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "restoops"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", "restoops123")
        )
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        query = "SELECT * FROM reservation_data WHERE 1=1"
        params = []
        
        if min_duration:
            query += " AND duration >= %s"
            params.append(min_duration)
        
        query += " ORDER BY id ASC"
        
        if limit:
            query += " LIMIT %s"
            params.append(limit)
        
        cursor.execute(query, params if params else None)
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        data = [dict(row) for row in results]
        
        return {
            "count": len(data),
            "data": data
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@router.get("/{reservation_id}")
def get_reservation_by_id(reservation_id: int):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "postgres"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "restoops"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", "restoops123")
        )
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        query = "SELECT * FROM reservation_data WHERE id = %s"
        cursor.execute(query, (reservation_id,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            return {"data": dict(result)}
        else:
            return {"status": "error", "detail": "Reservation not found"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@router.get("/token/{token}")
def get_reservation_by_token(token: str):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "postgres"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "restoops"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", "restoops123")
        )
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        query = "SELECT * FROM reservation_data WHERE token = %s"
        cursor.execute(query, (token.upper(),))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            return {"data": dict(result)}
        else:
            return {"status": "error", "detail": "Reservation not found"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@router.get("/table/{table_number}")
def get_reservations_by_table(table_number: int):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "postgres"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "restoops"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", "restoops123")
        )
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        query = "SELECT * FROM reservation_data WHERE reservation_table = %s ORDER BY id ASC"
        cursor.execute(query, (table_number,))
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        data = [dict(row) for row in results]
        
        return {
            "count": len(data),
            "table_number": table_number,
            "data": data
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}
