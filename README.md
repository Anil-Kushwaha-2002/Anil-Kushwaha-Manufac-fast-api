# Anil-Kushwaha-Manufac-fast-api
# Fuel Price Analytics API - Anil Kushwaha

This is a FastAPI-based backend service to analyze **Retail Selling Price (RSP) of Petrol and Diesel in Metro Cities**.  
Dataset: [NDAP (NITI Aayog)](https://ndap.niti.gov.in/dataset/7916)  
https://drive.google.com/file/d/1Zgb8KVmKoEWvk_3kMq9TVV7KDTujkfPd/view

### Features

- Get list of available metro cities  
- Analyze **min, max, avg** fuel price for a city & fuel type  
- Get **latest price** for a city & fuel type  
- Interactive API docs via Swagger UI (`/docs`)  

---

### Tech Stack

- **FastAPI** (Python backend framework)  
- **Pandas** (data analysis)  
- **Poetry** (dependency management)  
- **Docker** (containerization)  

---

## Project Structure
```
anil-kushwaha-manufac-fast-api/
│── app/
│ ├── init.py
│ ├── main.py # Entry point
│ ├── routes.py # API routes
│ ├── models.py # Pydantic schemas
│ ├── data_loader.py # Loads & preprocesses dataset
│── data/
│ └── fuel_prices.csv # Dataset (NDAP)
│── pyproject.toml # Poetry dependencies
│── Dockerfile # Docker build file
│── README.md # Project docs
```
---
## Installation & Usage
### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/anil-kushwaha-manufac-fast-api.git
cd anil-kushwaha-manufac-fast-api
```
### 2. Install dependencies using Poetry
```bash
poetry install
```

### 3. Run FastAPI server
```bash
poetry run uvicorn app.main:app --reload
```

### Server will start at:
👉 http://127.0.0.1:8000

### Docs available at:
- Swagger UI → http://127.0.0.1:8000/docs
- ReDoc → http://127.0.0.1:8000/redoc
---
---
## Example API Calls
### Get Cities
```bash
curl -X GET "http://127.0.0.1:8000/cities" -H "accept: application/json"
```
### Price Analysis (GET)
```bash
curl -X GET "http://127.0.0.1:8000/price_analysis?city=Delhi&fuel_type=Petrol"
```
### Price Analysis (POST)
```bash
curl -X POST "http://127.0.0.1:8000/price_analysis" \
    -H "Content-Type: application/json" \
    -d '{"city":"Delhi", "fuel_type":"Diesel"}'
```
### Latest Price
```bash
curl -X GET "http://127.0.0.1:8000/latest_price?city=Mumbai&fuel_type=Diesel"
```
# Docker Setup
### 1. Build Docker image
```bash
docker build -t fuel-api .
```
### 2. Run container
```bash
docker run -p 8000:8000 fuel-api
```
## API available at:
👉 http://127.0.0.1:8000/docs
