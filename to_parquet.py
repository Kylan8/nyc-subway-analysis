import pandas as pd
from pathlib import Path

RAW_DATA = Path("data/ridership_data.csv")
OUT_DIR = Path("data/cleaned_data")
CHUNK_SIZE = 1_000_000

COLUMN_DTYPES = {
    "transit_mode": "string",
    "station_complex_id": "string",
    "station_complex": "string",
    "borough": "string",
    "latitude": "float64",
    "longitude": "float64",
}   

USECOLS = [
    "transit_timestamp",
    "transit_mode",
    "station_complex_id",
    "station_complex",
    "borough",
    "ridership",
    "transfers",
    "latitude",
    "longitude",
]

def parse_timestamp(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, format="%m/%d/%Y %I:%M:%S %p")

def main() -> ():
    raw_data = pd.read_csv(RAW_DATA, chunksize=CHUNK_SIZE, dtype=COLUMN_DTYPES, usecols=USECOLS, thousands=",", low_memory=False)

    for i, chunk in enumerate(raw_data):
        chunk["transit_timestamp"] = parse_timestamp(chunk["transit_timestamp"])
        subway_mask = chunk["transit_mode"] == "subway"

        chunk = chunk[subway_mask]

        chunk = chunk.drop(columns="transit_mode")

        OUT_DIR.mkdir(parents=True, exist_ok=True)
        curr_path = OUT_DIR / f"part_{i:03d}.parquet"

        chunk.to_parquet(path=curr_path, index=False)


if __name__ == "__main__":
    main()
    