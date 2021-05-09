import base64
import json
import os
import uuid

import yaml
from django.http import JsonResponse
from rest_framework.decorators import api_view

from sample.settings import BASE_DIR
from utils.cluster import Cluster
from utils.kubernetes_operation import Kubernetes_Operations
from utils.miscellaneous_operations import dump_to_yaml, key_validations, get_cluster_from_cluster_id, \
    get_yaml_from_uuid_id


@api_view(['GET'])
def health_check(request):
    """
    This API will be used to get health status of the application
    """
    response = {"is_successful": True}
    return JsonResponse(response, safe=False)


@api_view(['POST'])
def create_yaml(request):
    """
    This API will fetch the data from request and save the information in a yaml file.
    """
    json_response = {
        'is_successful': False,
        'error': '',
        'uuid_for_yaml': None
    }
    try:
        json_request = json.loads(request.body)
        valid_json_keys = ['image_repository', 'image_tag']
        # key validations
        error_key_validations, response_key_validations = key_validations(
            json_request, valid_json_keys)
        if not error_key_validations:
            image_repository = json_request.get("image_repository")
            image_tag = json_request.get("image_tag")
            file_path_for_mongodb_deploy_values = os.path.join(BASE_DIR, "dependency", "mongodb_cr.yaml")

            with open(file_path_for_mongodb_deploy_values) as file:

                yaml.preserve_quotes = True
                mongodb_deploy_values = yaml.load(file, Loader=yaml.FullLoader)

            mongodb_deploy_values.get('spec').update({'ImageRepository': image_repository,
                                                 'ImageTag': image_tag})

            uuid_for_yaml = str(uuid.uuid4())
            error_dump_to_yaml, response_dump_to_yaml = dump_to_yaml(uuid_for_yaml, mongodb_deploy_values)
            if error_dump_to_yaml:
                raise Exception(response_dump_to_yaml)
            else:
                json_response.update({'is_successful': True,
                                      'uuid_for_yaml': uuid_for_yaml})
        else:
            raise Exception(response_key_validations.get('error'))
    except Exception as e:
        json_response.update({
            'error': str(e),
        })
    finally:
        return JsonResponse(data=json_response, safe=False)


@api_view(['POST'])
def add_cluster(request):
    """
    add kubernetes cluster
    :param request:
    :return:
    """
    json_response = {'is_successful': False,
                     'cluster_id': None,
                     'error': None}
    try:
        json_request = json.loads(request.body)
        valid_json_keys = ['cluster_config']
        # key validations
        error_key_validations, response_key_validations = key_validations(
            json_request, valid_json_keys)
        if error_key_validations:
            json_response.update({
                'error': response_key_validations.get('error')
            })
        else:
            cluster_config_json_request = json_request.get('cluster_config')

            if "b'" in json_request.get('cluster_config')[0:2]:
                length = len(str(json_request.get('cluster_config')))
                # stripping the text with initial b' and '
                cluster_config_json_request = str(json_request.get('cluster_config'))[2:length - 1]
            cluster_config = base64.b64decode(cluster_config_json_request)
            cluster = Cluster(cluster_config=cluster_config)
            error_add_cluster, response_add_cluster = cluster.add_cluster()
            if not error_add_cluster:
                json_response.update({
                    "is_successful": True,
                    "cluster_id": response_add_cluster
                })
            else:
                raise Exception(response_add_cluster)
    except Exception as e:
        json_response.update({
            'error': str(e)
        })
    finally:
        return JsonResponse(json_response, safe=False)


@api_view(['POST'])
def deploy_operator_resources(request):
    """
    Deploy on kubernetes cluster
    :param request:
    :return:
    """
    json_response = {
        'is_successful': False,
        'error': ''
    }
    try:
        json_request = json.loads(request.body)
        valid_json_keys = ['cluster_id']
        # key validations
        error_key_validations, response_key_validations = key_validations(
            json_request, valid_json_keys)
        if not error_key_validations:
            cluster_id = json_request.get("cluster_id")

            error_get_cluster_from_cluster_id, response_get_cluster_from_cluster_id = get_cluster_from_cluster_id(
                cluster_id)
            if not error_get_cluster_from_cluster_id:
                k8s_obj = Kubernetes_Operations(configuration_yaml=response_get_cluster_from_cluster_id)

                error_create_operator_resources, response_create_operator_resources = k8s_obj. \
                    create_operator_resources()
                if error_create_operator_resources:
                    raise Exception(response_create_operator_resources)
                elif len(response_create_operator_resources) != 11:
                    raise Exception("Not deployed resources properly")
                else:
                    json_response.update({
                        'is_successful': True,
                    })
            else:
                raise Exception(response_get_cluster_from_cluster_id)
        else:
            raise Exception(response_key_validations.get('error'))
    except Exception as e:
        json_response.update({
            'error': str(e),
        })
    finally:
        return JsonResponse(data=json_response, safe=False)


