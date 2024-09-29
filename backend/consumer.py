from kafka import KafkaConsumer
import json

def consume_messages(topic):
    """Consume messages from the Kafka topic."""
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=["localhost:9092"],
        auto_offset_reset="earliest",
        group_id="consumer-group-1",
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )
    
    try:
        print(f"Listening to topic {topic}...")
        for message in consumer:
            print(f"Received message: {message.value}")
    except Exception as e:
        print(f"Failed to consume message: {e}")
    finally:
        consumer.close()

if __name__ == "__main__":
    consume_messages("real_time_data")
