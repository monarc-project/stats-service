import uuid
from datetime import datetime, date
from sqlalchemy.dialects.postgresql import JSONB, UUID

from statsservice.bootstrap import db
from statsservice.lib.validation import validate_data


class Stats(db.Model):
    uuid = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    anr = db.Column(UUID(as_uuid=True), nullable=False)
    type = db.Column(db.String(), index=True, nullable=False)
    date = db.Column(db.Date(), index=True, nullable=False)
    data = db.Column(JSONB, default={}, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # foreign keys
    client_id = db.Column(db.Integer(), db.ForeignKey("client.id"), default=None)

    def __str__(self):
        return """Client {}
ANR: {}
Type: {}
Date: {}
Data: {}
Created at: {}
""".format(
            self.client.name,
            self.anr,
            self.type,
            self.date,
            self.data,
            self.created_at
        )
