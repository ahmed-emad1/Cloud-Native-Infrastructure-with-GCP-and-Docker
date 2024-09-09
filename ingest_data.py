import os
import sys
from time import time
import pandas as pd
import argparse
import pyarrow.parquet as pq
from sqlalchemy import create_engine


def main():

    user = os.getenv('USER')
    password = os.getenv('PASSWORD')
    host = os.getenv('HOST')
    port = os.getenv('PORT')
    db = os.getenv('DB')
    table_name = os.getenv('TABLE_NAME')
    url = os.getenv('URL')
    file_name = url.rsplit('/',1)[-1]

    os.system(f"wget {url} -O {file_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    if '.csv' in file_name:
        df = pd.read_csv(file_name,nrows= 10)
        # convert to datetime as .csv does not save data types
        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
        df_iter = pd.read_csv(file_name, iterator=True, chunksize = 100000)
    elif '.parquet' in file_name:
        file = pq.ParquetFile(file_name)
        df = next(file.iter_batches(batch_size=10)).to_pandas()
        df_iter = file.iter_batches(batch_size=100000)
    else:
        print('Error. Only .csv or .parquet files supported at this time.')
        sys.exit()

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    t_start = time()
    count = 0
    for batch in df_iter:
        count+=1
        if '.parquet' in file_name:
            batch_df = batch.to_pandas()
        else:
            batch_df = batch
             # Convert datetime columns
            batch_df['tpep_pickup_datetime'] = pd.to_datetime(batch_df['tpep_pickup_datetime'])
            batch_df['tpep_dropoff_datetime'] = pd.to_datetime(batch_df['tpep_dropoff_datetime'])

        t_start = time()

        # Append to SQL table
        batch_df.to_sql(name=table_name, con=engine, if_exists='append', index=False)

        t_end = time()
        print(f'Time for appending chunk: {t_end - t_start:.3f} seconds')
    
    t_end = time()   
    print(f'Completed! Total time taken was {t_end-t_start:10.3f} seconds for {count} batches.')    





if __name__ == '__main__':
    main()