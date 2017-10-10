import datetime
import os

import peewee
from playhouse.db_url import connect
from playhouse.postgres_ext import JSONField

DB = connect(
    os.environ.get(
        'DATABASE_URL',
        'postgres://localhost:5432/weatherapp'
    )
)

class BaseModel (peewee.Model):
    class Meta:
        database = DB

class WeatherData (BaseModel):
    db_city = peewee.CharField()
    db_weather_API_response = peewee.JSONField()
    db_requested_time = peewee.DateTimeField(default=datetime.datetime.utcnow)

    def __str__ (self):
        return self.name
