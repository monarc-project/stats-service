from statsservice.bootstrap import db


class Organization(db.Document):
    name = db.StringField(primary_key=True)  # or maybe UUID
    token = db.StringField(required=True, unique=True)

    def __str__(self):
        return "Name: {}\nToken: {}".format(self.name, self.token)
