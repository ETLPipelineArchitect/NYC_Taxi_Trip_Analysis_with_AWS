from pyspark.sql import SparkSession

# Initialize Spark Session
spark = SparkSession.builder.appName("NYCTaxiDataAnalysis").getOrCreate()

# Load Processed Data
processed_data_path = "s3://your-bucket/nyc_taxi_data/processed/"
taxi_df = spark.read.parquet(processed_data_path)

taxi_df.createOrReplaceTempView("taxi_data")

# Analyze Data
busiest_pickups = spark.sql("""
  SELECT PULocationID, COUNT(*) as trip_count
  FROM taxi_data
  GROUP BY PULocationID
  ORDER BY trip_count DESC
  LIMIT 10
""")
busiest_pickups.show()

peak_hours = spark.sql("""
  SELECT pickup_hour, COUNT(*) as trip_count
  FROM taxi_data
  GROUP BY pickup_hour
  ORDER BY trip_count DESC
""")
peak_hours.show()

avg_fare_by_day = spark.sql("""
  SELECT pickup_day_of_week, AVG(fare_amount) as avg_fare
  FROM taxi_data
  GROUP BY pickup_day_of_week
  ORDER BY pickup_day_of_week
""")
avg_fare_by_day.show()

# Save Results to S3
busiest_pickups.write.csv("s3://your-bucket/nyc_taxi_data/output/busiest_pickups.csv", mode='overwrite')
peak_hours.write.csv("s3://your-bucket/nyc_taxi_data/output/peak_hours.csv", mode='overwrite')
avg_fare_by_day.write.csv("s3://your-bucket/nyc_taxi_data/output/avg_fare_by_day.csv", mode='overwrite')
