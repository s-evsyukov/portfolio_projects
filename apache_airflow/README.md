# Apache Airflow

### Skills and tools
`VK.Cloud` `Airflow` `GreenPlum` `Jinja` `macros` `ETL` `parsing` `bash` `IDE` `CI/CD`

---
### Task: Create a DAG, with next features: 

1. Work from Monday to Saturday, but not on Sundays (can be implemented using schedules or branching operators)
2. Can connect with GreenPlum (use the connection 'conn_greenplum'. Solution option — PythonOperator with PostgresHook inside)
3. Upload from the articles' table the value of the heading field from the row with the id equal to the day of the week execution_date (Monday=1, Tuesday=2, ...)
4. Save the resulting value to XCom
5. The result of the work will be visible in the interface with XCom.
---

### Progress of work:

1. *Initiating GreenPlum cluster* in VK.Cloud
2. *Creating* [*export-dag.py*][1] performing the following steps:
    * Scheduler: Work from monday to saturday, but not on sunday
    * Delete tmp files
    * Export data from URL to XML file
    * Convert XML file to CSV file
    * Initiating table in greenplum
    * Insert data from CSV file to Greenplum DB (Prevent duplication by same date)
    * Select heading from GP DB articles where id equals current weekday
    * Save results to XCom
    * Print results to XCom
3. *Pushing DAG* through GitLab
4. *Initiating DAG* in Airflow


[1]:https://github.com/Amboss/portfolio_projects/blob/master/apache_airflow/scripts/export-dag.py
