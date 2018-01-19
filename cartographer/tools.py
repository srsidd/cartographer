#!/usr/bin/python
import logging
logger = logging.getLogger(__name__)

def get_config(raw_json_data, param_path):
    """ Traverse json data to get required field
        raw_json_data: (json) Json data which contains the parameter value that should be unpacked
        

        param_path: (string) Parameter path in the json data for which the value needs to extracted
    """
    config_params = param_path.split('/')

    if len(config_params[0]) == 0:  # Drop leading '/'
        config_params = config_params[1:]
    # recurse nested dictionaries
    def traverse(config_file, config_param):
        if isinstance(config_file, list):
            config_file = config_file[0]  # If type is list
        if len(config_param) > 1:
            return traverse(config_file[config_param[0]], config_param[1:])
        return config_file[config_param[0]]
    try:
        return traverse(raw_json_data, config_params)
    except KeyError:
        logger.error("Key not found in response")
        return None