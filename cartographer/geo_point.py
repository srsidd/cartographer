#
#
# Author: Siddharth Srivatsa <srivatsasiddharth@gmail.com>, 1/2018
import logging 

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_handler = logging.StreamHandler()
log_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))
logger.addHandler(log_handler)

class GeoPoint():

    def __init__(self, latitude, longitude, address):
        self.lat = latitude
        self.long = longitude
        self.address = address

    def output_values(self):
        logger.info("Address: %s", self.address)
        logger.info("Latitude: %s", self.lat)
        logger.info("Longitude: %s", self.long)
