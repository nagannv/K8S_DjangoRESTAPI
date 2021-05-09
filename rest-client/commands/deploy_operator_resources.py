import click
import sys
from utils.req_util import api_post


@click.command("deploy-operator-resources")
@click.option('--cluster-id', '-c', default="qwerty123", prompt='Enter the cluster_id', help='cluster_id')
def deploy_operator_resources(cluster_id):
    deploy_operator_api = "http://localhost:9090/example/deploy-operator-resources"
    deploy_operator_body = {"cluster_id": cluster_id}
    response = api_post(deploy_operator_api, deploy_operator_body)
    sys.stdout.write(str(response))
