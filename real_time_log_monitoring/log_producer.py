from kafka import KafkaProducer
import json
import time
import random
from datetime import datetime

# Kafka Producer connects to Kafka broker
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Convert dict to JSON bytes
)

# Sample data
log_levels = ['INFO', 'WARNING', 'ERROR']
messages = ['User login', 'Payment processed', 'Server crash', 'Database timeout']

# Send log every 2 seconds
while True:
    log = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "level": random.choice(log_levels),
        "message": random.choice(messages)
    }
    producer.send('logs-topic', value=log)
    print("Sent log:", log)
    time.sleep(2)
