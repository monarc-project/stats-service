import uuid
import secrets
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import JSONB, UUID

from statsservice.bootstrap import db

ROLE_USER = 1
ROLE_ADMIN = 2

def my_secret():
    return secrets.token_urlsafe(64)


class Client(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False,
    )
    name = db.Column(db.String(100), unique=True)
    token = db.Column(db.String(100), unique=True, default=my_secret)
    role = db.Column(db.Integer, default=ROLE_USER)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), onupdate=datetime.utcnow)

    # user rights
    is_active = db.Column(db.Boolean(), default=False)

    # relationship
    stats = db.relationship(
        "Stats", backref="client", lazy="dynamic", cascade="all,delete-orphan"
    )

    def get_id(self):
        """
        Return the id of the client.
        """
        return self.id

    def __str__(self):
        return "UUID: {}\nName: {}\nRole: {}\nToken: {}\nCreated at: {}".format(
            self.uuid, self.name, self.role, self.token, self.created_at
        )

    def is_admin(self):
        return self.role == ROLE_ADMIN