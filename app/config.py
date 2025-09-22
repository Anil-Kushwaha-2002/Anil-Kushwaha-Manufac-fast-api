# app/config.py

from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Path to dataset
DATA_FILE = BASE_DIR / "data" / "fuel_prices.csv"

# API settings
API_TITLE = "Fuel Price Analysis API"
API_VERSION = "1.0.0"
API_DESCRIPTION = """
This FastAPI service analyzes the Retail Selling Price (RSP) of Petrol and Diesel
in Metro Cities using the dataset provided by NDAP.
"""

# Default host and port for uvicorn (optional, can be used in Docker CMD)
HOST = "0.0.0.0"
PORT = 8000