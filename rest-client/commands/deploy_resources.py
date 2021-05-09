import click
import sys
from utils.req_util import api_post


@click.command("deploy-resources")
@click.option('--cluster-id', '-c', default="qwerty123", prompt='Enter the cluster_id', help='cluster_id')
@click.option('--uuid-for-yaml', '-u', default="qwerty123", prompt='Enter the uuid for yaml', help="UUID of yaml")
def deploy_resources(cluster_id, uuid_for_yaml):
    deploy_api = "http://localhost:9090/example/deploy-resources"
    deploy_body = {"uuid_for_yaml": uuid_for_yaml,
                   "cluster_id": cluster_id}
    deploy_response = api_post(deploy_api, deploy_body)
    sys.stdout.write(str(deploy_response))
