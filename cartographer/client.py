#!/usr/bin/python
#
# Author: Siddharth Srivatsa <srivatsasiddharth@gmail.com>, 1/2018

"""
Core client functionality, common across all API requests (including performing
HTTP requests).
"""

########################################################
# Here  API credentials - 
# App ID=SXlp6ZNY2WbxLZA2KK9c
# App Code=zYyz6W7wkgMHhaKuxHQO-w

# Google API credentials -
# API key=AIzaSyCkGMOjHINaKqBGFqhjRsxrjoWgAsC5cuI
########################################################


import os
import json
import logging
import ssl
import urllib2

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
logger.addHandler(log_handler)

from geo_point import GeoPoint
from tools import get_config


# Links for geo coding services used by HERE API and Google API
_HERE_BASE_URL = "https://geocoder.cit.api.here.com/6.2/geocode.json"
_GOOGLE_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

# pylint: disable=too-few-public-methods
class CartographerClient(object):
    """ Performs http requests to different geocoding services """

    ADDR_QUERY_STR = "Please enter the address separated by spaces:\n"

    # Config params for traversing json data returned by the HERE API
    _HERE_LAT_LONG_CONFIG = "Response/View/Result/Location/DisplayPosition"
    _HERE_ADDR_CONFIG = "Response/View/Result/Location/Address/Label"
    _HERE_STATUS_CONFIG = "Response/View"

    # Config params for traversing json data returned by the Google API
    _GOOGLE_LAT_LONG_CONFIG = "results/geometry/location"
    _GOOGLE_ADDR_CONFIG = "results/formatted_address"
    _GOOGLE_STATUS_CONFIG = "status"

    def __init__(self):
        """
            here_app_id: (string) (for HERE API for Work customers) Your APP ID.

            here_app_code: (string) (for HERE API for Work customers) Your APP code.

            google_api_key: (string) (for Google Maps API for Work customers) Your client ID.
        """
        self.here_app_id = None
        self.here_app_code = None
        self.google_api_key = None
        self.ssl_context = None
        logger.info("Initialized geoclient")
        self.bypass_ssl_verification()

    def bypass_ssl_verification(self):
        """ Method to bypass ssl ceritficate verification """
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        logger.warn("Bypassing SSL verification")

    def request(self, url):
        """ Method to make get requests
            url: (string) URL path for making get requests

            Returns: (json) parsed json response received from the queried url
        """
        logger.info("Sending get request to %s", url)
        # Try sending a get request to the url
        try: 
            response = urllib2.urlopen(url, context=self.ssl_context)
        except urllib2.HTTPError, e:
            logger.error('HTTPError %d with reason, %s', e.code, e.reason)
            return None
        except urllib2.URLError, e:
            logger.error('URLError with reason, %s', e.reason)
            return None
        except Exception:
            import traceback
            logger.error('generic exception occurred, %s', traceback.format_exc())
            return None

        json_raw_response = response.read()

        logger.removeHandler(log_handler) # temporarily disable console logging
        logger.info("Raw response recd from server: %s", json_raw_response)
        json_data = json.loads(json_raw_response)
        logger.addHandler(log_handler) # Reenable console logging

        return json_data

    def here_geocode_service(self, address):
        """ Method to access the geocoding service by HERE
            address: (string) Address for which latitude longitudes are required. Must be space separated

            Returns: None or GeoPoint with the latitude, longitude and full address
        """
        if self.here_app_id is None or self.here_app_code is None:
            logger.error('here_app_id or here_app_code is incorrect')
            raise ValueError("Are you sure here app credentials are set")

        app_id = "?app_id=" + self.here_app_id
        app_code = "&app_code=" + self.here_app_code
        address = "&searchtext=" + address
        request_url = _HERE_BASE_URL + app_id + app_code + address
        api_response = self.request(url=request_url)
        if api_response is None:
            return None
        if get_config(api_response, self._HERE_STATUS_CONFIG):
            lat_long = get_config(api_response, self._HERE_LAT_LONG_CONFIG)
            addr = get_config(api_response, self._HERE_ADDR_CONFIG)
            pt = GeoPoint(latitude=lat_long['Latitude'], longitude=lat_long['Longitude'], address=addr)
            return pt
        logger.error('Bad request, no data received')
        return None

    def google_geocode_service(self, address):
        """ Method to access the geocoding service by Google
            address: (string) Address for which latitude longitudes are required. Must be space separated

            Returns: None or GeoPoint with the latitude, longitude and full address
        """
        if self.google_api_key is None:
            logger.error('google_api_key is incorrect')
            raise ValueError("Are you sure google api credentials are set")
            return None
        address = "?address=" + address
        request_url = _GOOGLE_BASE_URL + address
        api_response = self.request(url=request_url)
        if api_response is None:
            return None
        if get_config(api_response, self._GOOGLE_STATUS_CONFIG) == "OK":
            lat_long = get_config(api_response, self._GOOGLE_LAT_LONG_CONFIG)
            addr = get_config(api_response, self._GOOGLE_ADDR_CONFIG)
            pt = GeoPoint(latitude=lat_long['lat'], longitude=lat_long['lng'], address=addr)
            return pt
        logger.error('Bad request for google API, status received: ' + get_config(api_response, self._GOOGLE_STATUS_CONFIG))
        return None

    def get_address(self):
        """ Method to get an address from the user and parse it to the right format """
        in_addr = raw_input(self.ADDR_QUERY_STR)
        if len(in_addr) > 1:
            addr_list = in_addr.strip().split(" ")
            out_str = ""
            for word in addr_list:
                out_str = out_str + word + "+"
            logger.info("Querrying address for %s", out_str)
            return out_str
        raise ValueError("Address entered is too small, please try again")

    # Getters and setters for HERE API json config
    def get_here_lat_long_config(self):
        return self._HERE_LAT_LONG_CONFIG

    def get_here_addr_config(self):
        return self._HERE_ADDR_CONFIG

    def get_here_status_config(self):
        return self._HERE_STATUS_CONFIG

    def set_here_lat_long_config(self, config):
        logger.info("Setting here lat long config to %s", config)
        self._HERE_LAT_LONG_CONFIG = config

    def set_here_addr_config(self, config):
        logger.info("Setting here addr config to %s", config)
        self._HERE_ADDR_CONFIG = config

    def set_here_status_config(self, config):
        logger.info("Setting here status config to %s", config)
        self._HERE_STATUS_CONFIG = config

    # Getters and setters for GOOGLE API json Config
    def get_google_lat_long_config(self):
        return self._GOOGLE_LAT_LONG_CONFIG

    def get_google_addr_config(self):
        return self._GOOGLE_ADDR_CONFIG

    def get_google_status_config(self):
        return self._GOOGLE_STATUS_CONFIG

    def set_google_lat_long_config(self, config):
        logger.info("Setting google lat long config to %s", config)
        self._GOOGLE_LAT_LONG_CONFIG = config

    def set_google_addr_config(self, config):
        logger.info("Setting google addr config to %s", config)
        self._GOOGLE_ADDR_CONFIG = config

    def set_google_status_config(self, config):
        logger.info("Setting google status config to %s", config)
        self._GOOGLE_STATUS_CONFIG = config

    # Getters and Setters for HERE API credentials
    def get_here_api_creds(self):
        return [self.here_app_id, self.here_app_code]

    def set_here_api_creds(self, app_id, app_code):
        logger.info("Setting here app_id to %s and app_code to %s", app_id, app_code)
        self.here_app_id = app_id 
        self.here_app_code = app_code

    # Getters and Setters for Google API credentials
    def get_google_api_creds(self):
        return self.google_api_key

    def set_google_api_creds(self, api_key):
        logger.info("Setting google api_key to %s", api_key)
        self.google_api_key = api_key