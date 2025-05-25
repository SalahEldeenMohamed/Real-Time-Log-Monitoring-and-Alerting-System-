# Real-Time Log Monitoring System

## Project Overview
Monitors application logs using Kafka, Spark, Airflow, and Python scripts. Alerts if error rate exceeds threshold.

## Setup Instructions

### 1. Kafka
```bash
# Start services
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
bin/kafka-topics.sh --create --topic logs-topic --bootstrap-server localhost:9092
