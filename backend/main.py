from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, numerology, zodiac, love, tarot, fortune, users, history
from app.database.mongodb import init_db
from datetime import datetime
import uvicorn
import os

app = FastAPI(
    title="FateVerse API - Ứng Dụng Xem Bói",
    description="API Backend cho ứng dụng xem bói FateVerse - Khám phá vận mệnh của bạn",
    version="1.0.0"
)

# Get CORS origins from environment variable
cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost,http://127.0.0.1:3000")
cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(numerology.router, prefix="/api/numerology", tags=["numerology"])
app.include_router(zodiac.router, prefix="/api/zodiac", tags=["zodiac"])
app.include_router(love.router, prefix="/api/love", tags=["love"])
app.include_router(tarot.router, prefix="/api/tarot", tags=["tarot"])
app.include_router(fortune.router, prefix="/api/fortune", tags=["fortune"])
app.include_router(history.router, prefix="/api/history", tags=["history"])

@app.on_event("startup")
async def startup_event():
    """Initialize database connections and indexes"""
    await init_db()

@app.get("/")
async def root():
    return {
        "message": "Chào mừng đến với FateVerse API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "description": "API cho ứng dụng xem bói FateVerse"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "FateVerse API"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)