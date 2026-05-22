import json
from confluent_kafka import Consumer
import config

def run_consumer():
    # Configure Consumer
    conf = {
        'bootstrap.servers': config.KAFKA_BOOTSTRAP_SERVERS,
        'security.protocol': 'SASL_SSL',
        'sasl.mechanisms': config.KAFKA_SASL_MECHANISM,
        'sasl.username': config.KAFKA_API_KEY,
        'sasl.password': config.KAFKA_API_SECRET,
        'group.id': 'weather_output_consumer_2',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(conf)
    consumer.subscribe([config.PREDICTIONS_TOPIC])

    print(f"Waiting for predictions on '{config.PREDICTIONS_TOPIC}'. Press Ctrl+C to stop.")
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue

            # Parse and print
            value = msg.value().decode('utf-8')
            try:
                data = json.loads(value)
                print("--- New Prediction Received ---")
                print(f"Timestamp: {data.get('timestamp')}")
                print(f"Current Temp: {data.get('current_temp')} °C")
                print(f"Predicted Next Hour: {data.get('predicted_next_temp')} °C\n")
            except json.JSONDecodeError:
                print(f"Raw Message: {value}")

    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        consumer.close()

if __name__ == "__main__":
    run_consumer()
