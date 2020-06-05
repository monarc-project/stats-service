import secrets
import datetime

from statsservice.bootstrap import db


class Organization(db.Document):
    name = db.StringField(primary_key=True)  # or maybe UUID
    token = db.StringField(required=True, unique=True, default=secrets.token_urlsafe(64))
    created_at = db.DateTimeField(default=datetime.datetime.utcnow)
    updated_at = db.DateTimeField(default=datetime.datetime.utcnow)

    def __str__(self):
        return "Name: {}\nToken: {}\nCreated at:{}".format(self.name, self.token, self.created_at)
