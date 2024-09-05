import os
from time import time
import pandas as pd
import argparse
from sqlalchemy import create_engine


def main(params):

    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url
    csv_name = 'yellow_taxi.csv.gz'

    os.system(f"wget {url} -O {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    df_iter = pd.read_csv(csv_name, iterator=True, chunksize = 100000)

    df = next(df_iter)


    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    df.to_sql(name=table_name, con=engine, if_exists='append')

    while True:
        try:
            df = next(df_iter)
        except StopIteration:
            print("All chunks processed.")
            break

        t_start = time()
        
        # Convert datetime columns
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

        # Append to SQL table
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

        t_end = time()
        print(f'Time for appending chunk: {t_end - t_start:.3f} seconds')





if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ingest CSV data')
 
    parser.add_argument('--user',help='username for postgres')
    parser.add_argument('--password',help='password for postgres')
    parser.add_argument('--host',help='host name for postgres')
    parser.add_argument('--port',help='port name for postgres')
    parser.add_argument('--db',help='db name for postgres')
    parser.add_argument('--table_name',help='name of table where data will be written')
    parser.add_argument('--url',help='url for data file')

    args = parser.parse_args()

    main(args)