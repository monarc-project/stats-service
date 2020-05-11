import uuid
import datetime

from statsapi.bootstrap import db
from statsapi.documents import Organization

# class Data(db.EmbeddedDocument):
#     json = db.DynamicField()


class Stats(db.Document):
    uuid = db.UUIDField(binary=True, default=lambda: str(uuid.uuid4()), primary_key=True)
    organization = db.ReferenceField(Organization, required=True)
    type = db.StringField(max_length=120, required=True)
    day = db.IntField(required=True)
    week = db.IntField(required=True)
    month = db.IntField(required=True)
    data = db.DynamicField()  # db.EmbeddedDocumentField(Data)
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)
