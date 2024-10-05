import pandas as pd 
import sqlalchemy
import sys


def create_engine(server,database):
    connection_string = f'mssql+pymssql://{server}:1434/{database}'
    engine_ = sqlalchemy.create_engine(connection_string)
    return engine_

def fetch_data(engine,table_name):
    query=f"select * from {table_name}"
    df=pd.read_sql(query,engine)
    return df


server = 'localhost'
database = 'master'
table_name = 'Insurance'

def get_engine():
    return create_engine(server,database)
print(get_engine())

