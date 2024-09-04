commands for running project locally


### data file links
https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet


### Run Docker image for postgres db
this is where the nyc yellow taxi data will be loaded
```
docker run -it \
-e POSTGRES_USER="root" \
-e POSTGRES_PASSWORD="root" \
-e POSTGRES_DB="ny_taxi" \
-v /$(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
-p 5432:5432 \
--network=pg-network \
--name pg-database \
postgres:13   
```

