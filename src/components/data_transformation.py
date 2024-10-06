import numpy as np 
import pandas as pd 
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline 
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer

from src.exception import CustomException
from src.logger import logging
from src.utils import save_obj
from dataclasses import dataclass
import os
import sys


@dataclass
class Datatransformerconfig:
    preprocessor_obj_file_path=os.path.abspath(os.path.join('artifacts', 'preprocessor.pkl'))

class DataTransformation:
    def __init__(self):
        self.data_trans_config=Datatransformerconfig()
    
    def data_transformation_get_obj(self):
        try:
            num_columns=['age','bmi','children']
            cat_columns=['sex','smoker','region']

            num_pipeline=Pipeline(
                steps=[
                    ('SimpleImputer',SimpleImputer(strategy='median')),
                    ('StandardScaler',StandardScaler())
                ]
            )

            cat_pipeline=Pipeline(
                steps=[
                    ('SimpleImputer',SimpleImputer(strategy='most_frequent')),
                    ('OneHotEncoder',OneHotEncoder())
                ]
            )

            preprocessor=ColumnTransformer(
                [
                    ('num_pipeline',num_pipeline,num_columns),
                    ('cat_pipeline',cat_pipeline,cat_columns)
                ]
            )
            logging.info('Training and test pipeline have been created')

            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)


    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info('train and test dataframe created.')
            preprocessor_obj=self.data_transformation_get_obj()
            train_input_df=train_df.drop(columns=['charges'])
            train_target_df=train_df['charges']
            test_input_df=test_df.drop(columns=['charges'])
            test_target_df=test_df['charges']
            logging.info('data has splitted succesfully into target and input')

            train_input_arr=preprocessor_obj.fit_transform(train_input_df)
            test_input_arr=preprocessor_obj.transform(test_input_df)

            train_arr=np.c_[train_input_arr,np.array(train_target_df)]
            test_arr=np.c_[test_input_arr,np.array(test_target_df)]

            save_obj(
                file_path=self.data_trans_config.preprocessor_obj_file_path,
                obj=preprocessor_obj
            )

            logging.info('object saved in a pickle file')
            return (
                train_arr,
                test_arr,
                self.data_trans_config.preprocessor_obj_file_path
            )

        except Exception as e:
            raise CustomException(e,sys)