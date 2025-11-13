from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from datetime import datetime
import psycopg2
import psycopg2.extras

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "restoops")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "restoops123")

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:     %(message)s'
)

app = FastAPI(
    title="RestoOps API",
    version="1.0.0",
    description="API untuk mengelola data menu dan reservasi restoran",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "🍽️ RestOops API is ready! Please go to /docs for API documentation.",
        "version": "1.0.0",
        "description": "API untuk mengelola data menu dan reservasi restoran",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json"
        },
        "endpoints": {
            "menu": "/menu",
            "reservation": "/reservation",
            "sync": "/sync",
            "health": "/health",
            "stats": "/stats"
        }
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "RestOops API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "api": "running",
        "database": "connected"
    }

@app.get("/stats", tags=["Statistics"])
def get_stats():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM menu_data")
        menu_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM reservation_data")
        reservation_count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return {
            "total_menus": menu_count,
            "total_reservations": reservation_count,
            "database": {
                "type": "PostgreSQL 17",
                "status": "connected"
            }
        }
    except Exception as e:
        return {
            "error": str(e),
            "database": {
                "type": "PostgreSQL 17",
                "status": "error"
            }
        }

from routers.menu_router import router as menu_router
from routers.reservation_router import router as reservation_router
from routers.sync_router import router as sync_router

app.include_router(menu_router)
app.include_router(reservation_router)
app.include_router(sync_router)
