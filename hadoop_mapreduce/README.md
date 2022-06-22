# Hadoop_map_reduce
map reduce practice

#### Задача: Написать map-reduce приложение, использующее данные Нью-Йоркского такси и вычисляющее среднее значение "чаевых" за каждый месяц 2020 года:

| Payment type | Date |	Tips average amount | Passengers total |
| :------------| :--- | :------------------ | :--------------- |
|Cash|	2020-01-31|	999.99|	112|

#### Input-data: file.csv:
---
1,2020-04-01 00:41:22,2020-04-01 01:01:53,1,1.20,1,N,41,24,2,5.5,0.5,0.5,0,0,0.3,6.8,0

Подробнее о источнике данных [*здесь*][6]
---

### Ход работы:
1. *Разворачивание кластера Hadoop* с использованием облачного решения Yandex.Cloud:
2. *Создание бакета* на `s3`.
3. [*Копирование данных*][3] (базы данных) на созданный бакет `s3` с помощью утилиты distcp.
4. [*Разработка mapper*][2].
5. [*Разработка reducer*][3]. 
6. [*Разработка shell-скрипта*][4] для запуска MapReduce задания. Настроен размер контейнера для операций `map` (т.к. стандартный размер составляет 3072Mb, а обрабатываемые файлы меньше 1024Mb, значение изменено на 1024Mb), что значительно ускоряет стадию `map`.
7. [*Доставка кода*][5] на удаленный сервер `make copy`.
8. *Запуск приложения*.

[1]:https://github.com/Amboss/Hadoop_map_reduce/blob/master/data/dawnload_s3_data.sh
[2]:https://github.com/Amboss/Hadoop_map_reduce/blob/master/script/mapper.py
[3]:https://github.com/Amboss/Hadoop_map_reduce/blob/master/script/reducer.py
[4]:https://github.com/Amboss/Hadoop_map_reduce/blob/master/script/run.sh
[5]:https://github.com/Amboss/Hadoop_map_reduce/blob/master/script/make_file
[6]:https://registry.opendata.aws/nyc-tlc-trip-records-pds/
