import pandas as pd 
import sqlalchemy
import sys
from src.logger import logging
from src.exception import CustomException

def create_engine(server,database):
    connection_string = f'mssql+pymssql://localhost:1434/master'
    engine = sqlalchemy.create_engine(connection_string)
    return engine

def fetch_data(engine,table_name):
    query=f"select * from {table_name}"
    df=pd.read_sql(query,engine)
    return df


if __name__=="__main__":

    server = 'localhost'
    database = 'master'
    table_name = 'Insurance'

    engine=create_engine(server,database)

    try:
        df=fetch_data(engine,table_name)
        logging.info("Data fetched successfully!")
        print(df.head())
    except Exception as e:
        logging.info("Error fetching data.")
        raise CustomException(e,sys)
    finally:
        engine.dispose()