from pyspark.sql import SparkSession

import os

from pyspark.sql import functions as f
from pyspark.sql.dataframe import DataFrame
from pyspark.sql.functions import collect_set, to_json, struct
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, IntegerType, DoubleType

from practice4.main import create_dict, dim_columns, vendor_rows, trips_schema, payment_rows


def foreach_batch_function(df: DataFrame, epoch_id):
    df.write.mode("append").json("output_report")


def main(spark: SparkSession):
    jsonOptions = {"timestampFormat": "yyyy-MM-dd'T'HH:mm:ss.sss'Z'"}

    fields = list(map(lambda x: f"json_message.{x.name}", trips_schema.fields))

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:29092") \
        .option("subscribe", "taxi") \
        .option("startingOffsets", "latest") \
        .load() \
        .select(f.from_json(f.col("value").cast("string"), trips_schema, jsonOptions).alias("json_message")) \
        .select(fields)

    # .option("maxOffsetsPerTrigger", 1000) \

    # пишем на диск
    # writer = df \
    #     .writeStream \
    #     .foreachBatch(foreach_batch_function) \
    #     .trigger(processingTime='10 seconds') \
    #     .option("path", "output_report") \
    #     .outputMode("append") \
    #     .start()

    # считаем витрину
    mart = df.groupBy('payment_type', f.to_date('tpep_pickup_datetime').alias('dt')).agg(
        f.count(f.col('*')).alias('cnt')) \
        .join(
        other=create_dict(spark, dim_columns, payment_rows),
        on=f.col('payment_type') == f.col('id'),
        how='inner') \
        .select(f.col('name'), f.col('cnt'), f.col('dt')) \
        .orderBy(f.col('name'), f.col('dt')) \
        .select(to_json(struct("name", "cnt", "dt")).alias('value'))

    # writer = mart \
    #     .writeStream \
    #     .trigger(processingTime='10 seconds') \
    #     .format("console") \
    #     .outputMode("complete") \
    #     .option("truncate", "false") \
    #     .start()
    #

    writer = mart \
        .writeStream \
        .trigger(processingTime='10 seconds') \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:29092") \
        .option("topic", "report") \
        .option("checkpointLocation", "streaming-job-checkpoint") \
        .outputMode("complete") \
        .start()



    writer.awaitTermination()


if __name__ == '__main__':
    main(SparkSession.
         builder
         .appName("streaming_job")
         .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.2.0")
         .getOrCreate())
