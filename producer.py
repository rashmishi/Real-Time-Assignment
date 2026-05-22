import json
import time
import pandas as pd
from confluent_kafka import Producer
import config

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed for record {msg.key()}: {err}")
    else:
        print(f"Record successfully produced to {msg.topic()} [{msg.partition()}]")

def create_producer():
    conf = {
        'bootstrap.servers': config.KAFKA_BOOTSTRAP_SERVERS,
        'security.protocol': config.KAFKA_SECURITY_PROTOCOL,
        'sasl.mechanisms': config.KAFKA_SASL_MECHANISM,
        'sasl.username': config.KAFKA_API_KEY,
        'sasl.password': config.KAFKA_API_SECRET,
        'client.id': 'weather-producer'
    }
    return Producer(conf)

def run_producer():
    print("Initializing Producer...")
    producer = create_producer()
    
    print("Loading weather data...")
    try:
        df = pd.read_csv("weather.csv")
    except FileNotFoundError:
        print("Error: weather.csv not found!")
        return

    print("Starting to stream data at ~1 row/second...")
    for index, row in df.iterrows():
        record_value = row.to_dict()
        json_value = json.dumps(record_value)
        
        producer.produce(
            topic=config.RAW_TOPIC,
            key=str(index).encode('utf-8'),
            value=json_value.encode('utf-8'),
            on_delivery=delivery_report
        )
        producer.poll(0)
        time.sleep(1)

    print("Flushing records...")
    producer.flush()
    print("Done.")

if __name__ == "__main__":
    run_producer()
