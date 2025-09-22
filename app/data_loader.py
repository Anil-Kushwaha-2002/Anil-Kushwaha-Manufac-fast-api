import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "data" / "fuel_prices.csv"

def load_data():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}. Place the NDAP CSV here.")

    # Read dataset, treat missing as 0
    df = pd.read_csv(DATA_PATH, encoding='utf-8')
    df.fillna(0, inplace=True)

    # Normalize column names: strip + lower
    df.columns = df.columns.str.strip()

    # Identify the long retail price column automatically (best-effort)
    long_price_col = None
    for col in df.columns:
        if "retail" in col.lower() and "price" in col.lower():
            long_price_col = col
            break

    if long_price_col is None:
        # fallback: try common names
        candidates = [c for c in df.columns if c.lower() in ("price", "retail_price", "rsp")]
        long_price_col = candidates[0] if candidates else None

    if long_price_col is None:
        raise ValueError("Could not find retail price column in dataset. Columns found: " + ", ".join(df.columns))

    # Standardize column names we will use in code
    df.rename(columns={
        long_price_col: "retail_price",
        "Products": "products",
        "Metro Cities": "metro_cities",
        "Calendar Day": "calendar_day",
        "Month": "month",
        "Year": "year",
        "Country": "country"
    }, inplace=True)

    # Ensure column names are lowercased & stripped
    df.columns = df.columns.str.strip().str.lower()

    # convert calendar_day to datetime if possible
    if "calendar_day" in df.columns:
        try:
            df["calendar_day"] = pd.to_datetime(df["calendar_day"], errors="coerce")
        except Exception:
            pass

    return df

# load once at module import
df = load_data()

