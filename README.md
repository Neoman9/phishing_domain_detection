
## Phishing Domain Detection

This project aims to identify and classify phishing websites or domains.Code for data preprocessing, feature engineering, model selection, training, and evaluation can be found in this repo. The project attempts to implement an accurate algorithm for real-time phishing domain identification, improving online security, by utilizing a curated dataset.


## Table of Contents 

- [Phishing Domain Detection](#phishing-domain-detection)
  - [Table of Contents](#table-of-contents)
  - [Description](#description)
  - [Tech Stack Used](#tech-stack-used)
  - [Infrastructure Required](#)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [Acknowledgements](#)
  - [License](#license)
## Description 

This research assists in locating potentially harmful domains that are employed in phishing scams. The dataset for this project was obtained from the internship page of Ineuron.ai, and it consisted of 87,000 domains, a mix of legitimate and fraudulent domains. These domains were gathered, cleaned, analyzed, preprocessed, trained, and evaluated in order to create predictive models that aid in the detection of phishing domains in order to lessen cyberattacks.
## Tech Stack Used

- [Python](#)
- [Flask](#)
- [Docker](#)
- [Machine learning algorithms](#)
- [HTML, Java Script](#)

## Infrastructure Required

- [AWS EC2 Instance](#)
- [AWS ECR](#)
- [GIT Actions](#)
## Usage 

To get started with detecting Phishing Domain, you will need an AWS account to to access services like, EC2 Instances and ECR,follow these installation steps:

1. Clone the repository:

git clone https://github.com/Neoman9/phishing_domain_detection.git

2. Create a conda environment after opening the repository

conda create -n my_new_env python=3.10

conda activate my_new_env

3. Install the required dependencies

pip install -r requirements.txt

4. Export the environment variable

export AWS_ACCESS_KEY_ID=<AWS_ACCESS_KEY_ID>

export AWS_SECRET_ACCESS_KEY=<AWS_SECRET_ACCESS_KEY>

export AWS_DEFAULT_REGION=<AWS_DEFAULT_REGION>

5. Run the application server

python app.py



## Contributing

Contributions are highly welcomed! See `contributing.md` for ways to get started. Please send a pull request if you have any suggestions for changes, enhancements, or bug corrections. You can also create an issue to report issues or offer Feedbacks.
## Acknowledgements

 - [I was inspired for this project by the Ineuron.ai portal page]()
 

## License

[MIT](https://choosealicense.com/licenses/mit/)

