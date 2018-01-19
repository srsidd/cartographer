#!/usr/bin/python
#
# Author: Siddharth Srivatsa <srivatsasiddharth@gmail.com>, 1/2018
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
logger.addHandler(log_handler)

class CartographerIface(object):
""" Class to interface with the Cartographer client """

    def __init__(self, cartographer_client):
        self.client = cartographer_client
        self.addr = None

    def use_custom_geoCoding(self):
        """ Method to send a http GET req to a custom url 
            
            Returns: (String) Response sent by the server or None
        """
        query_url = raw_input("Please enter the entire url to be querried:\n")
        response = self.client.request(url=query_url)
        if api_response is None:
            return None
        confirm = raw_input("Please press y if you would like to parse the json response\n")
        if confirm.lower()=='y' or confirm.lower()=='yes':
            config_path = raw_input("Please enter the config path of the parameter you wish to retrieve the value of:\n")
            return self.client.get_config(response, config_path)
        return response

    def use_google_geoCoding(self):
        """ Method to send a http GET req to the google geo coding req

            Returns: (GeoPoint) Address, latitude and longitude of the address
        """
        if self.addr is None:
            self.addr = self.client.get_address()
        g_data = self.client.google_geocode_service(address=self.addr)
        return g_data

    def use_here_geoCoding(self):
        """ Method to send a http GET req to the here geo coding req

            Returns: (GeoPoint) Address, latitude and longitude of the address
        """
        if self.addr is None:
            self.addr = self.client.get_address()
        g_data = self.client.here_geocode_service(address=self.addr)
        return g_data

    def get_json_config(self):
        """ Method to get the config path to retrieve the latitude, longitude and the address
            from the response returned by the google and here API's

            Returns: (dict) Dictionary for each API with config paths for Address, latitude
            and longitude of the address
        """
        google_json_config = [self.client.get_google_lat_long_config(), self.get_google_addr_config(), self.get_google_status_config()]
        here_json_config = [self.client.get_here_lat_long_config(), self.client.get_here_addr_config(), self.get_here_status_config()]
        
        default_config = {'google_json_config': google_json_config, 
                          'here_json_config': here_json_config}
        return default_config

    def get_api_creds(self):
        """ Method to retrieve the credentials to access the google and here API's

            Returns: (dict) Dictionary for each API with their corresponding api keys and ids
        """
        google_api_cred = self.client.get_google_api_creds()
        here_api_cred = self.client.get_here_api_creds()
        default_creds = {'google_api_cred': google_api_cred, 
                          'here_api_cred': here_api_cred}
        return default_creds

    def set_creds(self, google_api_cred=None, here_creds=None):
        """ Method to set the credentials to access the google and here API's

            google_api_cred: (string) The api google api key which can be got from
                            https://developers.google.com/maps/documentation/geocoding/get-api-key

            here_creds: (list) [app_id, app_code] here API parameters which can be got from
                        https://developer.here.com/documentation/geocoder/common/credentials.html 
        """
        if google_api_cred is not None:
            self.client.set_google_api_creds(google_api_cred)
        if isinstance(here_creds, list) and None not in here_creds:
            self.client.set_here_api_creds(app_id=here_creds[0], app_code=here_creds[1])
        elif here_creds is None:
            pass
        else:
            raise ValueError("Need to set both app_id and app_key")
            return False
        return True