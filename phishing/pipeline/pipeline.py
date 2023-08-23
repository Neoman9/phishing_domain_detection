from phishing.logger import logging
from phishing.exception import PhishingException
from phishing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact
from phishing.entity.config_entity import DataIngestionConfig
from phishing.config.configuration import configuration
from phishing.constants import *


from phishing.component.data_ingestion import DataIngestion
from phishing.component.data_validation import DataValidation
from phishing.component.data_transformation import DataTransformation




import os,sys

from collections import namedtuple
from datetime import datetime
import uuid 
from multiprocessing import process
from typing import List 
from threading import Thread




Experiment = namedtuple("Experiment", ["experiment_id", "initialization_timestamp", "artifact_time_stamp",
                                       "running_status", "start_time", "stop_time", "execution_time", "message",
                                       "experiment_file_path", "accuracy", "is_model_accepted"])


class Pipeline(Thread):
    experiment: Experiment = Experiment(*([None] * 11))
    experiment_file_path = None

    def __init__(self, config: configuration ) -> None:
        try:
            os.makedirs(config.training_pipeline_config.artifact_dir, exist_ok=True)
            Pipeline.experiment_file_path=os.path.join(config.training_pipeline_config.artifact_dir,EXPERIMENT_DIR_NAME, EXPERIMENT_FILE_NAME)
            super().__init__(daemon=False, name="pipeline")
            self.config = config
        except Exception as e:
            raise PhishingException(e, sys) from e
        

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise PhishingException(e, sys) from e

    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact :
        try:
            data_validation =  DataValidation(data_validation_config=self.config.get_data_validation_config(), data_ingestion_artifact=data_ingestion_artifact)

            return data_validation.initiate_data_validation()

        except Exception as e:
            raise PhishingException(e,sys) from e
        
    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_artifact: DataValidationArtifact)->DataTransformationArtifact:
        try:
            Data_Transformation = DataTransformation(data_transformation_config=self.config.get_data_transformation_config(),data_ingestion_artifact=data_ingestion_artifact,data_validation_artifact=data_validation_artifact)

            return Data_Transformation.initiate_data_transformation()

        except Exception as e:
            raise PhishingException(e,sys) from e
        
        




