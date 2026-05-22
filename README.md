# Real-Time Weather Streaming with Kafka and Faust

This project satisfies the ENGR 5785G Assignment 1 requirements, demonstrating a complete real-time machine learning pipeline using Apache Kafka, Confluent Cloud, and Faust-Streaming.

## Dataset
- **Name**: Weather (Oshawa/Toronto)
- **Source**: `climate.weather.gc.ca`
- **Task**: Predict next-hour temperature (`Temp (°C)`)
- **Process**: We fetched 3 months of 2023 hourly data for Toronto Pearson Int'l Airport using a custom python script (`data_fetcher.py`).

## Machine Learning Model
We trained a `LinearRegression` model offline using historical temperature, dew point, humidity, wind speed, visibility, and station pressure.
The model predicts the temperature of the *next* hour based on the current hour's conditions. It evaluates to a solid R-squared score and is saved as `weather_model.joblib`.

## Setup Instructions

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configuration**
   The `config.py` file contains the API keys and Bootstrap server information to connect to Confluent Cloud.

## How to Run

For the video demo, you should open **three separate terminals**, all pointing to the `weather_project` directory, and start them in the following order:

### Terminal 1: Stream Processor (Faust)
Start the Faust streaming application, which will sit and wait for raw data:
```bash
faust -A processor worker -l info
```

### Terminal 2: Output Consumer
Start the output consumer, which will wait for predictions:
```bash
python consumer.py
```

### Terminal 3: Producer
Finally, start the producer. It will read `weather.csv` row by row and send live Kafka events at ~1 row per second:
```bash
python producer.py
```

As the Producer sends data, the Processor will consume it, run the ML model, and output the prediction to the `predictions` topic, which the Output Consumer will pick up and display live!
