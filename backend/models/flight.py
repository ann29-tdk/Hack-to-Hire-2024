from mongoengine import Document, StringField, BooleanField, DateTimeField, ListField, IntField

class Flight(Document):
    flightNumber = StringField(required=True)
    arrivalDate = DateTimeField(required=True)
    arrivalTimes = ListField(StringField())
    departureTimes = ListField(StringField())
    isCancelled = BooleanField(default=False)
    destination = StringField(required=True)
    arrivalDelays = ListField(IntField())
    departureDelays = ListField(IntField())
