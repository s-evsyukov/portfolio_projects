#!/bin/bash
## creating view

hive -v -f table_dict.sql;
hive -v -f table_fact.sql;
hive -v -f insert_to_table_fact.sql;
hive -v -f view.sql;
hive -e "exit;"
