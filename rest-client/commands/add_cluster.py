import base64
import json
import os
import sys
from pathlib import Path

import click
import yaml

from utils.req_util import api_post


@click.command("add-cluster")
@click.option('--kubeconfig', '-k', default=os.path.join(str(Path.home()), ".kube", "config"),
              prompt='Path to kube config file', help='Absolute path to kube '
                                                      'config file')
def add_cluster(kubeconfig):
    add_cluster_api = "http://localhost:9090/example/add-cluster"
    if not os.path.exists(kubeconfig):
        raise Exception("Config file do not exists")
    with open(kubeconfig, 'r') as file:
        data_for_cluster_config = yaml.load(file, Loader=yaml.FullLoader)
    encoded_kubeconfig = base64.b64encode(bytes(str(data_for_cluster_config), 'utf-8'))
    add_body = {"cluster_config": str(encoded_kubeconfig)}
    add_response = api_post(add_cluster_api, add_body)
    sys.stdout.write(str(add_response))
