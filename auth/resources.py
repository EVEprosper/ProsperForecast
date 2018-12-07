"""Flask plugins go here"""

import passlib
import flask_sqlalchemy
import flask_jwt_extended
import flask_marshmallow
import flask_migrate


db = flask_sqlalchemy.SQLAlchemy()
jwt = flask_jwt_extended.JWTManager()
ma = flask_marshmallow.Marshmallow()
migrate = flask_migrate.Migrate()
pwd_context = passlib.context.CryptContext(
    schemes=['pbkdf2_sha256'],
    deprecated='auto',
)
