import flask
import flask_restful
import flask_jwt_extended

from . import models
from . import resources

class UserSchema(resources.ma.Schema):

    username = resources.ma.String(required=True)
    password = resources.ma.String(required=True)

    class Meta:
        model = models.User
        sqla_session = resources.db.session


class Login(flask_restful.Resource):

    schema = UserSchema()
    model = models.User

    def __init__(self):
       self.data = self.schema.load(flask.request.json)

    def post(self):
        """handle login requests"""
        if self.data.errors:
            return {'ERROR': f'INVALID REQUEST {self.data.errors}'}, 400

        user_info = self.model.query.filter_by(username=self.data['username']).first()
        if any([
                not user_info,
                not resources.pwd_context.verify(self.data['password'], user_info.password),
        ]):
            return {'ERROR': 'INVALID CREDENTIALS'}, 400

        access_token = flask_jwt_extended.create_access_token(identity=user_info.id)
        refresh_token = flask_jwt_extended.create_refresh_token(identity=user_info.id)
        flask_jwt_extended.add_token_to_database(
            access_token, flask.current_app.config['JWT_IDENTITY_CLAIM']
        )
        flask_jwt_extended.add_token_to_database(
            refresh_token, flask.current_app.config['JWT_IDENTITY_CLAIM']
        )

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
        }, 200

class RevokeAccess(flask_restful.Resource):

    schema = UserSchema()
    model = models.User

    def delete(self):
        """handle revoke requests"""
