import argparse
from pyspark.ml import PipelineModel
from pyspark.sql import SparkSession


MODEL_PATH = '/data/spark_ml_model'


def process(data_path, model_path, result_path):
    """
    Application of the saved model.

    :param data_path: path to the file with the data to which the prediction should be made.
    ::param model_path: path to the saved model (From the task PySparkMLFit.py ).
    :param result_path: the path to save the prediction results ([session_id, prediction]).date
    """
    spark = _spark_session()
    df = spark.read.parquet(data_path)
    loaded_model = PipelineModel.load(model_path)
    prediction = loaded_model.transform(df)
    prediction.select('session_id', 'prediction').write.mode("overwrite").parquet(result_path)
    spark.stop()
    print("Done.")


def main(data, result):
    spark = _spark_session()
    process(spark, data, result)


def _spark_session() -> SparkSession:
    """
    Creating SparkSession.

    :return: SparkSession
    """
    return SparkSession.builder.appName('Predict').getOrCreate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data', type=str, default='data.parquet', help='Please set datasets path.')
    parser.add_argument(
        '--result', type=str, default='result', help='Please set result path.')
    args = parser.parse_args()
    data = args.data
    result = args.result
    main(data, result)
