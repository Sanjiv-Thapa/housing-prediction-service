from fastapi import FastAPI
from .api.v1 import predict
from .database import engine, Base
from .models import db_models
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pathlib import Path

db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Housing Price Prediction Service",
    description="A production-ready API using XGBoost and FastAPI",
    version="1.0.0"
)

# Get the correct path to static directory
# __file__ is app/main.py, so parent.parent gets project root
BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

print(f"📁 Base Directory: {BASE_DIR}")
print(f"📁 Static Directory: {STATIC_DIR}")
print(f"✓ Static directory exists: {STATIC_DIR.exists()}")

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", tags=["UI"])
async def read_index():
    """Serves the custom HTML frontend."""
    index_path = STATIC_DIR / "index.html"
    print(f"🔍 Looking for index.html at: {index_path}")
    print(f"✓ File exists: {index_path.exists()}")
    
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": f"Frontend not found at {index_path}"}

app.include_router(predict.router, prefix="/api/v1/predict", tags=["Prediction"])

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "housing-prediction-api"}