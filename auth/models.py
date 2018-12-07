"""SQLalchemy scheamas for services"""

from . import resources

class User(resources.db.Model):
    """basic user model"""

    id = resources.db.Column(
        resources.db.Integer,
        primary_key=True,
    )
    username = resources.db.Column(
        resources.db.String(64),
        unique=True,
        nullable=False,
    )
    email = resources.db.Column(
        resources.db.String(128),
        unique=True,
        nullable=False,
    )
    password = resources.db.Column(
        resources.db.String(128),
        nullable=False,
    )
    active = resources.db.Column(
        resources.db.Boolean,
        default=True,
    )

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = resources.pwd_context.hash(self.password)
