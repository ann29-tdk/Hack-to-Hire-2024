from mongoengine import Document, StringField, BooleanField, DateTimeField, ListField, EmbeddedDocument, EmbeddedDocumentField
from datetime import datetime

class Notification(EmbeddedDocument):
    message = StringField()
    date = DateTimeField(default=lambda: datetime.utcnow())

class User(Document):
    name = StringField(required=True)
    phoneNumber = StringField(required=True, unique=True)
    password = StringField(required=True)
    isAdmin = BooleanField(default=False)
    notifications = ListField(EmbeddedDocumentField(Notification))
    associatedFlights = ListField(StringField())
