from confluent_kafka.admin import AdminClient, NewTopic
import config

def create_topics():
    admin = AdminClient({
        'bootstrap.servers': config.KAFKA_BOOTSTRAP_SERVERS,
        'security.protocol': config.KAFKA_SECURITY_PROTOCOL,
        'sasl.mechanisms': config.KAFKA_SASL_MECHANISM,
        'sasl.username': config.KAFKA_API_KEY,
        'sasl.password': config.KAFKA_API_SECRET,
    })

    # Confluent Cloud requires replication_factor=3
    topics = [
        NewTopic(config.RAW_TOPIC, num_partitions=1, replication_factor=3),
        NewTopic(config.PREDICTIONS_TOPIC, num_partitions=1, replication_factor=3)
    ]
    
    fs = admin.create_topics(topics)
    for topic, f in fs.items():
        try:
            f.result()
            print(f"Topic '{topic}' created successfully.")
        except Exception as e:
            print(f"Failed to create topic '{topic}': {e}")

if __name__ == "__main__":
    create_topics()
