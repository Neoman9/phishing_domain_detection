from flask  import Flask, request
from flask import send_file,abort, render_template
import sys
from matplotlib.style import context
import json
import os


import pip
from phishing.util.util import read_yaml_file,write_yaml_file
from phishing.logger import logging
from phishing.exception import PhishingException
from phishing.config.configuration import configuration
from phishing.constants import CONFIG_DIR,get_current_time_stamp
from phishing.pipeline.pipeline import Pipeline
from phishing.entity.phishing_predictor import PhishingData, PhishingPredictor
from phishing.logger import get_log_dataframe

ROOT_DIR = os.getcwd()
LOG_FOLDER_NAME = "logs"
PIPELINE_FOLDER_NAME = "phishing"
SAVED_MODELS_DIR_NAME = "saved_models"
MODEL_CONFIG_FILE_PATH = os.path.join(ROOT_DIR, CONFIG_DIR, "model.yaml")
LOG_DIR = os.path.join(ROOT_DIR, LOG_FOLDER_NAME)
PIPELINE_DIR = os.path.join(ROOT_DIR, PIPELINE_FOLDER_NAME)
MODEL_DIR = os.path.join(ROOT_DIR, SAVED_MODELS_DIR_NAME)


PHISHING_DATA_KEY = "phishing_data"
PHISHING_KEY = "phishing"

app = Flask(__name__)


@app.route('/artifact', defaults={'req_path': 'phishing'})
@app.route('/artifact/<path:req_path>')
def render_artifact_dir(req_path):
    os.makedirs("phishing", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        if ".html" in abs_path:
            with open(abs_path, "r", encoding="utf-8") as file:
                content = ''
                for line in file.readlines():
                    content = f"{content}{line}"
                return content
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file_name): file_name for file_name in os.listdir(abs_path) if
             "artifact" in os.path.join(abs_path, file_name)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('files.html', result=result)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return str(e)
    
@app.route('/view_experiment_hist', methods=['GET', 'POST'])
def view_experiment_history():
    experiment_df = Pipeline.get_experiments_status()
    context = {
        "experiment": experiment_df.to_html(classes='table table-striped col-12')
    }
    return render_template('experiment_history.html', context=context)


@app.route('/train', methods=['GET', 'POST'])
def train():
    message = ""
    pipeline = Pipeline(config=configuration(current_time_stamp=get_current_time_stamp()))
    if not Pipeline.experiment.running_status:
        message = "Training started."
        pipeline.start()
    else:
        message = "Training is already in progress."
    context = {
        "experiment": pipeline.get_experiments_status().to_html(classes='table table-striped col-12'),
        "message": message
    }
    return render_template('train.html', context=context)

