# sample_data_generator.py
import pandas as pd
from pathlib import Path
import numpy as np
from datetime import datetime, timedelta

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def generate_building_csv(building_name, start_date="2024-01-01", days=90, freq_minutes=60):
    """
    Create a CSV with timestamp,kWh rows for a building for `days` days with hourly readings.
    """
    periods = days * (24 * 60 // freq_minutes)
    rng = pd.date_range(start=start_date, periods=periods, freq=f"{freq_minutes}min")
    # create baseline consumption and daily pattern with noise
    base = {
        "Admin": 10,
        "Library": 6,
        "Hostel": 8,
        "Lab": 12,
        "Sports": 4
    }.get(building_name, 5)
    hours = rng.hour
    # simulate higher kWh during day/evening
    kwh = base + 2 * ((hours >= 8) & (hours <= 20)).astype(int) + np.random.normal(0, 0.8, size=len(rng))
    df = pd.DataFrame({"timestamp": rng, "kWh": np.round(kwh, 3)})
    # Add small chance of corrupt row to simulate "dirty" data
    if np.random.rand() < 0.2:
        df.loc[5, "kWh"] = "bad_val"
    # Save to CSV
    filename = DATA_DIR / f"{building_name}.csv"
    df.to_csv(filename, index=False)
    print(f"Generated {filename} ({len(df)} rows)")

if __name__ == "__main__":
    buildings = ["Admin", "Library", "Hostel", "Lab", "Sports"]
    for b in buildings:
        generate_building_csv(b, start_date="2024-09-01", days=60, freq_minutes=60)
    print("Sample CSV files created in ./data/")