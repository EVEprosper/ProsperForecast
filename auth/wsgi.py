"""WSGI launcher for gunicorn and other direct-launchers"""
from . import app as flask_app

app = flask_app.create_app()
