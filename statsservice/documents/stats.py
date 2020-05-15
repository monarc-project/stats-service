import uuid
import datetime

from statsservice.bootstrap import db
from statsservice.documents import Organization


class Stats(db.Document):
    uuid = db.UUIDField(binary=True, default=uuid.uuid4, required=True, unique=True)
    organization = db.ReferenceField(Organization, required=True)
    anr = db.IntField(required=True)
    type = db.StringField(max_length=120, required=True)
    day = db.IntField(required=True)
    week = db.IntField(required=True)
    month = db.IntField(required=True)
    data = db.DynamicField()
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return """Organization: {}
        ANR: {}
        Type: {}
        Day: {}
        Week: {}
        Month: {}
        """.format(
            self.organization, self.anr, self.type, self.day, self.week, self.month
        )
