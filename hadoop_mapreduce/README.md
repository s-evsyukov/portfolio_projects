# Hadoop_map_reduce


### Task: To write a mapreduce application using New York taxi data and calculating the average value of "tips" for each month of 2020:

| Payment type | Date |	Tips average amount | Passengers total |
| :------------| :--- | :------------------ | :--------------- |
|Cash|	2020-01-31|	999.99|	112|

### Input-data: taxi_data.csv:
1,2020-04-01 00:41:22,2020-04-01 01:01:53,1,1.20,1,N,41,24,2,5.5,0.5,0.5,0,0,0.3,6.8,0

Learn more about the data source [*here*][1]

### Progress of work:
1. *Deploying a Hadoop cluster* using a `Yandex.Cloud` solution :
2. *Creating a bucket* using a `S3` Yandex.Cloud solution.
3. [*Downloading data*][2] (database) to created `s3` bucket using `distcp`.
4. [*Creating mapper*][3].
5. [*Creating reducer*][4]. 
6. [*Creating shell-script*][5] to initiate MapReduce task. Container configured for `map` operation with size 1024 MB, because standard size is 3072 Mb and current file size is less than 1024 MB
8. [*Uploading script*][6] to remote server `make copy`.
9. *Initiating application*.

[1]:https://registry.opendata.aws/nyc-tlc-trip-records-pds/
[2]:https://github.com/Amboss/portfolio_projects/blob/master/hadoop_mapreduce/data/dawnload_s3_data.sh
[3]:https://github.com/Amboss/portfolio_projects/blob/master/hadoop_mapreduce/script/mapper.py
[4]:https://github.com/Amboss/portfolio_projects/blob/master/hadoop_mapreduce/script/reducer.py
[5]:https://github.com/Amboss/portfolio_projects/blob/master/hadoop_mapreduce/script/run.sh
[6]:https://github.com/Amboss/portfolio_projects/blob/master/hadoop_mapreduce/script/Makefile
