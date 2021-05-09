import click
import sys
from utils.req_util import api_post


@click.command("create-yaml")
@click.option('--image-tag', '-i', default="latest", prompt='Enter the image tag', help='Image tag')
@click.option('--image-name', '-n', default="docker.io/mongodb-exporter", prompt='Enter the image name', help="Image name")
def create_yaml(image_tag, image_name):
    print("{0} and {1}".format(image_name, image_tag))
    create_yaml_api = "http://localhost:9090/example/create-yaml"
    body = {"image_repository": image_name, "image_tag": image_tag}
    create_response = api_post(create_yaml_api, body)
    sys.stdout.write(str(create_response))
