# Commands for Running the Project Locally

## Data File Links
- [January 2021 CSV Data](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz)
- [January 2024 Parquet Data](https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet)

## Build Docker Image After Updating the Script
Build the Docker image every time the script is updated:
```docker build -t taxi_ingest:v001 .```

### Create Docker network
Create a network for Docker containers:
```
docker network create pg-network
```

### Run Postgres Docker Container Using the Network
This container will host the NYC yellow taxi data:
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

### Run pgAdmin Docker Container Using the Network
pgAdmin will be used to manage the database:
```
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin-2 \
  dpage/pgadmin4
```

### Run the Ingestion Script with Docker
Run the script to ingest NYC taxi data into the database:
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

### Use Docker Compose to Build and Run Containers
Use Docker Compose to set up and run the containers using `docker-compose-without-ingestion-script.yaml`:
```
docker compose up
```

### Ingest Data and Load it into the Database
To ingest data into the database, adjust the network name as needed (replace `docker_sql_default` with `local_dev_default` or the appropriate name):
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

### Tear Down Containers and Network
To stop and remove all containers and networks except the container that ran the script as it wasn't made using docker compose:
```
docker compose down
```

### Run the Entire Project and Ingestion Script
You can add the script build and run steps to the Docker Compose file. To run everything at once use `docker-compose.yaml`:
```
docker compose build
docker compose up
```

To run in detached mode (without logs):
```
docker compose up -d
```

## Check Data in pgAdmin and Tear Down
After confirming the data has been ingested using pgAdmin, you can stop the containers and remove them:
```
docker compose down
```