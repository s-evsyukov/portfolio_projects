# Apache Spark ML

### Skills and tools
`PySpark` `SparkML` `SparkSession` `Pipeline` `mlflow`                                               


### Task: Create a bot identifier among user sessions with two tasks - to train the best data model and to apply it.

### Datasets: 
    session-stat.parquet
    test.parquet

---
### The structure of the Datasets:

| Field               | Discription                                              |
|:--------------------|:---------------------------------------------------------|
| session_id          | unique user session ID                                   |
| user_type           | user type [authorized/guest]                             |
| duration            | session duration time (in seconds)                       |
| platform            | user platform [web/ios/android]                          |
| item_info_events    | number of product information viewing events per session |
| select_item_events  | number of product selection events per session           |
| make_order_events   | number of product order processing events per session    |
| events_per_min      | number of events per minute on average per session       |
| is_bot              | bot attribute [0 - user, 1 - bot]                        |

### Progress of work:
1. [*Creating PySparkMLFit.py*][1] for the model training and searching for best prediction configuration.
2. [*Creating PySparkMLPredict.py*][2] for the prediction.  
3. *Initiating PySparkMLFit.py:*
    * `PySparkMLFit.py --data_path=session-stat.parquet --model_path=spark_ml_model`
4. *Initiating PySparkMLPredict.py*. 
    * `PySparkMLPredict.py --data_path=test.parquet --model_path=spark_ml_model --result_path=result`
   
[1]:https://github.com/Amboss/portfolio_projects/blob/master/apache_pyspark_ml/scripts/PySparkFit.py
[2]:https://github.com/Amboss/portfolio_projects/blob/master/apache_pyspark_ml/scripts/PySparkPredict.py

