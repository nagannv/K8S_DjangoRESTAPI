import click
import sys
from utils.req_util import api_delete


@click.command("delete-operator-resources")
@click.option('--cluster-id', '-c', default="qwerty123", prompt='Enter the cluster_id', help='cluster_id')
def delete_operator_resources(cluster_id):
    delete_api = "http://localhost:9090/example/delete-operator-resources"
    params = {"cluster_id": cluster_id}
    res = api_delete(delete_api, params)
    sys.stdout.write(str(res))
