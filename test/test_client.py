#!/usr/bin/python
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

""" Tests for the client module """


import unittest
from cartographer import CartographerClient

addr = "3451 Walnut Street Philadelphia"

class ClientTest(unittest.TestCase):
    """ Test suite for testing the client"""

    def test_empty_url_request(self):
        """ Test if client raises an exception for an empty url  """
        with self.assertRaises(Exception):
            client = CartographerClient()
            client.request()
        print"Client requested url"

    def test_google_cred_not_set(self):
        """ Test if google credentials are not set """
        client = CartographerClient()
        self.assertIsNone(client.google_geocode_service(addr))

    def test_here_cred_not_set(self):
        """ Test if here credentials are not set """
        client = CartographerClient()
        self.assertIsNone(client.here_geocode_service(addr))

    def test_incorrect_url(self):
        """ Test if the client can handle an incorrect url """
        client = CartographerClient()
        self.assertIsNone(client.request("https://www.google.com/"))

    def test_invalid_url(self):
        """ Test if the client can handle an invalid url """
        client = CartographerClient()
        self.assertIsNone(client.request("http://www.siddisthegreatestintheworld.com/"))
