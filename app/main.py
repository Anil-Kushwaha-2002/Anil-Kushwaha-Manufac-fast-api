from fastapi import FastAPI
from app.routes import router as api_router

app = FastAPI(
    title="Fuel Price Analytics API - Anil Kushwaha",
    description="Analyze Retail Selling Price (RSP) of Petrol & Diesel in Metro Cities (NDAP dataset)",
    version="1.0.0"
)

app.include_router(api_router)

