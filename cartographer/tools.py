


def get_config(raw_json_data, param_path):
    """ Traverse json data to get required field
        :param raw_json_data: Json data which contains the parameter value that should be unpacked
        :type json

        :param param_path: Parameter path in the json data for which the value needs to extracted
        :type: string
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
        # Logger.error("Key not found in response")
        return None