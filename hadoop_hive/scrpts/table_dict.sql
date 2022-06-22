create database yellow_taxi;


set hive.execution.engine=tez;


CREATE EXTERNAL TABLE yellow_taxi.payment_type
(
    ID int,
    NAME string
)
STORED AS parquet;


WITH t AS (SELECT 1, 'Credit card'
UNION ALL
SELECT 2, 'Cash'
UNION ALL
SELECT 3, 'No charge'
UNION ALL
SELECT 4, 'Dispute'
UNION ALL
SELECT 5, 'Unknown'
UNION ALL
SELECT 6, 'Voided trip')
INSERT INTO yellow_taxi.payment_type 
SELECT * FROM t;