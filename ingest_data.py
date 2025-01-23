import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os
import gzip
import shutil


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url

    # Download the gzipped file
    gz_name = 'output.csv.gz'
    csv_name = 'output.csv'

    # os.system(f"wget {url} -O {csv_name}")
    os.system(f"wget {url} -O {gz_name}")

    # Decompress the gzipped file
    with gzip.open(gz_name, 'rb') as f_in:
        with open(csv_name, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Connect to the postgres database
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    with engine.connect() as connection:

        # Load data from CSV file
        df_iter = pd.read_csv(csv_name, iterator=True, chunksize=100000)
        df = next(df_iter)

        df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
        df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])

        # creating the empty table first without data
        df.head(n=0).to_sql(name=table_name, con=connection, if_exists='replace')

        # inserting the first set of data into the table
        df.to_sql(name=table_name, con=connection, if_exists='append')

        # inserting the rest of the data into the table
        while True:
            try:
                t_start = time()
                df = next(df_iter)

                df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
                df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

                df.to_sql(name=table_name, con=connection, if_exists='append')
                t_end = time()

                print('inserted another chunk, took %.3f second' % (t_end - t_start))
            except StopIteration:
                print("Finished ingesting data into the postgres database")
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='username for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the csv file')


    args = parser.parse_args()

    main(args)
