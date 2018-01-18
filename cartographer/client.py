#
# Copyright 2017 Siddharth Srivatsa. All rights reserved.
#
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
#
# Author: Siddharth Srivatsa <srivatsasiddharth@gmail.com>, 1/2018

"""
Core client functionality, common across all API requests (including performing
HTTP requests).
"""
glob_data = {u'Response': {u'MetaInfo': {u'Timestamp': u'2018-01-17T06:35:39.578+0000'},
  u'View': [{u'Result': [{u'Location': {u'Address': {u'AdditionalData': [{u'key': u'CountryName',
          u'value': u'United States'},
         {u'key': u'StateName', u'value': u'Texas'},
         {u'key': u'CountyName', u'value': u'Harris'},
         {u'key': u'PostalCodeType', u'value': u'N'}],
        u'City': u'Houston',
        u'Country': u'USA',
        u'County': u'Harris',
        u'District': u'Neartown/Montrose',
        u'HouseNumber': u'3618',
        u'Label': u'3618 Garrott St, Houston, TX 77006, United States',
        u'PostalCode': u'77006',
        u'State': u'TX',
        u'Street': u'Garrott St'},
       u'DisplayPosition': {u'Latitude': 29.74001, u'Longitude': -95.3856799},
       u'LocationId': u'NT_rWcK0AV22v7yQdh4RPXl-A_zYTM4A',
       u'LocationType': u'point',
       u'MapView': {u'BottomRight': {u'Latitude': 29.7388858,
         u'Longitude': -95.3843852},
        u'TopLeft': {u'Latitude': 29.7411342, u'Longitude': -95.3869746}},
       u'NavigationPosition': [{u'Latitude': 29.74001,
         u'Longitude': -95.38546}]},
      u'MatchLevel': u'houseNumber',
      u'MatchQuality': {u'City': 1.0, u'HouseNumber': 1.0, u'Street': [1.0]},
      u'MatchType': u'pointAddress',
      u'Relevance': 1.0}],
    u'ViewId': 0,
    u'_type': u'SearchResultsViewType'}]}}

########################################################
# Here  API credentials - 
# App ID=SXlp6ZNY2WbxLZA2KK9c
# App Code=zYyz6W7wkgMHhaKuxHQO-w

# Google API credentials -
# API key=AIzaSyCkGMOjHINaKqBGFqhjRsxrjoWgAsC5cuI
########################################################


import json
import logging
import ssl
import urllib2
from geo_point import GeoPoint
from tools import get_config


logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s', filename='log/carographer.log', level=logging.INFO)


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

    def __init__(self, here_app_id, here_app_code, google_api_key, timeout=None):
        """
            :param here_app_id: (for HERE API for Work customers) Your APP ID.
            :type here_app_id: string

            :param here_app_code: (for Maps API for Work customers) Your APP code.
            :type here_app_id: string

            :param google_api_key: (for Google Maps API for Work customers) Your client ID.
            :type google_api_key: string

            :param timeout: Timeout period for http requests in seconds.
                Specify "None" for no timeout
            :type timeout: int

        """
        if not (here_app_id and here_app_code):
            raise ValueError("Must provide a HERE app id and key or enterprise credentials "
                             "for the HERE API when creating client")

        if not google_api_key:
            raise ValueError("Must provide a Google API key or enterprise credentials for "
                             "the Google API when creating client")

        self.here_app_id = here_app_id
        self.here_app_code = here_app_code
        self.google_api_key = google_api_key
        self.timeout = timeout
        self.ssl_context = None
        logging.info("Initialized geoclient with here_app_id %s, here_app_code %s and google_api_key %s", here_app_id, here_app_code, google_api_key)
        self.bypass_ssl_verification()

    def bypass_ssl_verification(self):
        """ Method to bypass ssl ceritficate verification """
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        logging.warn("Bypassing SSL verification")

    def request(self, url):
        """ Method to make get requests
            :param url: URL path for making get requests
            :type url: string

            :rtype: json
        """
        logging.info("Sending get request to %s", url)
        try: 
            response = urllib2.urlopen(url, context=self.ssl_context)
        except urllib2.HTTPError, e:
            logging.error('HTTPError %d with reason %s', e.code, e.reason)
            return None
        except urllib2.URLError, e:
            logging.error('URLError with reason %s', e.reason)
            return None
        except Exception:
            import traceback
            logging.error('generic exception occurred, %s', traceback.format_exc())
            return None
        json_raw_response = response.read()
        logger.info("Raw response recd from server: %s", json_raw_response)
        json_data = json.loads(json_raw_response)
        logger.info("JSON response recd from API: %s", json_data)
        return json_data

    def here_geocode_service(self, address):
        """ Method to access the geocoding service by HERE
            :param address: Address for which latitude longitudes are required. Must be space separated
            :type string

            :rtype: GeoPoint or None
        """
        app_id = "?app_id=" + self.here_app_id
        app_code = "&app_code=" + self.here_app_code
        address = "&searchtext=" + address
        request_url = _HERE_BASE_URL + app_id + app_code + address
        api_response = self.request(url=request_url)
        # print("api_response: ", api_response)
        # TODO: Add checker for status
        api_response = glob_data  # {
        # u'Response': {
        #     u'View': [], 
        #     u'MetaInfo': {
        #         u'Timestamp': u'2018-01-17T19:17:20.606+0000'}
        #     }
        # }  # 
        get_config(api_response, self._HERE_STATUS_CONFIG)
        if get_config(api_response, self._HERE_STATUS_CONFIG):
            lat_long = get_config(api_response, self._HERE_LAT_LONG_CONFIG)
            addr = get_config(api_response, self._HERE_ADDR_CONFIG)
            pt = GeoPoint(latitude=lat_long['Latitude'], longitude=lat_long['Longitude'], address=addr)
            return pt
        Logger.error('Bad request, no data received')
        return None

    def google_geocode_service(self, address):
        """ Method to access the geocoding service by Google
            :param address: Address for which latitude longitudes are required. Must be space separated
            :type string

            :rtype: GeoPoint or None
        """
        address = "?address=" + address
        request_url = _GOOGLE_BASE_URL + address
        api_response = self.request(url=request_url)
        print("api_response: ", api_response)
        # api_response = glob_data
        if get_config(api_response, self._GOOGLE_STATUS_CONFIG) == "OK":
            lat_long = get_config(api_response, self._GOOGLE_LAT_LONG_CONFIG)
            addr = get_config(api_response, self._GOOGLE_ADDR_CONFIG)
            pt = GeoPoint(latitude=lat_long['lat'], longitude=lat_long['lng'], address=addr)
            return pt
        Logger.error('Bad request for google API, status received: ' + get_config(api_response, self._GOOGLE_STATUS_CONFIG))

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
    def get_here_lat_long_config():
        return self._HERE_LAT_LONG_CONFIG

    def get_here_addr_config():
        return self._HERE_ADDR_CONFIG

    def get_here_status_config():
        return self._HERE_STATUS_CONFIG

    def set_here_lat_long_config(config):
        self._HERE_LAT_LONG_CONFIG = config

    def set_here_addr_config(config):
        self._HERE_ADDR_CONFIG = config

    def set_here_status_config(config):
        self._HERE_STATUS_CONFIG = config


    # Getters and setters for GOOGLE API json Config
    def get_google_lat_long_config():
        return self._GOOGLE_LAT_LONG_CONFIG

    def get_google_addr_config():
        return self._GOOGLE_ADDR_CONFIG

    def get_google_status_config():
        return self._GOOGLE_STATUS_CONFIG

    def set_google_lat_long_config(config):
        self._GOOGLE_LAT_LONG_CONFIG = config

    def set_google_addr_config(config):
        self._GOOGLE_ADDR_CONFIG = config

    def set_google_status_config(config):
        self._GOOGLE_STATUS_CONFIG = config

    # Getters and Setters for HERE API credentials
    def get_here_api_creds():
        return [self.here_app_id, self.here_app_code]

    def set_here_api_creds(app_id, app_code):
        self.here_app_id = app_id 
        self.here_app_code = app_code

    # Getters and Setters for Google API credentials
    def set_google_api_creds(api_key):
        self.google_api_key = api_key

    def get_google_api_creds():
        return self.google_api_key


if __name__ == '__main__':
    client = CartographerClient(here_app_id="SXlp6ZNY2WbfxLZA2KK9c", here_app_code="zYyz6W7wkgfMHhaKuxHQO-w", google_api_key="AIzaSyCkGMOjHINaKqBGFqhjRsxrjoWgAsC5cuI")
    addr = client.get_address()
    # g_data = client.google_geocode_service(address=addr)
    # print(g_data)
    g_data = client.here_geocode_service(address=addr)
    g_data.output_values()
    # lat_long = geo_data["results"][0]["geometry"]["location"] #["results"]["geometry"]["location"]
    # print lat_long
    # print type(lat_long)
