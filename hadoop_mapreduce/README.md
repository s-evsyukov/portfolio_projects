# Hadoop_map_reduce
map reduce practice

#### Задача: Написать map-reduce приложение, использующее данные Нью-Йоркского такси и вычисляющее среднее значение "чаевых" за каждый месяц 2020 года:

| Payment type | Date |	Tips average amount | Passengers total |
| :------------| :--- | :------------------ | :--------------- |
|Cash|	2020-01-31|	999.99|	112|

### Input-data: taxidata.csv:
1,2020-04-01 00:41:22,2020-04-01 01:01:53,1,1.20,1,N,41,24,2,5.5,0.5,0.5,0,0,0.3,6.8,0
Подробнее о источнике данных [*здесь*][1]

---

### Ход работы:
1. *Разворачивание кластера Hadoop* с использованием облачного решения Yandex.Cloud:
2. *Создание бакета* на `s3`.
3. [*Копирование данных*][2] (базы данных) на созданный бакет `s3` с помощью утилиты distcp.
4. [*Разработка mapper*][3].
5. [*Разработка reducer*][4]. 
6. [*Разработка shell-скрипта*][5] для запуска MapReduce задания. Настроен размер контейнера для операций `map` (т.к. стандартный размер составляет 3072Mb, а обрабатываемые файлы меньше 1024Mb, значение изменено на 1024Mb), что значительно ускоряет стадию `map`.
7. [*Доставка кода*][6] на удаленный сервер `make copy`.
8. *Запуск приложения*.

[1]:https://registry.opendata.aws/nyc-tlc-trip-records-pds/
[2]:https://github.com/Amboss/portfolio_projects/blob/master/hadoop_mapreduce/data/dawnload_s3_data.sh
[3]:https://github.com/Amboss/portfolio_projects/blob/master/hadoop_mapreduce/script/mapper.py
[4]:https://github.com/Amboss/portfolio_projects/blob/master/hadoop_mapreduce/script/reducer.py
[5]:https://github.com/Amboss/portfolio_projects/blob/master/hadoop_mapreduce/script/run.sh
[6]:https://github.com/Amboss/portfolio_projects/blob/master/hadoop_mapreduce/script/Makefile
