from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType

# Create Spark Session
spark = SparkSession.builder \
    .appName("Log Processor") \
    .getOrCreate()

# Define schema of logs
schema = StructType() \
    .add("timestamp", StringType()) \
    .add("level", StringType()) \
    .add("message", StringType())

# Read stream from Kafka topic
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "logs-topic") \
    .load()

# Convert Kafka byte stream to JSON
logs = df.selectExpr("CAST(value AS STRING)") \
         .select(from_json(col("value"), schema).alias("data")) \
         .select("data.*")

# Filter only ERROR logs
error_logs = logs.filter("level = 'ERROR'")

# Save ERROR logs to JSON files
query = error_logs.writeStream \
    .format("json") \
    .option("path", "logs_output/") \
    .option("checkpointLocation", "checkpoint/") \
    .start()

query.awaitTermination()