def predict():
    context = {
        PHISHING_DATA_KEY: None,
        PHISHING_KEY: None
    }

    if request.method == 'POST':
        qty_dot_url = int(request.form['qty_dot_url'])
        qty_hyphen_url= int(request.form['qty_hyphen_url'])
        qty_underline_url= int(request.form['qty_underline_url'])
        qty_slash_url= int(request.form['qty_slash_url'])
        qty_questionmark_url= int(request.form['qty_questionmark_url'])
        qty_equal_url= int(request.form['qty_equal_url'])
        qty_at_url= int(request.form['qty_at_url'])
        qty_and_url= int(request.form['qty_and_url'])
        qty_exclamation_url= int(request.form['qty_exclamation_url'])
        qty_space_url= int(request.form['qty_space_url'])
        qty_tilde_url= int(request.form['qty_tilde_url'])
        qty_comma_url= int(request.form['qty_comma_url'])
        qty_plus_url= int(request.form['qty_plus_url'])
        qty_asterisk_url= int(request.form['qty_asterisk_url'])
        qty_hashtag_url= int(request.form['qty_hashtag_url'])
        qty_dollar_url= int(request.form['qty_dollar_url'])
        qty_percent_url= int(request.form['qty_percent_url'])
        qty_tld_url= int(request.form['qty_tld_url'])
        length_url= int(request.form['length_url'])
        qty_dot_domain= int(request.form['qty_dot_domain'])
        qty_hyphen_domain= int(request.form['qty_hyphen_domain'])
        qty_underline_domain= int(request.form['qty_underline_domain'])
        qty_at_domain= int(request.form['qty_at_domain'])
        qty_vowels_domain= int(request.form['qty_vowels_domain'])
        domain_length= int(request.form['domain_length'])
        domain_in_ip= int(request.form['domain_in_ip'])
        server_client_domain= int(request.form['server_client_domain'])
        qty_dot_directory= int(request.form['qty_dot_directory'])
        qty_hyphen_directory= int(request.form['qty_hyphen_directory'])
        qty_underline_directory=int(request.form['qty_underline_directory'])
        qty_slash_directory= int(request.form['qty_slash_directory'])
        qty_questionmark_directory= int(request.form['qty_questionmark_directory'])
        qty_equal_directory= int(request.form['qty_equal_directory'])
        qty_at_directory= int(request.form['qty_at_directory'])
        qty_and_directory= int(request.form['qty_and_directory']),
        qty_exclamation_directory= int(request.form['qty_exclamation_directory'])
        qty_space_directory= int(request.form['qty_space_directory'])
        qty_tilde_directory= int(request.form['qty_tilde_directory'])
        qty_comma_directory= int(request.form['qty_comma_directory'])
        qty_plus_directory= int(request.form['qty_plus_directory'])
        qty_asterisk_directory= int(request.form['qty_asterisk_directory'])
        qty_hashtag_directory= int(request.form['qty_hashtag_directory'])
        qty_dollar_directory= int(request.form['qty_dollar_directory'])
        qty_percent_directory= int(request.form['qty_percent_directory'])
        directory_length= int(request.form['directory_length'])
        qty_dot_file= int(request.form['qty_dot_file'])
        qty_hyphen_file= int(request.form['qty_hyphen_file'])
        qty_underline_file= int(request.form['qty_underline_file'])
        qty_slash_file= int(request.form['qty_slash_file'])
        qty_questionmark_file= int(request.form['qty_questionmark_file'])
        qty_equal_file= int(request.form['qty_equal_file'])
        qty_at_file= int(request.form['qty_at_file'])
        qty_and_file= int(request.form['qty_and_file']),
        qty_exclamation_file= int(request.form['qty_exclamation_file'])
        qty_space_file= int(request.form['qty_space_file'])
        qty_tilde_file= int(request.form['qty_tilde_file'])
        qty_comma_file= int(request.form['qty_comma_file'])
        qty_plus_file= int(request.form['qty_plus_file'])
        qty_asterisk_file=int(request.form['qty_asterisk_file'])
        qty_hashtag_file= int(request.form['qty_hashtag_file'])
        qty_dollar_file= int(request.form['qty_dollar_file'])
        qty_percent_file= int(request.form['qty_percent_file'])
        file_length= int(request.form['file_length'])
        qty_dot_params= int(request.form['qty_dot_params'])
        qty_hyphen_params= int(request.form['qty_hyphen_params'])
        qty_underline_params= int(request.form['qty_underline_params'])
        qty_slash_params= int(request.form['qty_slash_params'])
        qty_questionmark_params= int(request.form['qty_questionmark_params'])
        qty_equal_params= int(request.form['qty_equal_params'])
        qty_at_params= int(request.form['qty_at_params'])
        qty_and_params= int(request.form['qty_and_params'])
        qty_exclamation_params= int(request.form['qty_exclamation_params'])
        qty_space_params= int(request.form['qty_space_params'])
        qty_tilde_params= int(request.form['qty_tilde_params'])
        qty_comma_params= int(request.form['qty_comma_params'])
        qty_plus_params= int(request.form['qty_plus_params'])
        qty_asterisk_params= int(request.form['qty_asterisk_params'])
        qty_hashtag_params= int(request.form['qty_hashtag_params'])
        qty_dollar_params= int(request.form['qty_dollar_params'])
        qty_percent_params= int(request.form['qty_percent_params'])
        params_length= int(request.form['params_length'])
        tld_present_params= int(request.form['tld_present_params'])
        qty_params=int(request.form['qty_params'])
        email_in_url= int(request.form['email_in_url'])
        time_response= float(request.form['time_response'])
        domain_spf= int(request.form['domain_spf'])
        asn_ip= int(request.form['asn_ip'])
        time_domain_activation= int(request.form['time_domain_activation'])
        time_domain_expiration= int(request.form['time_domain_expiration'])
        qty_ip_resolved= int(request.form['qty_ip_resolved'])
        qty_nameservers= int(request.form['qty_nameservers'])
        qty_mx_servers= int(request.form['qty_mx_servers'])
        ttl_hostname= int(request.form['ttl_hostname'])
        tls_ssl_certificate= int(request.form['tls_ssl_certificate'])
        qty_redirects= int(request.form['qty_redirects'])
        url_google_index= int(request.form['url_google_index'])
        domain_google_index= int(request.form['domain_google_index'])
        url_shortened= int(request.form['url_shortened'])

        phishing_data = PhishingData(
            
            qty_dot_url = qty_dot_url,
            qty_hyphen_url= qty_hyphen_url,
            qty_underline_url= qty_underline_url,
            qty_slash_url= qty_slash_url,
            qty_questionmark_url= qty_questionmark_url,
            qty_equal_url= qty_equal_url,
            qty_at_url= qty_at_url,
            qty_and_url= qty_and_url,
            qty_exclamation_url= qty_exclamation_url,
            qty_space_url= qty_space_url,
            qty_tilde_url= qty_tilde_url,
            qty_comma_url= qty_comma_url,
            qty_plus_url= qty_plus_url,
            qty_asterisk_url= qty_asterisk_url,
            qty_hashtag_url= qty_hashtag_url,
            qty_dollar_url= qty_dollar_url,
            qty_percent_url= qty_percent_url,
            qty_tld_url= qty_tld_url,
            length_url= length_url,
            qty_dot_domain= qty_dot_domain,
            qty_hyphen_domain= qty_hyphen_domain,
            qty_underline_domain= qty_underline_domain,
            qty_at_domain= qty_at_domain,
            qty_vowels_domain= qty_vowels_domain,
            domain_length= domain_length,
            domain_in_ip= domain_in_ip,
            server_client_domain= server_client_domain,
            qty_dot_directory= qty_dot_directory,
            qty_hyphen_directory= qty_hyphen_directory,
            qty_underline_directory=qty_underline_directory,
            qty_slash_directory= qty_slash_directory,
            qty_questionmark_directory= qty_questionmark_directory,
            qty_equal_directory= qty_equal_directory,
            qty_at_directory= qty_at_directory,
            qty_and_directory= qty_and_directory,
            qty_exclamation_directory= qty_exclamation_directory,
            qty_space_directory= qty_space_directory,
            qty_tilde_directory= qty_tilde_directory,
            qty_comma_directory= qty_comma_directory,
            qty_plus_directory= qty_plus_directory,
            qty_asterisk_directory= qty_asterisk_directory,
            qty_hashtag_directory= qty_hashtag_directory,
            qty_dollar_directory= qty_dollar_directory,
            qty_percent_directory= qty_percent_directory,
            directory_length= directory_length,
            qty_dot_file= qty_dot_file,
            qty_hyphen_file= qty_hyphen_file,
            qty_underline_file= qty_underline_file,
            qty_slash_file= qty_slash_file,
            qty_questionmark_file= qty_questionmark_file,
            qty_equal_file= qty_equal_file,
            qty_at_file= qty_at_file,
            qty_and_file= qty_and_file,
            qty_exclamation_file= qty_exclamation_file,
            qty_space_file= qty_space_file,
            qty_tilde_file= qty_tilde_file,
            qty_comma_file= qty_comma_file,
            qty_plus_file= qty_plus_file,
            qty_asterisk_file=qty_asterisk_file,
            qty_hashtag_file= qty_hashtag_file,
            qty_dollar_file= qty_dollar_file,
            qty_percent_file= qty_percent_file,
            file_length= file_length,
            qty_dot_params= qty_dot_params,
            qty_hyphen_params= qty_hyphen_params,
            qty_underline_params= qty_underline_params,
            qty_slash_params= qty_slash_params,
            qty_questionmark_params= qty_questionmark_params,
            qty_equal_params= qty_equal_params,
            qty_at_params= qty_at_params,
            qty_and_params= qty_and_params,
            qty_exclamation_params= qty_exclamation_params,
            qty_space_params= qty_space_params,
            qty_tilde_params= qty_tilde_params,
            qty_comma_params= qty_comma_params,
            qty_plus_params= qty_plus_params,
            qty_asterisk_params= qty_asterisk_params,
            qty_hashtag_params= qty_hashtag_params,
            qty_dollar_params= qty_dollar_params,
            qty_percent_params= qty_percent_params,
            params_length= params_length,
            tld_present_params= tld_present_params,
            qty_params=qty_params,
            email_in_url= email_in_url,
            time_response= time_response,
            domain_spf= domain_spf,
            asn_ip= asn_ip,
            time_domain_activation= time_domain_activation,
            time_domain_expiration= time_domain_expiration,
            qty_ip_resolved= qty_ip_resolved,
            qty_nameservers= qty_nameservers,
            qty_mx_servers= qty_mx_servers,
            ttl_hostname= ttl_hostname,
            tls_ssl_certificate= tls_ssl_certificate,
            qty_redirects= qty_redirects,
            url_google_index= url_google_index,
            domain_google_index= domain_google_index,
            url_shortened= url_shortened,
                                   )
        phishing_df = phishing_data.get_phishing_input_dataframe()
        phishing_predictor = PhishingPredictor(model_dir=MODEL_DIR)
        phishing_value = phishing_predictor.predict(X=phishing_df)
        context = {
            PHISHING_DATA_KEY: phishing_data.get_phishing_data_dict(),
            PHISHING_KEY: phishing_value,
        }
        return render_template('predict.html', context=context)
    return render_template("predict.html", context=context)

