import datetime

from statsapi.bootstrap import db
from statsapi.documents import Organization

# class Data(db.EmbeddedDocument):
#     json = db.DynamicField()


class Stats(db.Document):
    organization = db.ReferenceField(Organization)
    type = db.StringField(max_length=120, required=True)
    day = db.IntField(required=True)
    week = db.IntField(required=True)
    month = db.IntField(required=True)
    data = db.DynamicField()  # db.EmbeddedDocumentField(Data)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)
