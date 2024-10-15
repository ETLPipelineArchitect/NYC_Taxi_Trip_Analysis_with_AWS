from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, hour, dayofweek, regexp_replace
from pyspark.sql.types import DoubleType, IntegerType
from pyspark.sql.functions import unix_timestamp, when

# Initialize Spark Session
spark = SparkSession.builder.appName("NYCTaxiDataAnalysis").getOrCreate()

# Read Data from S3
taxi_df = spark.read.csv("s3://your-bucket/nyc_taxi_data/raw/*.csv", header=True, inferSchema=True)

# Data Cleaning and Transformation
taxi_df = taxi_df.dropna(how='any')

taxi_df = taxi_df.withColumn('passenger_count', col('passenger_count').cast(IntegerType()))\
    .withColumn('trip_distance', col('trip_distance').cast(DoubleType()))\
    .withColumn('fare_amount', col('fare_amount').cast(DoubleType()))\
    .withColumn('tip_amount', col('tip_amount').cast(DoubleType()))\
    .withColumn('pickup_datetime', to_timestamp(col('tpep_pickup_datetime'), 'yyyy-MM-dd HH:mm:ss'))\
    .withColumn('dropoff_datetime', to_timestamp(col('tpep_dropoff_datetime'), 'yyyy-MM-dd HH:mm:ss'))\
    .withColumn('trip_duration', (unix_timestamp('dropoff_datetime') - unix_timestamp('pickup_datetime')) / 60)\
    .withColumn('vendor_id', regexp_replace('VendorID', r'[^0-9]', '').cast(IntegerType()))\
    .filter((col('trip_duration') > 0) & (col('trip_duration') < 120))\
    .filter((col('trip_distance') > 0) & (col('trip_distance') < 100))\
    .withColumn('pickup_hour', hour(col('pickup_datetime')))\
    .withColumn('pickup_day_of_week', dayofweek(col('pickup_datetime')))\
    .withColumn('average_speed_mph', when(col('trip_duration') > 0, (col('trip_distance') / (col('trip_duration') / 60))).otherwise(0))

# Save Processed Data
processed_data_path = "s3://your-bucket/nyc_taxi_data/processed/"
taxi_df.write.parquet(processed_data_path, mode='overwrite')
