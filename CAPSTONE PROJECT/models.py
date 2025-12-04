# models.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import pandas as pd

@dataclass
class MeterReading:
    timestamp: pd.Timestamp
    kwh: float

@dataclass
class Building:
    name: str
    readings: List[MeterReading] = field(default_factory=list)

    def add_reading(self, timestamp, kwh):
        """Add a MeterReading (timestamp can be str or pd.Timestamp)."""
        ts = pd.to_datetime(timestamp)
        try:
            k = float(kwh)
        except Exception:
            # if invalid, skip adding
            return
        self.readings.append(MeterReading(ts, k))

    def total_consumption(self):
        return sum(r.kwh for r in self.readings)

    def to_dataframe(self):
        """Return readings as a DataFrame indexed by timestamp."""
        if not self.readings:
            return pd.DataFrame(columns=["timestamp", "kWh"]).set_index("timestamp")
        df = pd.DataFrame([{"timestamp": r.timestamp, "kWh": r.kwh} for r in self.readings])
        df = df.set_index("timestamp").sort_index()
        return df

    def summary_stats(self):
        df = self.to_dataframe()
        if df.empty:
            return {"mean": 0, "min": 0, "max": 0, "sum": 0}
        return {
            "mean": float(df["kWh"].mean()),
            "min": float(df["kWh"].min()),
            "max": float(df["kWh"].max()),
            "sum": float(df["kWh"].sum())
        }

class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def get_or_create(self, name):
        if name not in self.buildings:
            self.buildings[name] = Building(name=name)
        return self.buildings[name]

    def add_reading(self, building_name, timestamp, kwh):
        b = self.get_or_create(building_name)
        b.add_reading(timestamp, kwh)

    def combined_dataframe(self):
        """Return a single DataFrame with building column and timestamp index."""
        frames = []
        for name, building in self.buildings.items():
            df = building.to_dataframe().copy()
            if df.empty:
                continue
            df["Building"] = name
            frames.append(df.reset_index())
        if not frames:
            return pd.DataFrame(columns=["timestamp", "kWh", "Building"])
        combined = pd.concat(frames, ignore_index=True)
        combined = combined.rename(columns={"timestamp": "timestamp"})
        combined["timestamp"] = pd.to_datetime(combined["timestamp"])
        combined = combined.set_index("timestamp").sort_index()
        return combined