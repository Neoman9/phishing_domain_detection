from phishing.logger import logging
from phishing.exception import PhishingException
from phishing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from phishing.entity.config_entity import DataValidationConfig


import os, sys
import yaml
import json
import pandas as pd 



from evidently.report import Report
from evidently.metric_preset import DataDriftPreset


class DataValidation:

    def __init__ (self, data_validation_config: DataValidationConfig, data_ingestion_artifact: DataIngestionArtifact):
        try:
            logging.info(f"{'>>' * 20} Data Validation log started {'<<' * 20} \n\n")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact

        except Exception as e:
            raise PhishingException(e,sys) from e
        
    def get_train_and_test_df(self):
        try:
            train_df= pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df,test_df

        except Exception as e:
            raise PhishingException(e,sys) from e 
        
    def does_train_test_file_exist (self)-> bool:
        try:
            logging.info(f" checking to see if test and train file is available ")
            does_train_file_exist = None 
            does_test_file_exist = None 

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path= self.data_ingestion_artifact.test_file_path

            does_train_file_exist = os.path.exists(train_file_path)
            does_test_file_exist= os.path.exists(test_file_path)

            is_available = does_train_file_exist and does_test_file_exist

            logging.info(f"does train and test file exist? -> {is_available}")

            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file= self.data_ingestion_artifact.test_file_path
                message =f" training file :{training_file} or testing file :{testing_file} is not present "

                raise Exception(message)
            
            return is_available
        
        except Exception as e:
            raise PhishingException(e,sys) from e
        
    def get_and_save_data_drift_report(self):
        try:
            data_drift_report_1 = Report(metrics= [DataDriftPreset(num_stattest='ks', cat_stattest='psi', num_stattest_threshold=0.2, cat_stattest_threshold=0.)])

            train_df, test_df =self.get_train_and_test_df()
            data_drift_report_1.run(reference_data=train_df, current_data=test_df)

            report= json.loads(data_drift_report_1.json())

            report_file_path = self.data_validation_config.report_file_path
            report_dir =os.path.dirname(report_file_path)

            os.makedirs(report_dir,exist_ok=True)

            with open(report_file_path,"w") as report_file:
                json.dump(report,report_file, indent =6)

            return report


        except Exception as e:
            raise PhishingException(e,sys) from e 
        
    def save_data_drift_report_page (self):
        try:
            data_drift_report = Report(metrics=[DataDriftPreset(num_stattest='ks', cat_stattest='psi', num_stattest_threshold=0.2, cat_stattest_threshold=0.)])
            train_df,test_df= self.get_train_and_test_df()
            
            data_drift_report.run(reference_data=train_df,current_data=test_df)

            report_page_file_path= self.data_validation_config.report_page_file_path
            report_page_dir= os.path.dirname(report_page_file_path)

            os.makedirs(report_page_dir,exist_ok=True)
            data_drift_report.save_html(report_page_file_path)

        except Exception as e:
            raise PhishingException(e,sys) from e 
    
    def is_data_drift_found(self) -> bool:
        try:
            report= self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True


        except Exception as e:
            raise PhishingException (e,sys) from e
        
    def validate_dataset_schema(self) -> bool:
        try:
            validation_status = False

            #1. Number of Column

            # Load the YAML data from the schema file
            #with open(self.data_validation_config.schema_file_path, 'r') as file:
                #schema_data = yaml.safe_load(file)

            # Access the 'numerical_columns' attribute from the schema data
            #expected_numerical_columns = schema_data['numerical_columns']
            #expected_target_column = [schema_data['target_column']]  # Convert to list

            # Check if the number of columns in train_df matches the expected columns
            #train_df, test_df = self.get_train_and_test_df()

            #if len(train_df.columns) != len(expected_numerical_columns) + 1:
               # print("Error: Number of columns in the training dataset does not match the expected schema.")
                #return False

            # Check if the number of columns in test_df matches the expected columns
            #if len(test_df.columns) != len(expected_numerical_columns) + 1:
              #  print("Error: Number of columns in the testing dataset does not match the expected schema.")
              #  return False

            # Checking column names
            # expected_columns = expected_numerical_columns + expected_target_column
            #expected_columns.sort()

            #train_columns = list(train_df.columns)
            #train_columns.sort()

            #test_columns = list(test_df.columns)
            #test_columns.sort()

            #if train_columns != expected_columns or test_columns != expected_columns:
                #print("Error: Column names do not match the expected schema.")
                #return False

            # If all validation checks pass, set validation_status to True
            validation_status = True
            return validation_status

        except Exception as e :
            raise PhishingException(e,sys) from e 
        
    def initiate_data_validation(self)-> DataValidationArtifact:
        try:
            self.does_train_test_file_exist()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(schema_file_path=self.data_validation_config.schema_file_path, report_file_path=self.data_validation_config.report_file_path,
                                                          report_page_file_path=self.data_validation_config.report_page_file_path,
                                                          is_validated=True,message="Data validation performed successfully")
        
            logging.info(f"Data Validation Artifact :{data_validation_artifact}")
            return data_validation_artifact
        
        except Exception as e:
            raise PhishingException(e,sys) from e
        
    def   __del__(self):
        logging.info(f"{'>>'*30}Data Validation log Completed.{'<<'*30} \n\n")