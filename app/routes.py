from fastapi import APIRouter, HTTPException, Query
from typing import List
from app.data_loader import df
from app.models import PriceRequest, PriceResponse, LatestPriceResponse
import pandas as pd
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse


router = APIRouter()

@router.get("/")
def root():
    return RedirectResponse(url="/docs")

@router.get("/cities", response_model=List[str])
def get_cities():
    """Return list of unique metro cities."""
    if "metro_cities" not in df.columns:
        raise HTTPException(status_code=500, detail="Dataset missing 'metro_cities' column.")
    cities = sorted(df["metro_cities"].dropna().unique().tolist())
    return cities

@router.get("/price_analysis", response_model=PriceResponse)
def price_analysis_get(city: str = Query(...), fuel_type: str = Query(...)):
    """
    Get min, max, avg price for the given city and fuel type (Products column).
    Example: /price_analysis?city=Delhi&fuel_type=Petrol
    """
    # Normalize input
    city = city.strip().lower()
    fuel_type = fuel_type.strip().lower()

    # Ensure columns exist
    if "metro_cities" not in df.columns or "products" not in df.columns or "retail_price" not in df.columns:
        raise HTTPException(status_code=500, detail="Dataset missing required columns.")

    # Filter rows
    mask_city = df["metro_cities"].astype(str).str.strip().str.lower() == city
    mask_fuel = df["products"].astype(str).str.strip().str.lower() == fuel_type

    filtered = df[mask_city & mask_fuel]

    if filtered.empty:
        # More diagnostic info
        available_cities = df["metro_cities"].astype(str).str.strip().str.lower().unique().tolist()
        available_fuels = df["products"].astype(str).str.strip().str.lower().unique().tolist()
        raise HTTPException(
            status_code=404,
            detail=f"No records found for city='{city}' and fuel_type='{fuel_type}'. "
                f"Available cities: {available_cities[:10]} ...; Available fuel types: {available_fuels}"
        )

    # Compute stats (treat retail_price as numeric)
    prices = pd.to_numeric(filtered["retail_price"], errors="coerce").fillna(0)
    return PriceResponse(
        city=city,
        fuel_type=fuel_type,
        min_price=float(prices.min()),
        max_price=float(prices.max()),
        avg_price=float(prices.mean())
    )

@router.post("/price_analysis", response_model=PriceResponse)
def price_analysis_post(request: PriceRequest):
    return price_analysis_get(city=request.city, fuel_type=request.fuel_type)

@router.get("/latest_price", response_model=LatestPriceResponse)
def latest_price(city: str = Query(...), fuel_type: str = Query(...)):
    """
    Return the most recent record (by calendar_day if present) for city+fuel type.
    """
    city = city.strip().lower()
    fuel_type = fuel_type.strip().lower()

    if "metro_cities" not in df.columns or "products" not in df.columns or "retail_price" not in df.columns:
        raise HTTPException(status_code=500, detail="Dataset missing required columns.")

    mask_city = df["metro_cities"].astype(str).str.strip().str.lower() == city
    mask_fuel = df["products"].astype(str).str.strip().str.lower() == fuel_type
    filtered = df[mask_city & mask_fuel].copy()

    if filtered.empty:
        raise HTTPException(status_code=404, detail="No data for given city and fuel type.")

    # If calendar_day exists and is datetime, use it
    if "calendar_day" in filtered.columns and filtered["calendar_day"].dtype.kind in ("M",):
        filtered = filtered.sort_values("calendar_day", ascending=False)
        latest = filtered.iloc[0]
        date_val = latest.get("calendar_day")
        date_str = str(date_val.date()) if hasattr(date_val, "date") else str(date_val)
    else:
        # fallback: take last row by index
        latest = filtered.iloc[-1]
        date_str = latest.get("calendar_day", None)

    price = float(pd.to_numeric(latest["retail_price"], errors="coerce") or 0.0)

    return LatestPriceResponse(city=city, fuel_type=fuel_type, date=date_str, price=price)



# from fastapi import APIRouter, HTTPException
# from typing import List
# from app.data_loader import df
# from app.models import PriceRequest, PriceResponse

# router = APIRouter()

# @router.get("/cities", response_model=List[str])
# def get_cities():
#     """Return list of all cities in the dataset"""
#     return df['Metro Cities'].unique().tolist()


# @router.get("/price_analysis")
# def price_analysis_get(city: str, fuel_type: str):
#     # Filter by city
#     city_df = df[df['Metro Cities'].str.lower() == city.lower()]
#     if city_df.empty:
#         raise HTTPException(status_code=404, detail="City not found")

#     # Filter by fuel type (Products column)
#     fuel_df = city_df[city_df['Products'].str.lower() == fuel_type.lower()]
#     if fuel_df.empty:
#         raise HTTPException(status_code=404, detail="Fuel type not found")

#     # Rename long column for readability
#     price_col = "Retail Selling Price (Rsp) Of Petrol And Diesel (UOM:INR/L(IndianRupeesperLitre)), Scaling Factor:1"

#     return {
#         "city": city,
#         "fuel_type": fuel_type,
#         "min_price": float(fuel_df[price_col].min()),
#         "max_price": float(fuel_df[price_col].max()),
#         "avg_price": float(fuel_df[price_col].mean())
#     }


# # ✅ POST version with Pydantic models
# @router.post("/price_analysis", response_model=PriceResponse)
# def price_analysis(request: PriceRequest):
#     """Analyze price of a fuel type in a city"""
#     # Filter by city
#     city_df = df[df['Metro Cities'].str.lower() == request.city.lower()]
#     if city_df.empty:
#         raise HTTPException(status_code=404, detail="City not found")

#     # Filter by fuel type
#     fuel_df = city_df[city_df['Products'].str.lower() == request.fuel_type.lower()]
#     if fuel_df.empty:
#         raise HTTPException(status_code=404, detail="Fuel type not found")

#     # Price column
#     price_col = "Retail Selling Price (Rsp) Of Petrol And Diesel (UOM:INR/L(IndianRupeesperLitre)), Scaling Factor:1"

#     min_price = fuel_df[price_col].min()
#     max_price = fuel_df[price_col].max()
#     avg_price = fuel_df[price_col].mean()

#     return PriceResponse(
#         city=request.city,
#         fuel_type=request.fuel_type,
#         min_price=float(min_price),
#         max_price=float(max_price),
#         avg_price=float(avg_price)
#     )


