from phishing.logger import logging
from phishing.exception import PhishingException
from phishing.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact, ModelEvaluationArtifact, ModelPusherArtifact
from phishing.entity.config_entity import DataIngestionConfig
from phishing.config.configuration import configuration
from phishing.constants import *


from phishing.component.data_ingestion import DataIngestion
from phishing.component.data_validation import DataValidation
from phishing.component.data_transformation import DataTransformation
from phishing.component.model_trainer import ModelTrainer
from phishing.component.model_evaluation import ModelEvaluation
from phishing.component.model_pusher import ModelPusher




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
        
    def start_model_trainer(self, data_transformation_artifact : DataTransformationArtifact )-> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer (model_trainer_config=self.config.get_model_trainer_config(), data_transformation_artifact=data_transformation_artifact)

            return model_trainer.initiate_model_trainer()

        except Exception as e:
            raise PhishingException(e,sys) from e 
        
    def start_model_evaluation(self,data_ingestion_artifact : DataIngestionArtifact, data_validation_artifact: DataValidationArtifact,
                               model_trainer_artifact: ModelTrainerArtifact)-> ModelEvaluationArtifact:
        try:
            model_evaluation = ModelEvaluation (model_evaluation_config= self.config.get_model_evaluation_config(), data_ingestion_artifact=data_ingestion_artifact,
                                                data_validation_artifact=data_validation_artifact,model_trainer_artifact= model_trainer_artifact)
            
            return model_evaluation.initiate_model_evaluation()

        except Exception as e:
            raise PhishingException(e,sys) from e
        
    def start_model_pusher(self, model_evaluation_artifact : ModelEvaluationArtifact)-> ModelPusherArtifact:
        try:
            model_pusher=  ModelPusher(model_pusher_config= self.config.get_model_pusher_config(),model_evaluation_artifact=model_evaluation_artifact)

            return model_pusher.initiate_model_pusher()
        
        except Exception as e:
            raise PhishingException(e,sys) from e
        
        




