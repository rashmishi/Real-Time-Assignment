import faust
import joblib
import config
import logging
import ssl
import json

# Ensure logging is set up to see Faust output
logging.basicConfig(level=logging.INFO)

# Define the Faust app
app = faust.App(
    'weather_processor',
    broker=f'kafka://{config.KAFKA_BOOTSTRAP_SERVERS}',
    broker_credentials=faust.SASLCredentials(
        username=config.KAFKA_API_KEY,
        password=config.KAFKA_API_SECRET,
        ssl_context=ssl.create_default_context(),
        mechanism=config.KAFKA_SASL_MECHANISM
    ),
    topic_replication_factor=3,
    web_port=6067,
)

# Define Topics
raw_topic = app.topic(config.RAW_TOPIC, value_type=bytes)
predictions_topic = app.topic(config.PREDICTIONS_TOPIC, value_serializer='json')

# We load model at module level so agents can access it
print("Loading ML model...")
model = joblib.load("weather_model.joblib")
feature_cols = joblib.load("feature_cols.joblib")
print("Model loaded successfully.")

@app.agent(raw_topic)
async def process_weather_data(stream):
    async for raw_record in stream:
        try:
            if isinstance(raw_record, (bytes, bytearray)):
                record = json.loads(raw_record.decode('utf-8'))
            elif isinstance(raw_record, str):
                record = json.loads(raw_record)
            else:
                record = raw_record
            
            # Extract features for prediction
            features = [[record.get(col, 0) for col in feature_cols]]
            
            # Predict
            prediction = model.predict(features)[0]
            
            # Prepare output message
            output = {
                "timestamp": record.get("Date/Time (LST)", "unknown"),
                "current_temp": record.get("Temp (°C)", None),
                "predicted_next_temp": round(float(prediction), 2)
            }
            
            # Send to predictions topic
            print(f"Predicted: {output}")
            await predictions_topic.send(value=output)
            
        except Exception as e:
            print(f"Error processing record: {e}")

if __name__ == '__main__':
    app.main()
