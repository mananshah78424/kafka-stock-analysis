from json import loads

from kafka import KafkaConsumer
from kafka.errors import KafkaError

broker = "localhost:9092"
topicname = "stockPrice"

try:
    consumer = KafkaConsumer(
        topicname,
        bootstrap_servers=[broker],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
    )

    print("Consumer started. Waiting for messages...")

    for message in consumer:
        print(f"Received message: {message.value}")

except KafkaError as e:
    print(f"Kafka error occurred: {e}")
except Exception as e:
    print(f"An error occurred: {e}")
