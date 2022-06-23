import argparse
import os
from pyspark.sql import SparkSession
import mlflow


LOGGED_MODEL = 'runs:/*****'

# os.environ['MLFLOW_S3_ENDPOINT_URL'] = 'https://storage.yandexcloud.net'
# os.environ['AWS_ACCESS_KEY_ID'] = '*****'
# os.environ['AWS_SECRET_ACCESS_KEY'] = '******'


def process(spark, data_path, result):
    """
    Основной процесс задачи.

    :param spark: SparkSession
    :param data_path: путь до датасета
    :param result: путь сохранения результата
    """
    mlflow.set_tracking_uri("https://mlflow.lab.karpov.courses")
    model = mlflow.spark.load_model(LOGGED_MODEL)

    # read parquet
    df = spark.read.parquet(data_path)

    # transform
    prediction = model.transform(df)

    # saving result
    prediction.write.save(result)


def main(data, result):
    spark = _spark_session()
    process(spark, data, result)


def _spark_session() -> SparkSession:
    """
    Создание SparkSession.

    :return: SparkSession
    """
    return SparkSession.builder.appName('test_1').getOrCreate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='data.parquet', help='Please set datasets path.')
    parser.add_argument('--result', type=str, default='result', help='Please set result path.')
    args = parser.parse_args()
    data = args.data
    result = args.result
    main(data, result)
