import operator
import argparse

from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.sql import SparkSession
from pyspark.ml.classification import DecisionTreeClassifier
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.classification import GBTClassifier


"""
The main process of the task. A template for the process of training your model,
the task is to create a training plan for the model taking into account the optimization of hyper-parameters,
determine the best model and save it for future use
"""

MODEL_PATH = 'spark_ml_model'
LABEL_COL = 'is_bot'
TRAIN_DATA = "/data/session-stat.parquet"
FEATURES = ["duration", "item_info_events", "select_item_events",
            "make_order_events", "events_per_min", "platform_index", "user_type_index"]
FEATURES_COL = "features"
PREDICT_COL = "prediction"


def build_models() -> dict:
    """
    Initiating dict with experiments config

    :return: dict
    """
    cl_lst = {'dtc': DecisionTreeClassifier(), 'rfc': RandomForestClassifier(), 'gbc': GBTClassifier()}
    models = dict()
    for key, value in cl_lst:
        value.setLabelCol(labelCol=LABEL_COL)
        models.update({
            key: {
                'model': value,
                'params': ParamGridBuilder()
                    .addGrid(value.maxDepth, [2, 5, 10])
                    .addGrid(value.maxBins, [10, 20, 40]).build(),
                'best': None,
                'score': None}
        })
    return models


def build_pipeline(model_key, model_conf) -> Pipeline:
    """
    Creating pipline for model.

    :param model_key: the key of model type.
    :param model_conf: experiment model config.
    :return: Pipeline
    """
    user_type_indexer = StringIndexer(
        inputCol='user_type', outputCol="user_type_index")
    platform_indexer = StringIndexer(
        inputCol='platform', outputCol="platform_index")
    features = VectorAssembler(
        inputCols=FEATURES, outputCol='features')
    return Pipeline(
        stages=[user_type_indexer, platform_indexer, features, model_conf[model_key]['model']])


def train_pipeline(model_key, model_conf, evaluator, df_train, df_test):
    """
    Pipeline model training using CrossValidator. All results are saved in the configuration.

    :param model_key: model type key.
    :param model_conf: configuration of experiment models.
    :param evaluator: evaluator of model quality.
    :param df_train: dataset for training the model.
    :param df_test: dataset for evaluating the model.
    """
    cv = CrossValidator(estimator=build_pipeline(model_key, model_conf),
                        estimatorParamMaps=model_conf[model_key]['params'],
                        evaluator=evaluator, numFolds=2, parallelism=3)
    fitted_models = cv.fit(df_train)
    best_model = fitted_models.bestModel
    score = evaluator.evaluate(best_model.transform(df_test))
    model_conf[model_key]['best'] = best_model
    model_conf[model_key]['score'] = score


def get_best_model(model_conf):
    """
    Choosing the best model according to the evaluation.

    :param model_conf: configuration of experiment models.
    :return: key of the best model from the configuration.
    """
    md = {k: v['score'] for k, v in model_conf.items()}
    return max(md.items(), key=operator.itemgetter(1))[0]


def log_results(model_key, model_conf):
    """
    Logging of metrics and hyper-parameters of the model.

    :param model_key: model type key.
    :param model_conf: configuration of experiment models.
    """
    j_obj = model_conf[model_key]['best'].stages[-1]._java_obj
    print(f'\nModel type = {model_key}')
    print(f"F1 = {model_conf[model_key]['score']}")
    print(f'maxDepth = {j_obj.getMaxDepth()}')
    print(f'maxBins = {j_obj.getMaxBins()}')


def process(spark, d_path, m_path):
    """
    Train model with DecisionTreeClassifier, saving pipeline as 'spark_ml_model'

    :param spark: initiated Spark session
    :param d_path: path to file with db
    :param m_path: path for model
    """
    model_conf = build_models()
    evaluator = MulticlassClassificationEvaluator(
        labelCol="is_bot", predictionCol="prediction", metricName="f1")

    # Initiating Spark session & train models
    df = spark.read.parquet(data_path)
    df_bots_train, df_bots_test = df.filter(df.is_bot == 1).randomSplit([0.8, 0.2], 42)
    df_users_train, df_users_test = df.filter(df.is_bot == 0).randomSplit([0.8, 0.2], 42)
    df_train = df_users_train.union(df_bots_train)
    df_test = df_users_test.union(df_bots_test)

    for key in model_conf.keys():
        train_pipeline(key, model_conf, evaluator, df_train, df_test)
        log_results(key, model_conf)

    key = get_best_model(model_conf)
    print(f"Best model type = {key} with score = {model_conf[key]['score']}")
    best_model = model_conf[key]['best']
    best_model.write().overwrite().save(model_path)
    print('Best model saved')


def main(d_path, m_path):
    spark = SparkSession.builder.appName('PySparkMLFitJob').getOrCreate()
    process(spark, d_path, m_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--data_path', type=str, default=TRAIN_DATA, help='Please set data path.')
    parser.add_argument(
        '--model_path', type=str, default=MODEL_PATH, help='Please set model path.')
    args = parser.parse_args()
    data_path = args.data_path
    model_path = args.model_path
    main(data_path, model_path)
