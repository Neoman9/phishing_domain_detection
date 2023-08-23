import os
from datetime import datetime


def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

    
ROOT_DIR = os.getcwd()  #to get current working directory
CONFIG_DIR = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)



CURRENT_TIME_STAMP = get_current_time_stamp()


# Training pipeline related variable
TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir"
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"


EXPERIMENT_DIR_NAME="experiment"
EXPERIMENT_FILE_NAME="experiment.csv"




#data ingested related variable 
DATA_INGESTION_CONFIG_KEY = "data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR = "data_ingestion"
DATA_INGESTION_DATASET_DOWNLOAD_URL_KEY= "dataset_download_url"
DATA_INGESTION_RAW_DATA_DIR_KEY = "raw_data_dir"
DATA_INGESTION_INGESTED_DIR_KEY= "ingested_dir"
DATA_INGESTION_INGESTED_TRAIN_DIR_KEY= "ingested_train_dir"
DATA_INGESTION_INGESTED_TEST_DIR_KEY= "ingested_test_dir"



#data validation related variable 
DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_ARTIFACT_DIR= "data_validation"
DATA_VALIDATION_SCHEMA_DIR_KEY= "schema_dir"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = "schema_file_name"
DATA_VALIDATION_REPORT_FILE_NAME_KEY= "report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY ="report_page_file_name"


#data transformation related variable 
DATA_TRANSFORMATON_CONFIG_KEY = "data_transformation_config"
DATA_TRANSFORMATION_ARTIFACT_DIR = "data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DIR_KEY = "transformed_dir"
DATA_TRANSFORMATION_TRANSFORMED_TRAIN_DIR_KEY= "transformed_train_dir"
DATA_TRANSFORMATION_TRANSFORMED_TEST_DIR_KEY= "transformed_test_dir"
DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY= "preprocessing_dir"
DATA_TRANSFOEMATION_PREPROCESSED_OBJECT_FILE_NAME_KEY= "preprocessed_object_file_name"

#schema variables 
DATASET_SCHEMA_COLUMNS_KEY=  "columns"
NUMERICAL_COLUMN_KEY="numerical_columns"
TARGET_COLUMN_KEY="target_column"

#model trainer related variable
MODEL_TRAINER_CONFIG_KEY = "model_trainer_config"
MODEL_TRAINER_ARTIFACT_DIR= "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR_KEY= "trained_model_dir"
MODEL_TRAINER_MODEL_FILE_NAME_KEY= "model_file_name"
MODEL_TRAINER_BASE_ACCURACY_KEY="base_accuracy"
MODEL_TRAINER_MODEL_CONFIG_DIR_KEY= "model_config_dir"
MODEL_TRAINER_MODEL_CONFIG_FILE_NAME_KEY= "model_config_file_name"




