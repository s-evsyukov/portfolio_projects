import os

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as f
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, IntegerType, DoubleType
from pyspark.sql.functions import round
from typing import List
from pathlib import Path


MYSQL_HOST = 'rc1b-**************.mdb.yandexcloud.net'
MYSQL_PORT = 3306
MYSQL_DATABASE = 'test_db'
MYSQL_TABLE = 'test_table'
MYSQL_USER = '********'
MYSQL_PASSWORD = '********'

dim_columns = ['id', 'name']

vendor_rows = [
    (1, 'Creative Mobile Technologies, LLC'),
    (2, 'VeriFone Inc'),
]

rates_rows = [
    (1, 'Standard rate'),
    (2, 'JFK'),
    (3, 'Newark'),
    (4, 'Nassau or Westchester'),
    (5, 'Negotiated fare'),
    (6, 'Group ride'),
]

payment_rows = [
    (1, 'Credit card'),
    (2, 'Cash'),
    (3, 'No charge'),
    (4, 'Dispute'),
    (5, 'Unknown'),
    (6, 'Voided trip')
]


trips_schema = StructType([
    StructField('VendorID', StringType(), True),
    StructField('tpep_pickup_datetime', TimestampType(), True),
    StructField('tpep_dropoff_datetime', TimestampType(), True),
    StructField('passenger_count', IntegerType(), True),
    StructField('trip_distance', DoubleType(), True),
    StructField('RatecodeID', IntegerType(), True),
    StructField('store_and_fwd_flag', StringType(), True),
    StructField('PULocationID', IntegerType(), True),
    StructField('DOLocationID', IntegerType(), True),
    StructField('payment_type', IntegerType(), True),
    StructField('fare_amount', DoubleType(), True),
    StructField('extra', DoubleType(), True),
    StructField('mta_tax', DoubleType(), True),
    StructField('tip_amount', DoubleType(), True),
    StructField('tolls_amount', DoubleType(), True),
    StructField('improvement_surcharge', DoubleType(), True),
    StructField('total_amount', DoubleType(), True),
    StructField('congestion_surcharge', DoubleType()),
])


def agg_calc(spark: SparkSession) -> DataFrame:
    """
    Initiating DataFrame

    :param spark: current spark session
    :return: DataFrame
    """
    data_path = os.path.join(Path(__name__).parent, "I:/taxi", 'yellow_tripdata_2020-01.csv')

    trip_fact = spark.read \
        .option("header", "true") \
        .schema(trips_schema) \
        .csv(data_path)

    datamart = trip_fact \
        .where(trip_fact['VendorID'].isNotNull()) \
        .groupBy(trip_fact['payment_type'],
                 f.to_date(trip_fact['tpep_pickup_datetime']).alias('dt'),
                 ) \
        .agg(round(f.avg(trip_fact['total_amount'] / trip_fact['trip_distance']), 2).alias('Avg_trip_km_cost'),
             round(f.avg(trip_fact['tip_amount']), 2).alias("avg_tips_cost")
             ) \
        .select(f.col('payment_type'),
                f.col('dt'),
                f.col('avg_tips_cost'),
                f.col('avg_trip_km_cost')) \
        .orderBy(f.col('dt').desc(), f.col('payment_type').asc())
    return datamart


def save_to_mysql(host: str, port: int, db_name: str, username: str,
                  password: str, df: DataFrame, table_name: str):
    props = {
        'user': f'{username}',
        'password': f'{password}',
        'driver': 'com.mysql.cj.jdbc.Driver',
        "ssl": "true",
        "sslmode": "none",
    }

    df.write.jdbc(
        url=f'jdbc:mysql://{host}:{port}/{db_name}', table=table_name, properties=props)


def main(spark: SparkSession):
    payment_dim = spark.createDataFrame(data=payment_rows, schema=dim_columns)

    datamart = agg_calc(spark).cache()
    datamart = datamart.filter(f.month('dt').isin(1))
    # datamart.show(truncate=False, n=10)

    joined_datamart = datamart \
        .join(other=payment_dim, on=payment_dim['id'] == f.col('payment_type'), how='inner') \
        .select(payment_dim['name'].alias('payment_name'),
                f.col('dt'),
                f.col('avg_tips_cost'),
                f.col('avg_trip_km_cost')
                )

    # joined_datamart.show(truncate=False, n=50)
    joined_datamart.write.mode('overwrite').csv('output')


if __name__ == '__main__':
    main(SparkSession
         .builder
         .config("spark.jars", "jars/mysql-connector-java-8.0.28.jar")
         .appName('My first spark job')
         .getOrCreate())
