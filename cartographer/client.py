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

########################################################
# Here  API credentials - 
# App ID=SXlp6ZNY2WbxLZA2KK9c
# App Code=zYyz6W7wkgMHhaKuxHQO-w

# Google API credentials -
# API key=AIzaSyCkGMOjHINaKqBGFqhjRsxrjoWgAsC5cuI
########################################################


import json
import ssl
import urllib2

# Links for geo coding services used by HERE API and Google API
_HERE_BASE_URL = "https://geocoder.cit.api.here.com/6.2/geocode.json"
_GOOGLE_BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

class CartographerClient(object):
    """ Performs http requests to different geocoding services """

    ADDR_QUERY_STR = "Please enter the address separated by spaces: "


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
        self.bypass_ssl_verification()

    def bypass_ssl_verification(self):
        """ Method to bypass ssl ceritficate verification """
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE

    def request(self, url):
        """ Method to make get requests
            :param url: URL path for making get requests
            :type url: string

            :rtype: json
        """
        print("Querrying: ", url)
        try: 
            response = urllib2.urlopen(url, context=self.ssl_context)
        except urllib2.HTTPError, e:
            # Logger.error('HTTPError = ' + str(e.code))
            print('HTTPError = ' + str(e.code) + ' ' + str(e.reason))
            return None
        except urllib2.URLError, e:
            # Logger.error('URLError = ' + str(e.reason))
            print('URLError = ' + str(e.reason))
            return None
        except Exception:
            import traceback
            # Logger.error('generic exception: ' + traceback.format_exc())
            print('generic exception: ' + traceback.format_exc())
            return None
        json_raw_response = response.read()
        json_data = json.loads(json_raw_response)
        return json_data
