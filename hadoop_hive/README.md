# Hadoop Hive 

### Skills and tools
`Yandex.Cloud` `S3` `HDFS` `HIVE` `MapReduce` `TEZ` `YARN` `HiveSQL` `CLI` `Shell` `Hadoop Cluster Administration` 

---

### Task: To provide constant access to cold data, create a 'Star` scheme, create a showcase of the form:

| Payment type | Date         | 	Tips average amount | Passengers total |
|:-------------|:-------------|:---------------------|:-----------------|
| Cash         | 	2020-01-31  | 	999.99              | 	112             |


### Input-data: taxi_data.csv:
1,2020-04-01 00:41:22,2020-04-01 01:01:53,1,1.20,1,N,41,24,2,5.5,0.5,0.5,0,0,0.3,6.8,0

Learn more about the data source [*here*][1]

---

### Progress of work:
1. *Deploying a Hadoop cluster* using a `Yandex.Cloud` solution :
2. *Creating a bucket* using a `S3` Yandex.Cloud solution.
3. [*Downloading data*][2] (database) to created `s3` bucket using `distcp`.
4. [*Creating & configure Database*][3] (database). Setting configuration `Hive - TEZ`. 
   * "payment" according to the description of the data format. The storage format is parquet. 
   * The names of the id and name fields. Filling dimension table.
   * Using access utility - `Hive CLI`.
   * Tables created as external (`external`) to prevent data loss.
5. [*Creating tables*][4] trips built on top of the existing data in the `csv` format.
trips are partitioned by the day of the start of the trip, the storage format is `parquet`.
Thus, the search for the necessary data in the table will take the shortest possible time.
6. [*Configure partitions, transformation and upload data*][5] to fact tables.
7. [*Creating data showcase*][6] using a materialized view and `MAPJOIN`.
8. [*Creating terminal scenario*][7] for showcase auto-creation.
9. [*Rebuilding*][8] showcase.



[1]:https://registry.opendata.aws/nyc-tlc-trip-records-pds/
[2]:https://github.com/Amboss/portfolio_projects/blob/master/hadoop_hive/data/dawnload_s3_data.sh
[3]:https://github.com/Amboss/portfolio_projects/blob/master/hadoop_hive/scrpts/table_dict.sql
[4]:https://github.com/Amboss/portfolio_projects/blob/master/hadoop_hive/scrpts/table_fact.sql
[5]:https://github.com/Amboss/Hadoop_hive/blob/master/scrpts/insert_to_table_fact.sql
[6]:https://github.com/Amboss/portfolio_projects/blob/master/hadoop_hive/scrpts/view.sql
[7]:https://github.com/Amboss/portfolio_projects/blob/master/hadoop_hive/scrpts/run.sh
[8]:https://github.com/Amboss/portfolio_projects/blob/master/hadoop_hive/scrpts/rebuild.sh
