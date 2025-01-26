import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os
import gzip
import shutil

def create_db_engine(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    return create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

def load_taxi_data(params, url, table_name):
    gz_name = 'taxi_data.csv.gz'
    csv_name = 'taxi_data.csv'
    
     # Download the gzipped file
    os.system(f"wget {url} -O {gz_name}")
    
    # Decompress the gzipped file
    with gzip.open(gz_name, 'rb') as f_in:
        with open(csv_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    
    # Load data from CSV file
    df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
    df = next(df_iter)
    
    df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
    df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
    
    with params.engine.connect() as connection:
        # creating the empty table first without data
        df.head(n=0).to_sql(name=table_name, con=connection, if_exists='replace')
        
        while True:
            try:
                t_start = time()

                # inserting the data into the table
                df.to_sql(name=table_name, con=connection, if_exists='append')
                
                df = next(df_iter)
                df.lpep_pickup_datetime = pd.to_datetime(df.lpep_pickup_datetime)
                df.lpep_dropoff_datetime = pd.to_datetime(df.lpep_dropoff_datetime)
                
                t_end = time()
                print('Inserted taxi chunk, took %.3f seconds' % (t_end - t_start))
            except StopIteration:
                print("Finished ingesting taxi data")
                break

def load_zones_data(params, url, table_name):
    csv_name = 'zones.csv'

    # Download the file
    os.system(f"wget {url} -O {csv_name}")
    
    df = pd.read_csv(csv_name)

    with params.engine.connect() as connection: 
        # creating the empty table first without data
        df.head(n=0).to_sql(name=table_name, con=connection, if_exists='replace')

        # inserting the first set of data into the table 
        df.to_sql(name=table_name, con=connection, if_exists='replace')

        print("Finished ingesting zones data")

def main(params):
    params.engine = create_db_engine(params)
    load_zones_data(params, params.zones_url, params.zones_table)
    load_taxi_data(params, params.taxi_url, params.taxi_table)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest both taxi and zones data to Postgres')
    
    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--taxi_table', help='name for taxi data table')
    parser.add_argument('--zones_table', help='name for zones table')
    parser.add_argument('--taxi_url', help='url for taxi data')
    parser.add_argument('--zones_url', help='url for zones data')
    
    args = parser.parse_args()
    main(args)



