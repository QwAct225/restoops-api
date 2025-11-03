from fastapi import FastAPI
from routers import menu_router, reservation_router, sync_router
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s:     %(message)s'
)

app = FastAPI(
    title="RestOops API",
    description="API untuk menampilkan data menu dan reservasi restaurant",
    version="1.0.0",
)

@app.get("/")
def root():
    return {
        "message": "🍽️ RestOops API is ready! Please go to /docs for API documentation.",
        "version": "1.0.0",
        "endpoints": {
            "documentation": "/docs",
            "health": "/health",
            "menu": "/menu",
            "reservation": "/reservation",
            "sync": "/sync"
        }
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "RestOops API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": "running"
    }

app.include_router(menu_router.router)
app.include_router(reservation_router.router)
app.include_router(sync_router.router)
