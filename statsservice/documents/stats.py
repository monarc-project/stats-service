import uuid
import datetime
from mongoengine import ValidationError

from statsservice.bootstrap import db
from statsservice.lib.validation import validate_data
from statsservice.documents import Organization


class Stats(db.Document):
    uuid = db.UUIDField(binary=True, default=uuid.uuid4, required=True, unique=True)
    organization = db.ReferenceField(Organization, required=True)
    anr = db.UUIDField(binary=True, required=True)
    type = db.StringField(max_length=120, required=True)
    day = db.IntField(required=True)
    week = db.IntField(required=True)
    month = db.IntField(required=True)
    quarter = db.IntField(required=True)
    year = db.IntField(required=True)
    data = db.DynamicField(required=True)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)


    @staticmethod
    def data_validation(data, type):
        if not validate_data(data, type):
            raise ValidationError("data not valid for type {}".format(type))


    def clean(self):
        self.data_validation(self.data, self.type)


    def __str__(self):
        return """Organization: {}
        ANR: {}
        Type: {}
        Day: {}
        Week: {}
        Month: {}
        Quarter: {}
        Year: {}
        """.format(
            self.organization,
            self.anr,
            self.type,
            self.day,
            self.week,
            self.month,
            self.quarter,
            self.year,
        )
