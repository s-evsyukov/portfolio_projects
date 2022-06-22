aws s3 cp s3://nyc-tlc/trip\ data/yellow_tripdata_2020-04.csv ./data/ --no-sign-request

mkdir ~/.mysql && \
wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" -O ~/.mysql/root.crt && \
chmod 0600 ~/.mysql/root.crt

wget -O ./jars/mysql-connector-java-8.0.25.jar \
https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.25/mysql-connector-java-8.0.25.jar
