"""app creation and flask.CLI launcher"""

import click
import flask

import prosper.common.prosper_config as p_config
from . import app

def launch_app(info):
    return app.create_app(cli=True)

@click.group(cls=flask.cli.FlaskGroup)
def cli():
    """cli entry point"""

@cli.command('init')
@cli.option(
    '--secret-cfg',
    help='Path to jinja-templated secrets',
)
@cli.option(
    '--config',
    help='Path to configparser file for user configuration',
    default='config.j2',
)
def init():
    """generate DB's, and initialize data"""

if __name__ == '__main__':
    cli()