@app.route('/saved_models', defaults={'req_path': 'saved_models'})
@app.route('/saved_models/<path:req_path>')
def saved_models_dir(req_path):
    os.makedirs("saved_models", exist_ok=True)
    # Joining the base and the requested path
    print(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        return send_file(abs_path)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('saved_models_files.html', result=result)

@app.route("/update_model_config", methods=['GET', 'POST'])
def update_model_config():
    try:
        if request.method == 'POST':
            model_config = request.form['new_model_config']
            model_config = model_config.replace("'", '"')
            print(model_config)
            model_config = json.loads(model_config)

            write_yaml_file(file_path=MODEL_CONFIG_FILE_PATH, data=model_config)

        model_config = read_yaml_file(file_path=MODEL_CONFIG_FILE_PATH)
        return render_template('update_model.html', result={"model_config": model_config})

    except  Exception as e:
        logging.exception(e)
        return str(e)
    
@app.route(f'/logs', defaults={'req_path': f'{LOG_FOLDER_NAME}'})
@app.route(f'/{LOG_FOLDER_NAME}/<path:req_path>')
def render_log_dir(req_path):
    os.makedirs(LOG_FOLDER_NAME, exist_ok=True)
    # Joining the base and the requested path
    logging.info(f"req_path: {req_path}")
    abs_path = os.path.join(req_path)
    print(abs_path)
    # Return 404 if path doesn't exist
    if not os.path.exists(abs_path):
        return abort(404)

    # Check if path is a file and serve
    if os.path.isfile(abs_path):
        log_df = get_log_dataframe(abs_path)
        context = {"log": log_df.to_html(classes="table-striped", index=False)}
        return render_template('log.html', context=context)

    # Show directory contents
    files = {os.path.join(abs_path, file): file for file in os.listdir(abs_path)}

    result = {
        "files": files,
        "parent_folder": os.path.dirname(abs_path),
        "parent_label": abs_path
    }
    return render_template('log_files.html', result=result)


if __name__ == "__main__":
    app.run()
