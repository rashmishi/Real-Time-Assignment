import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import joblib

def train_and_save_model():
    print("Loading data...")
    try:
        df = pd.read_csv("weather.csv")
    except FileNotFoundError:
        print("Error: weather.csv not found. Please run data_fetcher.py first.")
        return

    print(f"Data loaded: {len(df)} rows.")

    # Sort by date/time
    if 'Date/Time (LST)' in df.columns:
        df = df.sort_values(by='Date/Time (LST)')
    
    # Predict the next hour's temperature
    df['Next_Temp'] = df['Temp (°C)'].shift(-1)
    df = df.dropna()

    # Features and Target
    feature_cols = ['Temp (°C)', 'Dew Point Temp (°C)', 'Rel Hum (%)', 'Wind Spd (km/h)', 'Visibility (km)', 'Stn Press (kPa)']
    # Ensure all feature columns exist
    feature_cols = [c for c in feature_cols if c in df.columns]
    
    X = df[feature_cols]
    y = df['Next_Temp']

    # Train/Test split (Sequential split since it's time series)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    print("Training Linear Regression model...")
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate
    predictions = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print(f"Model Evaluation -> MSE: {mse:.4f}, R2: {r2:.4f}")

    # Save the model and feature columns
    joblib.dump(model, "weather_model.joblib")
    joblib.dump(feature_cols, "feature_cols.joblib")
    
    print("Model saved to weather_model.joblib")

if __name__ == "__main__":
    train_and_save_model()
