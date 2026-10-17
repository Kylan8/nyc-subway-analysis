import pandas as pd

data = pd.read_parquet("data/cleaned_data", columns=["transit_timestamp", "station_complex_id", "ridership"])

hourly = data.groupby(["transit_timestamp", "station_complex_id"], as_index=False)["ridership"].sum()

hourly.to_parquet("data/hourly.parquet", index=False)