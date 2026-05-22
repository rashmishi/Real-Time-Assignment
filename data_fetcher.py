import pandas as pd
import numpy as np

def generate_synthetic_weather_data():
    print("Generating Synthetic Weather Data for Toronto...")
    num_rows = 1000
    
    # Generate dates
    dates = pd.date_range(start="2023-01-01 00:00:00", periods=num_rows, freq='h') # lowercase 'h' for pandas 2.2.0+
    
    # Generate realistic weather patterns
    np.random.seed(42)
    time_of_day = np.arange(num_rows) % 24
    daily_temp_cycle = -5 * np.cos((time_of_day - 4) * 2 * np.pi / 24)
    base_temp = 5.0
    temp = base_temp + daily_temp_cycle + np.random.normal(0, 2, num_rows)
    
    dew_point = temp - np.random.uniform(1, 5, num_rows)
    humidity = np.clip(100 - (temp - dew_point) * 5, 20, 100)
    wind_spd = np.clip(np.random.normal(15, 10, num_rows), 0, 80)
    visibility = np.clip(np.random.normal(24, 5, num_rows), 0, 25)
    pressure = np.random.normal(101.3, 1.0, num_rows)

    df = pd.DataFrame({
        'Date/Time (LST)': dates.astype(str),
        'Temp (°C)': temp,
        'Dew Point Temp (°C)': dew_point,
        'Rel Hum (%)': humidity,
        'Wind Spd (km/h)': wind_spd,
        'Visibility (km)': visibility,
        'Stn Press (kPa)': pressure
    })
    
    df.to_csv("weather.csv", index=False)
    print(f"Saved synthetic weather data to weather.csv. Total rows: {len(df)}")

if __name__ == "__main__":
    generate_synthetic_weather_data()
