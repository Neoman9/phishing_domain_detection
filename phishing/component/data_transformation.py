from phishing.exception import PhishingException
from phishing.logger import logging
from phishing.constants import *
from phishing.entity.config_entity import DataTransformationConfig
from phishing.entity.artifact_entity import DataTransformationArtifact, DataIngestionArtifact,DataValidationArtifact
from phishing.util.util import *


import os, sys 
import pandas as pd 
import numpy as np


from cgi import test
from sklearn import preprocessing
from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer





class DataTransformation:

        def __init__(self, data_transformation_config: DataTransformationConfig, data_ingestion_artifact: DataIngestionArtifact,data_validation_artifact: DataValidationArtifact ):
            try:
                logging.info(f"{'>>' * 30}Data Transformation log started.{'<<' * 30} ")
                self.data_transformation_config= data_transformation_config
                self.data_ingestion_artifact = data_ingestion_artifact
                self.data_validation_artifact = data_validation_artifact
            
            except Exception as e:
                raise PhishingException(e,sys) from e

        def get_data_transformer_object(self)->ColumnTransformer:
            try:
                schema_file_path = self.data_validation_artifact.schema_file_path

                dataset_schema = read_yaml_file(file_path=schema_file_path)

                numerical_columns = dataset_schema[NUMERICAL_COLUMN_KEY]

                num_pipeline= Pipeline(steps=[('imputer', SimpleImputer(strategy="median")),('scaler', StandardScaler())])

                logging.info(f"Numerical columns:{numerical_columns} ")

                preprocessing= ColumnTransformer([('num_pipeline', num_pipeline,numerical_columns)])
                return preprocessing
            except Exception as e:
                  raise PhishingException(e,sys) from e
            

        
        def initiate_data_transformation(self)-> DataTransformationArtifact:
            try:
                logging.info(f"obtaining prerocessing object")
                preprocessing_obj = self.get_data_transformer_object()

                logging.info(f"obtaining training and testing file path.")
                train_file_path = self.data_ingestion_artifact.train_file_path
                test_file_path=  self.data_ingestion_artifact.test_file_path

                schema_file_path= self.data_validation_artifact.schema_file_path
                schema = read_yaml_file(file_path= schema_file_path)

                logging.info(f"loading training and test data as pandas dataframe")
                train_df = load_data(file_path= train_file_path, schema_file_path=schema_file_path)
                test_df = load_data(file_path=test_file_path , schema_file_path=schema_file_path)
                target_column_name = schema[TARGET_COLUMN_KEY]

                columns_to_remove = ['qty_slash_domain', 'qty_questionmark_domain', 'qty_equal_domain','qty_and_domain','qty_exclamation_domain','qty_space_domain','qty_tilde_domain','qty_comma_domain','qty_plus_domain','qty_asterisk_domain','qty_hashtag_domain','qty_dollar_domain','qty_percent_domain']

                
                logging.info(f"Splitting input and target feature from training and testing dataframe ")
                input_feature_train_df = train_df.drop(columns=[target_column_name] + columns_to_remove, axis=1)
                target_feature_train_df = train_df[target_column_name]

                input_feature_test_df = test_df.drop(columns=[target_column_name] + columns_to_remove, axis=1)
                target_feature_test_df = test_df[target_column_name]

                # Remove duplicates from feature columns
                input_feature_train_df = input_feature_train_df.drop_duplicates()
                input_feature_test_df = input_feature_test_df.drop_duplicates()
        
                # Remove duplicates from target column
                target_feature_train_df = target_feature_train_df.drop_duplicates()
                target_feature_test_df = target_feature_test_df.drop_duplicates()

                logging.info(f"Applying preprocessing object on training dataframe and testing dataframe")
                input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
                input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

                train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
                test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

                transformed_train_dir = self.data_transformation_config.transformed_train_dir
                transformed_test_dir = self.data_transformation_config.transformed_test_dir

                train_file_name = os.path.basename(train_file_path).replace(".csv", ".npz")
                test_file_name = os.path.basename(test_file_path).replace(".csv", ".npz")

                transformed_train_file_path = os.path.join(transformed_train_dir, train_file_name)
                transformed_test_file_path = os.path.join(transformed_test_dir, test_file_name)

                logging.info(f"saving transformed training and testing array.")
                save_numpy_array_data(file_path=transformed_train_file_path, array=train_arr)
                save_numpy_array_data(file_path=transformed_test_file_path, array=test_arr)

                preprocessing_object_file_path = self.data_transformation_config.preprocessed_object_file_path
                logging.info(f"saving preprocessing object.")
                save_object(file_path=preprocessing_object_file_path, obj= preprocessing_obj)

                data_transformation_artifact= DataTransformationArtifact(is_transformed=True,message="Data transformed succesfully",transformed_test_file_path=transformed_test_file_path,
                                                                         transformed_train_file_path=transformed_train_file_path,preprocessed_object_file_path=preprocessing_object_file_path)
                
                logging.info( f"Data transformation artifact : {data_transformation_artifact}")

                return data_transformation_artifact

            except Exception as e:
                raise PhishingException(e,sys) from e
            

        def __del__(self):
            logging.info(f"{'>>'*30}Data Transformation log completed.{'<<'*30} \n\n")
            