@api_view(['POST'])
def deploy_resources(request):
    """
    Deploy on kubernetes cluster
    :param request:
    :return:
    """
    json_response = {
        'is_successful': False,
        'error': ''
    }
    try:
        json_request = json.loads(request.body)
        valid_json_keys = ['uuid_for_yaml', 'cluster_id']
        # key validations
        error_key_validations, response_key_validations = key_validations(
            json_request, valid_json_keys)
        if not error_key_validations:
            uuid_for_yaml = json_request.get("uuid_for_yaml")
            cluster_id = json_request.get("cluster_id")

            error_get_cluster_from_cluster_id, response_get_cluster_from_cluster_id = get_cluster_from_cluster_id(
                cluster_id)
            if not error_get_cluster_from_cluster_id:
                error_get_yaml_from_uuid_id, response_get_yaml_from_uuid_id = get_yaml_from_uuid_id(uuid_for_yaml)
                if not error_get_yaml_from_uuid_id:
                    k8s_obj = Kubernetes_Operations(configuration_yaml=response_get_cluster_from_cluster_id)
                    error_create_resource, response_create_resource = k8s_obj.create_resource(
                        response_get_yaml_from_uuid_id)
                    if error_create_resource:
                        raise Exception(response_create_resource)
                    else:
                        json_response.update({
                            'is_successful': True,
                        })
                else:
                    raise Exception(response_get_yaml_from_uuid_id)
            else:
                raise Exception(response_get_cluster_from_cluster_id)
        else:
            raise Exception(response_key_validations.get('error'))
    except Exception as e:
        json_response.update({
            'error': str(e),
        })
    finally:
        return JsonResponse(data=json_response, safe=False)


@api_view(['DELETE'])
def delete_resource(request):
    """
    Delete from kubernetes cluster
    :param request:
    :return:
    """
    json_response = {
        'is_successful': False,
        'error': ''
    }
    try:
        json_request = json.loads(request.body)
        valid_json_keys = ['cluster_id']
        # key validations
        error_key_validations, response_key_validations = key_validations(
            json_request, valid_json_keys)
        if not error_key_validations:

            cluster_id = json_request.get("cluster_id")

            error_get_cluster_from_cluster_id, response_get_cluster_from_cluster_id = get_cluster_from_cluster_id(
                cluster_id)
            if not error_get_cluster_from_cluster_id:
                k8s_obj = Kubernetes_Operations(configuration_yaml=response_get_cluster_from_cluster_id)

                error_delete_resource, response_delete_resource = k8s_obj.delete_resource()
                if error_delete_resource:
                    raise Exception(response_delete_resource)
                else:
                    json_response.update({
                        'is_successful': True,
                    })
            else:
                raise Exception(response_get_cluster_from_cluster_id)
        else:
            raise Exception(response_key_validations.get('error'))
    except Exception as e:
        json_response.update({
            'error': str(e),
        })
    finally:
        return JsonResponse(data=json_response, safe=False)


@api_view(['DELETE'])
def delete_operator_resources(request):
    """
    Delete from kubernetes cluster
    :param request:
    :return:
    """
    json_response = {
        'is_successful': False,
        'error': ''
    }
    try:
        json_request = json.loads(request.body)
        valid_json_keys = ['cluster_id']
        # key validations
        error_key_validations, response_key_validations = key_validations(
            json_request, valid_json_keys)
        if not error_key_validations:

            cluster_id = json_request.get("cluster_id")

            error_get_cluster_from_cluster_id, response_get_cluster_from_cluster_id = get_cluster_from_cluster_id(
                cluster_id)
            if not error_get_cluster_from_cluster_id:
                k8s_obj = Kubernetes_Operations(configuration_yaml=response_get_cluster_from_cluster_id)

                error_delete_operator_resources, response_delete_operator_resources = k8s_obj. \
                    delete_operator_resources()
                if error_delete_operator_resources:
                    raise Exception(response_delete_operator_resources)
                else:
                    json_response.update({
                        'is_successful': True,
                    })
            else:
                raise Exception(response_get_cluster_from_cluster_id)
        else:
            raise Exception(response_key_validations.get('error'))
    except Exception as e:
        json_response.update({
            'error': str(e),
        })
    finally:
        return JsonResponse(data=json_response, safe=False)
