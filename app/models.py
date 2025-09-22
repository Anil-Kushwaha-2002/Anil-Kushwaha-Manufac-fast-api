from pydantic import BaseModel
from typing import Optional

class PriceRequest(BaseModel):
    city: str
    fuel_type: str

class PriceResponse(BaseModel):
    city: str
    fuel_type: str
    min_price: float
    max_price: float
    avg_price: float

class LatestPriceResponse(BaseModel):
    city: str
    fuel_type: str
    date: Optional[str]
    price: float


# from pydantic import BaseModel
# from typing import List, Optional

# class PriceRequest(BaseModel):
#     city: str
#     fuel_type: str  # Petrol / Diesel

# class PriceResponse(BaseModel):
#     city: str
#     fuel_type: str
#     min_price: float
#     max_price: float
#     avg_price: float
