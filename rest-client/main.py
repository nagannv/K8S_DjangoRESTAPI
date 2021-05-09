import click
from commands.create_yaml import create_yaml
from commands.add_cluster import add_cluster
from commands.deploy_resources import deploy_resources
from commands.deploy_operator_resources import deploy_operator_resources
from commands.delete_resources import delete_resources
from commands.delete_operator_resources import delete_operator_resources


@click.group(help="CLI tool to interact with the django server")
def cli():
    pass


cli.add_command(create_yaml)
cli.add_command(add_cluster)
cli.add_command(deploy_resources)
cli.add_command(deploy_operator_resources)
cli.add_command(delete_resources)
cli.add_command(delete_operator_resources)

if __name__ == "__main__":
    cli()
