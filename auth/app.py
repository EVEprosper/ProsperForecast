"""Flask handles for application"""
import os

import flask

import prosper.common.prosper_logging as p_logging
from . import config
from . import views
from . import resources

__app_name__ = 'auth'
__version__ = 'v1'

HERE = HERE = os.path.abspath(os.path.dirname(__file__))

def create_app(testing=False, cli=False):
    """Flask Application Factory"""
    app = flask.Flask(__app_name__)

    configure_app(app, testing, cli)
    configure_extension(app, cli)
    register_blueprints(app)

    return app

def configure_app(app, testing=False, cli=False):
    """apply configurations to Flask App

    Args:
        app (:obj:`flask.Flask`): Flask application
        testing (bool): running as pytest-launcher
        cli (bool): running as cli-launcher

    """

    app.config.from_object('auth.config.DefaultConfig')
    log_builder = p_logging.ProsperLogger(
        app.name,
        app.config.get(
            'PROSPER_LOGGING__log_path',
            os.path.join(HERE, 'logs'),
        ),
    )

    if testing:
        app.config.from_object(f'{__app_name__}.config.Test')
        log_builder.configure_debug_logger()

    elif cli:
        app.config.from_object(f'{__app_name__}.config.Cli')
        log_builder.configure_debug_logger()
    else:
        app.config.from_object(f'{__app_name__}.config.Production')
        log_builder.configure_slack_logger(
            slack_webhook=app.config.get('SLACK_WEBHOOK') # TODO: fix this
        )

    [app.logger.addHandler(handler) for handler in log_builder.logger.handlers]

def configure_extension(app, cli=False):
    """initialize flask extension

    Args:
        app (:obj:`flask.Flask`): Flask application
        cli (bool): running as cli-launcher

    """
    resources.db.init_app(app)
    resources.jwt.init_app(app)

    if cli:
        resources.migrate.init_app(app, resources.db)

def register_blueprints(app):
    """register blueprints to application

    Args:
        app (:obj:`flask.Flask`): Flask application
    """
    # ENDPOINTS GO HERE #
    app.register_blueprint(views.blueprint)
