# main.py -- corrected for DailyDelhiClimateTest.csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1) Load CSV (make sure the CSV is in the same folder as main.py)
df = pd.read_csv("DailyDelhiClimateTest.csv")

# 2) Print columns to confirm names (run once)
print("Columns in CSV:", list(df.columns))

# 3) Convert date column and handle missing values
df['date'] = pd.to_datetime(df['date'])
df = df.fillna(method='ffill')   # forward-fill missing values

# 4) Select columns that actually exist in this dataset
# The DailyDelhiClimateTest.csv typically includes: date, meantemp, humidity, wind_speed, meanpressure
df = df[['date', 'meantemp', 'humidity', 'wind_speed', 'meanpressure']]

# 5) Basic statistics (Task 3)
print("\n--- Basic statistics ---")
print("Mean Temp:", np.mean(df['meantemp']))
print("Humidity Std:", np.std(df['humidity']))
print("Max Pressure:", np.max(df['meanpressure']))

# 6) Add month column for grouping
df['month'] = df['date'].dt.month

# # 7) Plot: Daily mean temperature
plt.figure(figsize=(10,4))
plt.plot(df['date'], df['meantemp'])
plt.xlabel("Date")
plt.ylabel("Mean Temperature (°C)")
plt.title("Daily Mean Temperature Trend")
plt.tight_layout()
plt.savefig("daily_temp.png")
plt.show()

# # 8) Plot: Humidity vs Mean Temperature (scatter)
plt.figure(figsize=(6,4))
plt.scatter(df['meantemp'], df['humidity'])
plt.xlabel("Mean Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.title("Humidity vs Mean Temperature")
plt.tight_layout()
plt.savefig("scatter_temp_humidity.png")
plt.show()

#  9) Plot: Average monthly wind speed (bar)
monthly_wind = df.groupby('month')['wind_speed'].mean()
plt.figure(figsize=(7,4))
monthly_wind.plot(kind='bar')
plt.xlabel("Month")
plt.ylabel("Average Wind Speed")
plt.title("Average Monthly Wind Speed")
plt.tight_layout()
plt.savefig("monthly_wind.png")
plt.show()

# 10) Export cleaned data
df.to_csv("cleaned_weather_data.csv", index=False)
print("\nCleaned data and plots saved to the project folder.")
print("Assignment complete!") 




