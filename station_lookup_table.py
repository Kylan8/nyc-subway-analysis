import pandas as pd

data = pd.read_parquet("data/cleaned_data", columns=["station_complex_id", "longitude", "latitude", "borough", "station_complex"])
stations = data.drop_duplicates()

stations.to_parquet("data/stations.parquet", index=False)
