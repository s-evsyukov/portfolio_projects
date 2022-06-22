"""
    Tasks:
    1) Scheduler: Work from monday to saturday, but not on sunday
    2) Delete tmp files
    3) Export data from URL to XML file
    4) Convert XML file to CSV file
    5) Initiating table in greenplum
    6) Insert data from CSV file to Greenplum DB (Prevent duplication by same date)
    7) Select heading from GP DB articles where id equals current weekday
    8) Save results to XCom
    9) Print results to XCom
"""

import os
import csv
import logging
import os.path
import xml.etree.ElementTree as ET

from airflow import DAG
from datetime import datetime
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.hooks.postgres_hook import PostgresHook
from airflow.operators.python_operator import PythonOperator

DEFAULT_ARGS = {
    'start_date': days_ago(2),
    'owner': 's-evsjukov',
    'poke_interval': 300,
}

with DAG(
        dag_id="s-evsjukov-pet",
        schedule_interval='0 0 * * 1-6',
        default_args=DEFAULT_ARGS,
        max_active_runs=1,
        tags=['s-evsjukov']
) as dag:

    # tmp files
    xml_file_name = '/tmp/test_cbr.xml'
    csv_file_name = '/tmp/test_cbr.csv'

    # DB names
    students_db = 'students.public.s_evsjukov_cbr'
    karpovcourses_db = 'karpovcourses.public.articles'

    # URL to download data
    currant_date = '{{ macros.ds_format(ds, "%Y-%m-%d", "%d/%m/%Y") }}'
    url = 'https://www.cbr.ru/scripts/XML_daily.asp/?date_req=' + currant_date


    def delete_files():
        """
        2) Delete tmp XML & CSV files if existing
        """
        if os.path.isfile(xml_file_name):
            os.remove(xml_file_name)
        if os.path.isfile(csv_file_name):
            os.remove(csv_file_name)


    delete_tmp_files = PythonOperator(
        task_id='delete_tmp_files',
        python_callable=delete_files,
        dag=dag
    )

    """
    3) Export data from URL to XML file
    """
    export_cbr_xml = BashOperator(
        task_id='export_cbr_xml',
        bash_command="curl {} | iconv -f Windows-1251 -t UTF-8 > {}".format(url, xml_file_name),
        dag=dag
    )


    def convert_xml_to_csv_func():
        """
        4) Convert XML file to CSV file
        """
        xml_parser = ET.XMLParser(encoding="UTF-8")
        xml_tree = ET.parse(xml_file_name, parser=xml_parser)
        xml_root = xml_tree.getroot()

        with open(csv_file_name, 'w') as csv_file:
            writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for valute in xml_root.findall('Valute'):
                num_code = valute.find('NumCode').text
                char_code = valute.find('CharCode').text
                nominal = valute.find('Nominal').text
                name = valute.find('Name').text
                value = valute.find('Value').text
                writer.writerow(
                    [xml_root.attrib['Date']] + [valute.attrib['ID']] +
                    [num_code] + [char_code] + [nominal] + [name] +
                    [value.replace(',', '.')]
                )
                logging.info(
                    [xml_root.attrib['Date']] + [valute.attrib['ID']] +
                    [num_code] + [char_code] + [nominal] + [name] +
                    [value.replace(',', '.')]
                )


    convert_xml_to_csv = PythonOperator(
        task_id='convert_xml_to_csv',
        python_callable=convert_xml_to_csv_func,
        dag=dag
    )


    def initiate_gp_func(**kwargs):
        """
        5) Initiating table in greenplum
        """
        pg_hook = PostgresHook(postgres_conn_id='conn_greenplum_write')
        conn = pg_hook.get_conn()
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS {} (
            dt text,
            id text,
            num_code text,
            char_code text,
            nominal text,
            nm text,
            value text)""".format(students_db))
        conn.close()


    initiate_gp = PythonOperator(
        task_id='initiate_gp',
        python_callable=initiate_gp_func,
        dag=dag
    )


    def insert_csv_to_gp_func(**kwargs):
        """
        6) Insert data from CSV file to greenplum DB, preventing copy with same date
        """
        args = kwargs['templates_dict']['implicit']
        pg_hook = PostgresHook(postgres_conn_id='conn_greenplum_write')
        conn = pg_hook.get_conn()
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("DELETE FROM {} WHERE dt='{}'".format(students_db, args))
        conn.close()
        pg_hook.copy_expert("COPY " + students_db + " FROM STDIN DELIMITER ','", csv_file_name)


    insert_csv_to_gp = PythonOperator(
        task_id='load_csv_to_gp',
        python_callable=insert_csv_to_gp_func,
        templates_dict={'implicit': '{{ ti.xcom_pull(task_ids="convert_xml_to_csv") }}'},
        provide_context=True,
        dag=dag
    )

    def select_from_gp_func(**kwargs):
        """
        7) Select heading from GP DB articles where id equals current weekday
        """
        week_day = datetime.today().weekday() + 1
        pg_hook = PostgresHook(postgres_conn_id='conn_greenplum')
        conn = pg_hook.get_conn()
        cursor = conn.cursor()
        cursor.execute("SELECT heading FROM {} WHERE id='{}'".format(karpovcourses_db, week_day))
        query_res = cursor.fetchall()
        # one_string = cursor.fetchone()[0]
        logging.info(query_res)

        """
        8) Save results to XCom
        """
        if query_res:
            kwargs['ti'].xcom_push(value=query_res, key='heading')
        else:
            kwargs['ti'].xcom_push(value="No data for for day " + str(week_day), key='heading')
        conn.close()


    select_from_gp = PythonOperator(
        task_id='select_from_gp',
        python_callable=select_from_gp_func,
        dag=dag
    )


    def print_result_func(**kwargs):
        """
        9) Print results to XCom
        """
        logging.info("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
        logging.info(kwargs['ti'].xcom_pull(task_ids='select_from_gp', key='heading'))
        logging.info("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")


    print_result = PythonOperator(
        task_id='print_result',
        python_callable=print_result_func,
        dag=dag
    )

    """
    Airflow task order
    """
    delete_tmp_files >> export_cbr_xml >> convert_xml_to_csv >> initiate_gp >> insert_csv_to_gp
    select_from_gp >> print_result
