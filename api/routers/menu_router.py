from fastapi import APIRouter, Query
from typing import Optional
from services.database_service import fetch_table
import psycopg2
import psycopg2.extras
import os

router = APIRouter(prefix="/menu", tags=["Menu"])

@router.get("/")
def get_all_menu(
    limit: Optional[int] = Query(None, description="Limit hasil (default: semua)"),
    sold_out: Optional[str] = Query(None, description="Filter berdasarkan sold_out status: 'Yes' or 'No'")
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
        
        query = "SELECT * FROM menu_data WHERE 1=1"
        params = []
        
        if sold_out:
            query += " AND sold_out = %s"
            params.append(sold_out)
        
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

@router.get("/{menu_id}")
def get_menu_by_id(menu_id: int):
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "postgres"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "restoops"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASS", "restoops123")
        )
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        query = "SELECT * FROM menu_data WHERE id = %s"
        cursor.execute(query, (menu_id,))
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        if result:
            return {"data": dict(result)}
        else:
            return {"status": "error", "detail": "Menu not found"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}
