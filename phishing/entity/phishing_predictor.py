import os, sys
import pandas as pd

from phishing.exception import PhishingException
from phishing.util.util import load_object

class PhishingData:

    def __init__(self ,
                 qty_dot_url: int, qty_hyphen_url: int,qty_underline_url: int, qty_slash_url: int,
                 qty_questionmark_url: int, qty_equal_url: int, qty_at_url: int, qty_and_url: int,
                 qty_exclamation_url: int, qty_space_url: int, qty_tilde_url: int,qty_comma_url: int,
                 qty_plus_url: int,qty_asterisk_url: int,qty_hashtag_url: int,qty_dollar_url: int,
                 qty_percent_url: int,qty_tld_url: int,length_url: int,qty_dot_domain: int,qty_hyphen_domain: int,
                 qty_underline_domain: int,qty_at_domain: int,qty_vowels_domain: int,domain_length: int,domain_in_ip: int, server_client_domain: int,
                 qty_dot_directory: int,qty_hyphen_directory: int,qty_underline_directory: int,qty_slash_directory: int,
                 qty_questionmark_directory: int,qty_equal_directory: int,qty_at_directory: int,qty_and_directory: int,
                 qty_exclamation_directory: int,qty_space_directory: int,qty_tilde_directory: int,qty_comma_directory: int,qty_plus_directory: int,
                 qty_asterisk_directory: int,qty_hashtag_directory: int,qty_dollar_directory: int,qty_percent_directory: int,directory_length: int,
                 qty_dot_file: int,qty_hyphen_file: int,qty_underline_file: int,qty_slash_file: int,qty_questionmark_file: int,qty_equal_file: int,
                 qty_at_file: int,qty_and_file: int,qty_exclamation_file: int,qty_space_file: int,qty_tilde_file: int,qty_comma_file: int,
                 qty_plus_file: int,qty_asterisk_file: int,qty_hashtag_file: int,qty_dollar_file: int,qty_percent_file: int,file_length: int,
                 qty_dot_params: int,qty_hyphen_params: int,qty_underline_params: int,qty_slash_params: int,qty_questionmark_params: int,qty_equal_params: int,
                 qty_at_params: int,qty_and_params: int,qty_exclamation_params: int,qty_space_params: int,qty_tilde_params: int,qty_comma_params: int,qty_plus_params: int,
                 qty_asterisk_params: int,qty_hashtag_params: int,qty_dollar_params: int,qty_percent_params: int, params_length: int,tld_present_params: int,
                 qty_params: int,email_in_url: int,time_response: int,domain_spf: int,asn_ip: int, time_domain_activation: int,time_domain_expiration: int,
                 qty_ip_resolved: int,qty_nameservers: int,qty_mx_servers: int,ttl_hostname: int,tls_ssl_certificate: int,qty_redirects: int,
                 url_google_index: int,domain_google_index: int,url_shortened: int, phishing: int = None):
        
        try:
            self.qty_dot_url = qty_dot_url
            self.qty_hyphen_url= qty_hyphen_url
            self.qty_underline_url= qty_underline_url
            self.qty_slash_url= qty_slash_url
            self.qty_questionmark_url= qty_questionmark_url
            self.qty_equal_url= qty_equal_url
            self.qty_at_url= qty_at_url
            self.qty_and_url= qty_and_url
            self.qty_exclamation_url= qty_exclamation_url
            self.qty_space_url= qty_space_url
            self.qty_tilde_url= qty_tilde_url
            self.qty_comma_url= qty_comma_url
            self.qty_plus_url= qty_plus_url
            self.qty_asterisk_url= qty_asterisk_url
            self.qty_hashtag_url= qty_hashtag_url
            self.qty_dollar_url= qty_dollar_url
            self.qty_percent_url= qty_percent_url
            self.qty_tld_url= qty_tld_url
            self.length_url= length_url
            self.qty_dot_domain= qty_dot_domain
            self.qty_hyphen_domain= qty_hyphen_domain
            self.qty_underline_domain= qty_underline_domain
            self.qty_at_domain= qty_at_domain
            self.qty_vowels_domain= qty_vowels_domain
            self.domain_length= domain_length
            self.domain_in_ip= domain_in_ip
            self.server_client_domain= server_client_domain
            self.qty_dot_directory= qty_dot_directory
            self.qty_hyphen_directory= qty_hyphen_directory
            self.qty_underline_directory=qty_underline_directory
            self.qty_slash_directory= qty_slash_directory
            self.qty_questionmark_directory= qty_questionmark_directory
            self.qty_equal_directory= qty_equal_directory
            self.qty_at_directory= qty_at_directory
            self.qty_and_directory= qty_and_directory
            self.qty_exclamation_directory= qty_exclamation_directory
            self.qty_space_directory= qty_space_directory
            self.qty_tilde_directory= qty_tilde_directory
            self.qty_comma_directory= qty_comma_directory
            self.qty_plus_directory= qty_plus_directory
            self.qty_asterisk_directory= qty_asterisk_directory
            self.qty_hashtag_directory= qty_hashtag_directory
            self.qty_dollar_directory= qty_dollar_directory
            self.qty_percent_directory= qty_percent_directory
            self.directory_length= directory_length
            self.qty_dot_file= qty_dot_file
            self.qty_hyphen_file= qty_hyphen_file
            self.qty_underline_file= qty_underline_file
            self.qty_slash_file= qty_slash_file
            self.qty_questionmark_file= qty_questionmark_file
            self.qty_equal_file= qty_equal_file
            self.qty_at_file= qty_at_file
            self.qty_and_file= qty_and_file
            self.qty_exclamation_file= qty_exclamation_file
            self.qty_space_file= qty_space_file
            self.qty_tilde_file= qty_tilde_file
            self.qty_comma_file= qty_comma_file
            self.qty_plus_file= qty_plus_file
            self.qty_asterisk_file=qty_asterisk_file
            self.qty_hashtag_file= qty_hashtag_file
            self.qty_dollar_file= qty_dollar_file
            self.qty_percent_file= qty_percent_file
            self.file_length= file_length
            self.qty_dot_params= qty_dot_params
            self.qty_hyphen_params= qty_hyphen_params
            self.qty_underline_params= qty_underline_params
            self.qty_slash_params= qty_slash_params
            self.qty_questionmark_params= qty_questionmark_params
            self.qty_equal_params= qty_equal_params
            self.qty_at_params= qty_at_params
            self.qty_and_params= qty_and_params
            self.qty_exclamation_params= qty_exclamation_params
            self.qty_space_params= qty_space_params
            self.qty_tilde_params= qty_tilde_params
            self.qty_comma_params= qty_comma_params
            self.qty_plus_params= qty_plus_params
            self.qty_asterisk_params= qty_asterisk_params
            self.qty_hashtag_params= qty_hashtag_params
            self.qty_dollar_params= qty_dollar_params
            self.qty_percent_params= qty_percent_params
            self.params_length= params_length
            self.tld_present_params= tld_present_params
            self.qty_params=qty_params
            self.email_in_url= email_in_url
            self.time_response= time_response
            self.domain_spf= domain_spf
            self.asn_ip= asn_ip
            self.time_domain_activation= time_domain_activation
            self.time_domain_expiration= time_domain_expiration
            self.qty_ip_resolved= qty_ip_resolved
            self.qty_nameservers= qty_nameservers
            self.qty_mx_servers= qty_mx_servers
            self.ttl_hostname= ttl_hostname
            self.tls_ssl_certificate= tls_ssl_certificate
            self.qty_redirects= qty_redirects
            self.url_google_index= url_google_index
            self.domain_google_index= domain_google_index
            self.url_shortened= url_shortened
            self.phishing= phishing
        except Exception as e:
            raise PhishingException(e,sys) from e
        
    def get_phishing_input_dataframe(self):
        try:
            phishing_input_dict= self.get_phishing_data_dict()
            return pd.DataFrame(phishing_input_dict)

        except Exception as e:
            raise PhishingException(e, sys) from e
        
    def get_phishing_data_dict(self):
        try:
            input_data ={
                "qty_dot_url": [self.qty_dot_url],
                "qty_hyphen_url" : [self.qty_hyphen_url],
                "qty_underline_url": [self.qty_underline_url],
                "qty_slash_url": [self.qty_slash_url],
                "qty_questionmark_url": [self.qty_questionmark_url],
                "qty_equal_url": [self.qty_equal_url],
                "qty_at_url": [self.qty_at_url],
                "qty_and_url": [self.qty_and_url],
                "qty_exclamation_url": [self.qty_exclamation_url],
                "qty_space_url": [self.qty_space_url],
                "qty_tilde_url": [self.qty_tilde_url],
                "qty_comma_url": [self.qty_comma_url],
                "qty_plus_url": [self.qty_plus_url],
                "qty_asterisk_url": [self.qty_asterisk_url],
                "qty_hashtag_url": [self.qty_hashtag_url],
                "qty_dollar_url": [self.qty_dollar_url],
                "qty_percent_url": [self.qty_percent_url],
                "qty_tld_url": [self.qty_tld_url],
                "length_url": [self.length_url],
                "qty_dot_domain": [self.qty_dot_domain],
                "qty_hyphen_domain": [self.qty_hyphen_domain],
                "qty_underline_domain":[self.qty_underline_domain],
                "qty_at_domain": [self.qty_at_domain],
                "qty_vowels_domain":[self.qty_vowels_domain],
                "domain_length": [self.domain_length],
                "domain_in_ip": [self.domain_in_ip],
                "server_client_domain": [self.server_client_domain],
                "qty_dot_directory": [self.qty_dot_directory],
                "qty_hyphen_directory": [self.qty_hyphen_directory],
                "qty_underline_directory": [self.qty_underline_directory],
                "qty_slash_directory": [self.qty_slash_directory],
                "qty_questionmark_directory": [self.qty_questionmark_directory],
                "qty_equal_directory": [self.qty_equal_directory],
                "qty_at_directory": [self.qty_at_directory],
                "qty_and_directory": [self.qty_and_directory],
                "qty_exclamation_directory": [self.qty_exclamation_directory],
                "qty_space_directory": [self.qty_space_directory],
                "qty_tilde_directory": [self.qty_tilde_directory],
                "qty_comma_directory": [self.qty_comma_directory],
                "qty_plus_directory": [self.qty_plus_directory],
                "qty_asterisk_directory": [self.qty_asterisk_directory],
                "qty_hashtag_directory": [self.qty_hashtag_directory],
                "qty_dollar_directory": [self.qty_dollar_directory],
                "qty_percent_directory": [self.qty_percent_directory],
                "directory_length": [self.directory_length],
                "qty_dot_file": [self.qty_dot_file],
                "qty_hyphen_file": [self.qty_hyphen_file],
                "qty_underline_file": [self.qty_underline_file],
                "qty_slash_file": [self.qty_slash_file],
                "qty_questionmark_file": [self.qty_questionmark_file],
                "qty_equal_file": [self.qty_equal_file],
                "qty_at_file": [self.qty_at_file],
                "qty_and_file": [self.qty_and_file],
                "qty_exclamation_file": [self.qty_exclamation_file],
                "qty_space_file": [self.qty_space_file],
                "qty_tilde_file": [self.qty_tilde_file],
                "qty_comma_file": [self.qty_comma_file],
                "qty_plus_file": [self.qty_plus_file],
                "qty_asterisk_file": [self.qty_asterisk_file],
                "qty_hashtag_file": [self.qty_hashtag_file],
                "qty_dollar_file": [self.qty_dollar_file],
                "qty_percent_file": [self.qty_percent_file],
                "file_length": [self.file_length],
                "qty_dot_params": [self.qty_dot_params],
                "qty_hyphen_params": [self.qty_hyphen_params],
                "qty_underline_params": [self.qty_underline_params],
                "qty_slash_params": [self.qty_slash_params],
                "qty_questionmark_params": [self.qty_questionmark_params],
                "qty_equal_params": [self.qty_equal_params],
                "qty_at_params": [self.qty_at_params],
                "qty_and_params": [self.qty_and_params],
                "qty_exclamation_params": [self.qty_exclamation_params],
                "qty_space_params": [self.qty_space_params],
                "qty_tilde_params": [self.qty_tilde_params],
                "qty_comma_params": [self.qty_comma_params],
                "qty_plus_params": [self.qty_plus_params],
                "qty_asterisk_params": [self.qty_asterisk_params],
                "qty_hashtag_params": [self.qty_hashtag_params],
                "qty_dollar_params": [self.qty_dollar_params],
                "qty_percent_params": [self.qty_percent_params],
                "params_length": [self.params_length],
                "tld_present_params": [self.tld_present_params],
                "qty_params": [self.qty_params],
                "email_in_url": [self.email_in_url],
                "time_response": [self.time_response],
                "domain_spf": [self.domain_spf],
                "asn_ip": [self.asn_ip],
                "time_domain_activation": [self.time_domain_activation],
                "time_domain_expiration": [self.time_domain_expiration],
                "qty_ip_resolved": [self.qty_ip_resolved],
                "qty_nameservers": [self.qty_nameservers],
                "qty_mx_servers": [self.qty_mx_servers],
                "ttl_hostname": [self.ttl_hostname],
                "tls_ssl_certificate": [self.tls_ssl_certificate],
                "qty_redirects": [self.qty_redirects],
                "url_google_index": [self.url_google_index],
                "domain_google_index": [self.domain_google_index],
                "url_shortened": [self.url_shortened]
            }

            return input_data

        except Exception as e :
            raise PhishingException(e, sys) from e 


class PhishingPredictor:

    def __init__(self, model_dir: str):
        try:
            self.model_dir= model_dir

        except Exception as e:
            raise PhishingException(e, sys ) from e 
        
    def get_latest_model_path(self):
        try:
            folder_name= list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path

        except Exception as e:
            raise PhishingException(e, sys) from e
        
    def predict(self, X):
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            phishing= model.predict(X)
            return phishing


        except Exception as e:
            raise PhishingException(e, sys) from e