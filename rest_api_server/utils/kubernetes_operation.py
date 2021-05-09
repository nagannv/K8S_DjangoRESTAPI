import json
import os
from os import path

import yaml
from kubernetes import client, utils
from kubernetes.client import Configuration, ApiException
from kubernetes.config import kube_config
from kubernetes.utils import FailToCreateError
from urllib3.exceptions import MaxRetryError
from yaml.scanner import ScannerError

from sample.settings import BASE_DIR


class Kubernetes_Operations(object):
    def __init__(self, configuration_yaml):
        """
        construtor for kubernetes operation class
        :param configuration_yaml:
        """
        self.configuration_yaml = configuration_yaml
        self._configuration_yaml = None

    @property
    def config(self):
        with open(self.configuration_yaml, 'r') as f:
            if self._configuration_yaml is None:
                yaml.warnings({'YAMLLoadWarning': False})
                self._configuration_yaml = yaml.load(f, Loader=yaml.FullLoader)
        return self._configuration_yaml

    @property
    def client(self):
        """
        client of kubernetes
        :return:
        """
        k8_loader = kube_config.KubeConfigLoader(self.config)
        call_config = type.__call__(Configuration)
        k8_loader.load_and_set(call_config)
        Configuration.set_default(call_config)
        return client

    @property
    def clientCoreV1(self):
        """
        client core method of kubernetes
        :return:
        """
        k8_loader = kube_config.KubeConfigLoader(self.config)
        call_config = type.__call__(Configuration)
        k8_loader.load_and_set(call_config)
        Configuration.set_default(call_config)
        return client.CoreV1Api()

    @property
    def clientAppsV1(self):
        """
        client Apps for kubernetes apps
        :return:
        """
        k8_loader = kube_config.KubeConfigLoader(self.config)
        call_config = type.__call__(Configuration)
        k8_loader.load_and_set(call_config)
        Configuration.set_default(call_config)
        return client.AppsV1Api()

    def create_operator_resources(self):
        """
        Creates a new app on kubernetes cluster using data
        :param cluster_id:
        :param data:
        :return:
        """

        response = None
        error = False
        created_app_list = []
        try:
            yaml_file_list_to_deploy = ['custom-resource-definition.yaml',
                                        'namespace.yaml',
                                        'leader-election-role.yaml',
                                        'cluster-role-manager-role.yaml',
                                        'cluster-role-metrics-reader.yaml',
                                        'cluster-role-proxy-role.yaml',
                                        'leader-election-rolebinding.yaml',
                                        'manager-rolebinding.yaml',
                                        'proxy-rolebinding.yaml',
                                        'controller-manager-metrics-service.yaml',
                                        'deployment.yaml']

            for file_path in yaml_file_list_to_deploy:
                yaml_file_path = os.path.join(BASE_DIR, 'dependency', 'mongodb-template', file_path)

                kube_loader = kube_config.KubeConfigLoader(self.config)
                call_config = type.__call__(Configuration)
                try:
                    kube_loader.load_and_set(call_config)
                except Exception:
                    # If cluster is unavailable or unreachable.
                    raise Exception('Cluster is unreachable')
                Configuration.set_default(call_config)
                kube_client = client.api_client.ApiClient()
                # kubernetes client object
                exception = None
                flag = False
                try:
                    # App creation on kubernetes cluster
                    utils.create_from_yaml(k8s_client=kube_client, yaml_file=yaml_file_path)
                    flag = True
                except Exception as e:
                    exception = e
                    flag = False
                if flag:
                    # if provided yaml or json is valid
                    with open(path.abspath(yaml_file_path)) as file:
                        yml_document_all = yaml.safe_load_all(file)

                        for yml_document in yml_document_all:
                            if 'List' in yml_document.get('kind'):
                                for yml_object in yml_document.get('items'):
                                    created_app_list.append({
                                        'name': yml_object.get('metadata').get('name'),
                                        'kind': yml_document.get('kind')
                                    })
                            else:
                                created_app_list.append({
                                    'name': yml_document.get('metadata').get('name'),
                                    'kind': yml_document.get('kind')
                                })

                            error = False

                else:
                    # if provided yaml or json is invalid
                    error = True
                    try:

                        if isinstance(exception, KeyError):
                            response = 'Key is missing %s' % str(exception)
                        elif isinstance(exception, TypeError):
                            response = 'Invalid YAML/JSON provided'
                        elif isinstance(exception, ValueError):
                            response = 'Value is missing %s' % str(exception)
                        elif isinstance(exception, FailToCreateError):
                            # response_dict.update({'error': e.api_exceptions})
                            api_exception_list = exception.api_exceptions
                            failed_object = ''
                            for api_exceptions in api_exception_list:
                                json_error_body = json.loads(api_exceptions.body)
                                if 'message' in json_error_body:
                                    if 'not found' in json_error_body.get('message'):
                                        failed_object = str(json_error_body.get('message'))
                                        failed_object = failed_object.replace('"', '')
                                    elif 'already exists' in json_error_body.get('message'):
                                        failed_object = str(json_error_body.get('message'))
                                        failed_object = failed_object.replace('"', '')
                                    else:
                                        failed_object = str(json_error_body.get('message'))
                                        failed_object = failed_object.replace('"', '')
                            response = failed_object
                        elif isinstance(exception, ScannerError):
                            response = 'Invalid yaml/json'
                        elif isinstance(exception, MaxRetryError):
                            response = 'Cluster is not available'
                        else:
                            response = str(exception)
                    except Exception as e:
                        response = str(e)
            response = created_app_list
        except Exception as e:
            error = True
            response = str(e)
            print(str(e))
        finally:
            return error, response

    def create_resource(self, file_path):
        """
        Creates a new app on kubernetes cluster using data
        :param file_path:
        :return:
        """

        response = None
        error = False
        created_app_list = []
        try:
            yaml_file_path = os.path.join(BASE_DIR, 'dependency', file_path)
            custom_resource_yaml_data = None
            with open(yaml_file_path, 'r+') as input_file:
                custom_resource_yaml_data = yaml.safe_load(input_file)
            if custom_resource_yaml_data is not None:
                kube_loader = kube_config.KubeConfigLoader(self.config)
                call_config = type.__call__(Configuration)
                try:
                    kube_loader.load_and_set(call_config)
                except Exception:
                    # If cluster is unavailable or unreachable.
                    raise Exception('Cluster is unreachable')
                Configuration.set_default(call_config)
                kube_client = client.CustomObjectsApi()
                # kubernetes client object
                exception = None
                flag = False
                try:
                    # App creation on kubernetes cluster
                    kube_client.create_namespaced_custom_object(
                        group="mongo.mytest",
                        namespace="default",
                        version="v1alpha1",
                        plural="mongodbs",
                        body=custom_resource_yaml_data,
                    )
                    flag = True
                except Exception as e:
                    exception = e
                    flag = False
                if flag:
                    # if provided yaml or json is valid
                    with open(path.abspath(yaml_file_path)) as file:
                        yml_document_all = yaml.safe_load_all(file)

                        for yml_document in yml_document_all:
                            if 'List' in yml_document.get('kind'):
                                for yml_object in yml_document.get('items'):
                                    created_app_list.append({
                                        'name': yml_object.get('metadata').get('name'),
                                        'kind': yml_document.get('kind')
                                    })
                            else:
                                created_app_list.append({
                                    'name': yml_document.get('metadata').get('name'),
                                    'kind': yml_document.get('kind')
                                })
                            error = False

                else:
                    # if provided yaml or json is invalid
                    error = True
                    try:

                        if isinstance(exception, KeyError):
                            response = 'Key is missing %s' % str(exception)
                        elif isinstance(exception, TypeError):
                            response = 'Invalid YAML/JSON provided'
                        elif isinstance(exception, ValueError):
                            response = 'Value is missing %s' % str(exception)
                        elif isinstance(exception, FailToCreateError):
                            # response_dict.update({'error': e.api_exceptions})
                            api_exception_list = exception.api_exceptions
                            failed_object = ''
                            for api_exceptions in api_exception_list:
                                json_error_body = json.loads(api_exceptions.body)
                                if 'message' in json_error_body:
                                    if 'not found' in json_error_body.get('message'):
                                        failed_object = str(json_error_body.get('message'))
                                        failed_object = failed_object.replace('"', '')
                                    elif 'already exists' in json_error_body.get('message'):
                                        failed_object = str(json_error_body.get('message'))
                                        failed_object = failed_object.replace('"', '')
                                    else:
                                        failed_object = str(json_error_body.get('message'))
                                        failed_object = failed_object.replace('"', '')
                            response = failed_object
                        elif isinstance(exception, ScannerError):
                            response = 'Invalid yaml/json'
                        elif isinstance(exception, MaxRetryError):
                            response = 'Cluster is not available'
                        else:
                            response = str(exception)
                    except Exception as e:
                        response = str(e)
            else:
                raise Exception('Unable to parse the custom resource yaml file')
        except Exception as e:
            error = True
            response = str(e)
            print(str(e))
        finally:
            return error, response

    def patch_k8s_objects(self, file_path):
        """
        Patches a new app on kubernetes cluster using data
        :param cluster_id:
        :param data:
        :return:
        """

        response = None
        error = False
        patched_app_list = []
        try:
            yaml_file_path = os.path.join(BASE_DIR, 'dependency', file_path)
            custom_resource_yaml_data = None
            with open(yaml_file_path, 'r+') as input_file:
                custom_resource_yaml_data = yaml.safe_load(input_file)
            if custom_resource_yaml_data is not None:
                kube_loader = kube_config.KubeConfigLoader(self.config)
                call_config = type.__call__(Configuration)
                try:
                    kube_loader.load_and_set(call_config)
                except Exception:
                    # If cluster is unavailable or unreachable.
                    raise Exception('Cluster is unreachable')
                Configuration.set_default(call_config)
                kube_client = client.CustomObjectsApi()
                # kubernetes client object
                exception = None
                flag = False
                try:
                    # App creation on kubernetes cluster
                    apiVersion = str(custom_resource_yaml_data.get("apiVersion")).split("/")
                    kube_client.patch_namespaced_custom_object(
                        group=apiVersion[0],
                        version=apiVersion[1],
                        namespace="default",
                        plural="mongodbs",
                        body=custom_resource_yaml_data,
                        name=str(custom_resource_yaml_data.get("metadata").get("name"))
                    )
                    flag = True
                except Exception as e:
                    exception = e
                    flag = False
                if flag:
                    # if provided yaml or json is valid
                    with open(path.abspath(yaml_file_path)) as file:
                        yml_document_all = yaml.safe_load_all(file)

                        for yml_document in yml_document_all:
                            if 'List' in yml_document.get('kind'):
                                for yml_object in yml_document.get('items'):
                                    patched_app_list.append({
                                        'name': yml_object.get('metadata').get('name'),
                                        'kind': yml_document.get('kind')
                                    })
                            else:
                                patched_app_list.append({
                                    'name': yml_document.get('metadata').get('name'),
                                    'kind': yml_document.get('kind')
                                })
                            error = False

                else:
                    # if provided yaml or json is invalid
                    error = True
                    try:

                        if isinstance(exception, KeyError):
                            response = 'Key is missing %s' % str(exception)
                        elif isinstance(exception, TypeError):
                            response = 'Invalid YAML/JSON provided'
                        elif isinstance(exception, ValueError):
                            response = 'Value is missing %s' % str(exception)
                        elif isinstance(exception, FailToCreateError):
                            # response_dict.update({'error': e.api_exceptions})
                            api_exception_list = exception.api_exceptions
                            failed_object = ''
                            for api_exceptions in api_exception_list:
                                json_error_body = json.loads(api_exceptions.body)
                                if 'message' in json_error_body:
                                    if 'not found' in json_error_body.get('message'):
                                        failed_object = str(json_error_body.get('message'))
                                        failed_object = failed_object.replace('"', '')
                                    elif 'already exists' in json_error_body.get('message'):
                                        failed_object = str(json_error_body.get('message'))
                                        failed_object = failed_object.replace('"', '')
                                    else:
                                        failed_object = str(json_error_body.get('message'))
                                        failed_object = failed_object.replace('"', '')
                            response = failed_object
                        elif isinstance(exception, ScannerError):
                            response = 'Invalid yaml/json'
                        elif isinstance(exception, MaxRetryError):
                            response = 'Cluster is not available'
                        else:
                            response = str(exception)
                    except Exception as e:
                        response = str(e)
            else:
                raise Exception('Unable to parse the custom resource yaml file')
            response = patched_app_list
        except Exception as e:
            error = True
            response = str(e)
            print(str(e))
        finally:
            return error, response

    def delete_resource(self):
        """
        Delete a new app on kubernetes cluster using data
        :return:
        """

        response = None
        error = True
        try:
            kube_loader = kube_config.KubeConfigLoader(self.config)
            call_config = type.__call__(Configuration)
            try:
                kube_loader.load_and_set(call_config)
            except Exception:
                # If cluster is unavailable or unreachable.
                raise Exception('Cluster is unreachable')
            Configuration.set_default(call_config)
            kube_client = client.CustomObjectsApi()
            # kubernetes client object
            try:
                # App creation on kubernetes cluster
                kube_client.delete_namespaced_custom_object(
                    group="mongo.mytest",
                    version="v1alpha1",
                    namespace="default",
                    plural="mongodbs",
                    body=client.V1DeleteOptions(),
                    name="Mongodb"
                )
                error = False
            except Exception as e:
                response = str(e)
                if isinstance(e, ApiException):
                    body = json.loads(e.body)
                    response = body.get("message")

        finally:
            return error, response

    def delete_operator_resources(self):
        """
        Delete operator resources
        :param cluster_id:
        :param data:
        :return:
        """

        response = None
        error = True
        created_app_list = []
        try:
            kube_loader = kube_config.KubeConfigLoader(self.config)
            call_config = type.__call__(Configuration)
            try:
                kube_loader.load_and_set(call_config)
            except Exception:
                # If cluster is unavailable or unreachable.
                raise Exception('Cluster is unreachable')
            Configuration.set_default(call_config)
            kube_client_rbac = client.RbacAuthorizationV1Api()
            kube_client_apps_v1 = client.AppsV1Api()
            kube_client_core_v1 = client.CoreV1Api()
            kube_client_custom_objects = client.ApiextensionsV1beta1Api()
            # kubernetes client object

            try:
                # App deletion on kubernetes cluster
                kube_client_apps_v1.delete_namespaced_deployment(name="controller-manager",
                                                                 namespace="system")
                kube_client_core_v1.delete_namespaced_service(namespace="system",
                                                              name="controller-manager-metrics-service")
                kube_client_rbac.delete_cluster_role_binding(name="proxy-rolebinding")
                kube_client_rbac.delete_cluster_role_binding(name="manager-rolebinding")
                kube_client_rbac.delete_namespaced_role_binding(name="leader-election-rolebinding",
                                                                namespace="system")

                kube_client_rbac.delete_namespaced_role(name="leader-election-role",
                                                        namespace="system")
                kube_client_rbac.delete_cluster_role(name="proxy-role")
                kube_client_rbac.delete_cluster_role(name="metrics-reader")
                kube_client_rbac.delete_cluster_role(name="manager-role")
                kube_client_core_v1.delete_namespace(name="system")
                kube_client_custom_objects.delete_custom_resource_definition(
                    name="mongo.mytest")
                error = False
            except Exception as e:
                response = str(e)
                if isinstance(e, ApiException):
                    body = json.loads(e.body)
                    response = body.get("message")
        finally:
            return error, response
