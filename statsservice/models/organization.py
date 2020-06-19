import uuid
import secrets
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB, UUID

from statsservice.bootstrap import db


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(
        UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False,
    )
    name = db.Column(db.String(100), unique=True)
    token = db.Column(db.String(100), unique=True, default=secrets.token_urlsafe(64))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # relationship
    stats = db.relationship(
        "Stats", backref="organization", lazy="dynamic", cascade="all,delete-orphan"
    )

    def __str__(self):
        return "UUID: {}\nName: {}\nToken: {}\nCreated at: {}".format(
            self.uuid, self.name, self.token, self.created_at
        )
