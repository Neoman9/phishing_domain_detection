from setuptools import setup, find_packages
from typing import List

#Declaring variables for setup functions
PROJECT_NAME="Phising_domain_detector"
VERSION="0.0.1"
AUTHOR="Neoman"
DESRCIPTION="A machine learning project focused on identifying phishing domains. Code for data preprocessing, feature engineering, model selection, training, and evaluation can be found in this repo. The project attempts to implement an accurate algorithm for real-time phishing domain identification, improving online security, by utilizing a curated dataset."

REQUIREMENT_FILE_NAME="requirements.txt"

HYPHEN_E_DOT = "-e ."


def get_requirements_list() -> List[str]:
    """
    Description: This function will return list of libararies listed  in the requirements.txt file 
    
    """
    with open(REQUIREMENT_FILE_NAME) as requirement_file:
        requirement_list = requirement_file.readlines()
        requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]
        if HYPHEN_E_DOT in requirement_list:
            requirement_list.remove(HYPHEN_E_DOT)
        return requirement_list



setup(
name=PROJECT_NAME,
version=VERSION,
author=AUTHOR,
description=DESRCIPTION,
packages=find_packages(), 
install_requires=get_requirements_list()
)