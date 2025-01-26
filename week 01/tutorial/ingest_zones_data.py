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

    # Download the csv file
    csv_name = 'output.csv'

    os.system(f"wget {url} -O {csv_name}")

    # Connect to the postgres database
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    with engine.connect() as connection:

        # Load data from CSV file
        df = pd.read_csv(csv_name)
       
        # creating the empty table first without data
        df.head(n=0).to_sql(name=table_name, con=connection, if_exists='replace')

        # inserting the data into the table
        df.to_sql(name=table_name, con=connection, if_exists='append')

        print("Finished ingesting data into the postgres database")


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


