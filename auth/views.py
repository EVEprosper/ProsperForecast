"""endpoint stuff goes here?"""
import flask
import flask_restful

from . import endpoints

blueprint = flask.Blueprint(
    'auth',
    __name__,
    url_prefix='/auth',
)
api = flask_restful.Api(blueprint)
api.add_resource(endpoints.Login, '/login')
