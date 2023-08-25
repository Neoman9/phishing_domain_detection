from phishing.logger import logging
from phishing.exception import PhishingException
from phishing.entity.artifact_entity import DataIngestionArtifact
from phishing.entity.config_entity import DataIngestionConfig
import sys,os
from phishing.constants import *
import numpy as np
import urllib
import pandas as pd
import shutil
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import train_test_split


class DataIngestion:

    def __init__ (self, data_ingestion_config : DataIngestionConfig):
        try:
            logging.info(f"{'>>' *20}  Data ingestion log started. {'<<' *20 }")
            self.data_ingestion_config =  data_ingestion_config

        except Exception as e:
            raise PhishingException(e,sys) from e 
        
    def download_phishing_data(self) -> str:
        try:
            dataset_path = self.data_ingestion_config.dataset_path
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            if os.path.exists(raw_data_dir):
                os.remove(raw_data_dir)

            os.makedirs(raw_data_dir,exist_ok=True)
            phishing_file_name = os.path.basename(dataset_path)
            raw_data_dir = os.path.join(raw_data_dir, phishing_file_name)

            logging.info(f"Copying file from: [{dataset_path}] into: [{raw_data_dir}]")
            shutil.copyfile(dataset_path, raw_data_dir)

            logging.info(f"File: [{raw_data_dir}] has been copied successfully.")
            return raw_data_dir
        except Exception as e:
            raise PhishingException(e, sys) from e
        


    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            file_name = os.path.basename(self.data_ingestion_config.dataset_path)
            phishing_file_path = os.path.join(raw_data_dir, file_name)

            logging.info(f"Reading csv file: [{phishing_file_path}]")
            phishing_data_frame = pd.read_csv(phishing_file_path)

            logging.info(f"Splitting data into train and test")
            strat_train_set, strat_test_set = train_test_split(
                phishing_data_frame,
                test_size=0.2,
                random_state=42
            )

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir, file_name)
            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir, file_name)

            os.makedirs(self.data_ingestion_config.ingested_train_dir, exist_ok=True)
            os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok=True)

            logging.info(f"Exporting training dataset to file: [{train_file_path}]")
            strat_train_set.to_csv(train_file_path, index=False)

            logging.info(f"Exporting test dataset to file: [{test_file_path}]")
            strat_test_set.to_csv(test_file_path, index=False)

            data_ingestion_artifact = DataIngestionArtifact(
                train_file_path=train_file_path,
                test_file_path=test_file_path,
                is_ingested=True,
                message=f"Data ingestion completed successfully."
            )

            logging.info(f"Data Ingestion artifact: [{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise PhishingException(e, sys) from e

        
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            self.download_phishing_data()
            return self.split_data_as_train_test()
            
           
        except Exception as e:
            raise PhishingException(e, sys) from e

    def __del__(self):
        logging.info(f"{'>>'*20}Data Ingestion log completed.{'<<'*20} \n\n")
    