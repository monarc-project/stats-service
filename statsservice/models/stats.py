import uuid
from datetime import datetime
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
    type = db.Column(db.String(), nullable=False)
    day = db.Column(db.Integer())
    week = db.Column(db.Integer())
    month = db.Column(db.Integer())
    quarter = db.Column(db.Integer())
    year = db.Column(db.Integer())
    data = db.Column(JSONB, default={})
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(), default=datetime.utcnow)

    # foreign keys
    org_id = db.Column(db.Integer(), db.ForeignKey("organization.id"), default=None)

    def __str__(self):
        return """Organization: {}
ANR: {}
Type: {}
Day: {}
Week: {}
Month: {}
Quarter: {}
Year: {}
Create at: {}
""".format(
            self.organization.name,
            self.anr,
            self.type,
            self.day,
            self.week,
            self.month,
            self.quarter,
            self.year,
            self.created_at,
        )
