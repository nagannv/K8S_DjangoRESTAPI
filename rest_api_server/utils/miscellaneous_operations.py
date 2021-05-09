import json
import os

import yaml

from sample.settings import BASE_DIR

yaml_dumps_path = os.path.join(BASE_DIR, 'yaml_dumps')
config_dumps_path = os.path.join(BASE_DIR, 'config_dumps')


def dump_to_yaml(uuid_for_yaml, data_to_dump):
    error = True
    response = None

    try:
        path = os.path.join(yaml_dumps_path, uuid_for_yaml)
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path, 'cr.yaml')
        if not os.path.exists(path):
            with open(path, 'w+') as outfile:
                yaml.dump(data_to_dump, outfile)
        error = False
    except Exception as e:
        response = str(e)
    finally:
        return error, response


def get_yaml_from_uuid_id(uuid_for_yaml):
    error = True
    response = None
    try:
        path = os.path.join(yaml_dumps_path, uuid_for_yaml)
        if not os.path.exists(path):
            raise Exception('Invalid uuid_for_yaml')
        path = os.path.join(path, 'cr.yaml')
        response = path
        error = False
    except Exception as e:
        response = str(e)
    finally:
        return error, response


def key_validations(request_keys, validation_keys):
    """
    validate the keys from request parameter
    :param request_keys: keys received from request which need to validate
    :param validation_keys: referenced keys for validation
    :return:
    """
    response = {}
    missing_key_flag = False
    missing_value_flag = False
    try:
        missing_keys = []
        missing_values = []
        for key in validation_keys:
            if key not in request_keys:
                missing_key_flag = True
                missing_keys.append(key)
            elif key in ['provider_id', 'user_id', 'webhook_id']:
                # checking the type of value is int only
                if not isinstance(request_keys.get(key), int):
                    missing_value_flag = True
                    missing_values.append(key)

        if missing_key_flag or missing_value_flag:
            response = {
                'error':
                    {
                        'message': 'Following keys and/or values are missing in request parameter or value type is invalid.',
                        'keys_info': {
                            'keys': missing_keys,
                            'values': missing_values,
                        }
                    }
            }
            if len(missing_keys) == 0 and len(missing_values) == 0:
                response.get('error').get('keys_info').update({'keys': []})
                response.get('error').get('keys_info').update({'values': []})
            elif len(missing_keys) == 0:
                response.get('error').get('keys_info').update({'keys': []})
            elif len(missing_keys) == 0:
                response.get('error').get('missing').update({'values': []})
    except Exception as e:
        error = True
        response.update({
            'message': str(e)
        })
        print(e)
    finally:
        if len(response) == 0:
            # return error=False if response is empty
            error = False
            return error, response
        else:
            # return error=True if response is not empty
            error = True
            return error, response


def create_cluster_config_file(cluster_id, config_details):
    """
    create the folder for the config file of kubernetes cluster with its id as a directory name
    :param cluster_id:
    :param config_details:
    :return:
    """
    error = True
    response = None
    try:
        path = os.path.join(config_dumps_path, cluster_id)
        if not os.path.exists(path):
            os.makedirs(path)
        path = os.path.join(path, 'config')
        if not os.path.exists(path):
            with open(path, 'w+') as outfile:
                json.dump(config_details, outfile)
        error = False
    except Exception as e:
        response = str(e)
    finally:
        return error, response


def get_cluster_from_cluster_id(cluster_id):
    error = True
    response = None
    try:
        path = os.path.join(config_dumps_path, cluster_id)
        if not os.path.exists(path):
            raise Exception('Invalid cluster_id')
        path = os.path.join(path, 'config')
        response = path
        error = False
    except Exception as e:
        response = str(e)
    finally:
        return error, response
