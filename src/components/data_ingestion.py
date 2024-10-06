import sys
print(sys.path)
import pandas as pd 
import sqlalchemy
from src.exception import CustomException
from src.logger import logging 
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
import os

from src.components.data_transformation import DataTransformation


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

@dataclass
class dataingestionconfig:
    train_data_path=os.path.join('artifacts','train.csv')
    test_data_path=os.path.join('artifacts','test.csv')
    raw_data_path=os.path.join('artifacts','raw.csv')

class dataingestion:
    def __init__(self):
        self.ingestion_config=dataingestionconfig()

    def initiate_data_ingestion(self):
        logging.info('We have entered into the data ingeston method')

        try:
            engine=create_engine(server,database)
            logging.info('engine has created successfully')
            df=fetch_data(engine,table_name)
            logging.info('Read the data successfully from the database')
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            logging.info('Train test split initiated')
            train_set,test_set=train_test_split(df,test_size=0.1,random_state=42)
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            logging.info('train and test file saved')

            return (self.ingestion_config.train_data_path,self.ingestion_config.test_data_path)

        except Exception as e:
            raise CustomException(e,sys)

if __name__=='__main__':
    obj=dataingestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    data_transformation.initiate_data_transformation(train_data,test_data)