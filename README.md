commands for running project locally


### data file links
https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet

### Build image everytime you update script
```
docker build -t taxi_ingest:v001 .
```

### Create Docker network
```
docker network create pg-network
```

### Run Docker image for postgres db using network
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

### Run Docker image for pgAdmin using network
this is where the nyc yellow taxi data will be loaded
```
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin-2 \
  dpage/pgadmin4
```

### Run the script with Docker 

```
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```

### Use Docker compose file to build and run above containers
use the following command to build
```
docker-compose up
```

## to ingest the data and load it into the db 
to change docker_sql_default with the name of your local dev folder followed by _default for example local_dev_default
```
URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet"

docker run --rm -it \
  --network=pgnetwork \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```

then to turn off and delete the containers and the network
```
docker-compose down
```