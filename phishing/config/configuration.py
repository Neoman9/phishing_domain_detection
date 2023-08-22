from phishing.exception import PhishingException
from phishing.logger import logging
from phishing.entity.config_entity import  DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig
from phishing.util.util import read_yaml_file


import sys, os
from phishing.constants import *

class configuration:
    def __init__(self, config_file_path:str = CONFIG_FILE_PATH, config_time_stamp: str = CURRENT_TIME_STAMP ) -> None:

        try:

            self.config_info = read_yaml_file(file_path= config_file_path)
            self.training_pipeline_config = self.get_training_pipeline_config()
            self.time_stamp= CURRENT_TIME_STAMP
        
        except Exception as e:
            raise PhishingException(e,sys) from e 
        
    def get_data_ingestion_config (self ) -> DataIngestionConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_ingestion_artifact_dir = os.path.join(artifact_dir,  DATA_INGESTION_ARTIFACT_DIR, self.time_stamp)
            data_ingestion_info=  self.config_info[DATA_INGESTION_CONFIG_KEY]

            dataset_download_url = data_ingestion_info[DATA_INGESTION_DATASET_DOWNLOAD_URL_KEY]
            raw_data_dir= os.path.join (data_ingestion_artifact_dir, data_ingestion_info[DATA_INGESTION_RAW_DATA_DIR_KEY])
            ingested_data_dir= os.path.join(data_ingestion_artifact_dir, data_ingestion_info[DATA_INGESTION_INGESTED_DIR_KEY])
            ingested_test_dir = os.path.join(ingested_data_dir, data_ingestion_info[DATA_INGESTION_INGESTED_TEST_DIR_KEY])
            ingested_train_dir= os.path.join(ingested_data_dir, data_ingestion_info[DATA_INGESTION_INGESTED_TRAIN_DIR_KEY])


            data_ingestion_config= DataIngestionConfig(dataset_download_url= dataset_download_url,
                                                       raw_data_dir=raw_data_dir,ingested_test_dir=ingested_test_dir, ingested_train_dir=ingested_train_dir)
            
            logging.info(f" Data ingested config : {data_ingestion_config}")


            return data_ingestion_config
        except Exception as e:
            raise PhishingException(e,sys) from e 
        
    def get_data_validation_config(self)-> DataValidationConfig:
        try:
            artifact_dir = self.training_pipeline_config.artifact_dir
            data_validation_artifact_dir = os.path.join(artifact_dir, DATA_VALIDATION_ARTIFACT_DIR , self.time_stamp)
            data_validation_config_info= self.config_info[DATA_VALIDATION_CONFIG_KEY]

            schema_file_path= os.path.join(ROOT_DIR, data_validation_config_info(DATA_VALIDATION_SCHEMA_DIR_KEY), data_validation_config_info(DATA_VALIDATION_SCHEMA_FILE_NAME_KEY))
            report_file_path= os.path.join(data_validation_artifact_dir,data_validation_config_info(DATA_VALIDATION_REPORT_FILE_NAME_KEY))
            report_page_file_path = os.path.join(data_validation_artifact_dir, data_validation_config_info(DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY))

            data_validation_config= DataValidationConfig(schema_file_path=schema_file_path,report_file_path=report_file_path,report_page_file_path=report_page_file_path)

            logging.info(f" Data Validation config: {data_validation_config}")
            return data_validation_config


        except Exception as e:
            raise PhishingException(e,sys) from e
        


    def get_training_pipeline_config(self) ->TrainingPipelineConfig:
        try:
            training_pipeline_config = self.config_info[TRAINING_PIPELINE_CONFIG_KEY]
            artifact_dir = os.path.join(ROOT_DIR,
            training_pipeline_config[TRAINING_PIPELINE_NAME_KEY],
            training_pipeline_config[TRAINING_PIPELINE_ARTIFACT_DIR_KEY]
            )

            training_pipeline_config = TrainingPipelineConfig(artifact_dir=artifact_dir)
            logging.info(f"Training pipleine config: {training_pipeline_config}")
            return training_pipeline_config
        
        except Exception as e:
            raise PhishingException(e,sys) from e 
    