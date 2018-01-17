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

class GeoPoint():

	def __init__(self, latitude, longitude, address):
		self.lat = latitude
		self.long = longitude
		self.address = address

	def output_values(self):
		print 'address: ', self.address
		print 'lat: ', self.lat
		print 'long: ', self.long
