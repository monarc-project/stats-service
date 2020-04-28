from statsapi.bootstrap import db


class Organization(db.Document):
    token = db.DynamicField(unique=True, required=True)
