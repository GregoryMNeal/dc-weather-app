import datetime
import os

import peewee
from playhouse.db_url import connect

# This import makes the JSONField data type available
from playhouse.postgres_ext import JSONField

# This makes the app aware of where the database lives.  The database MUST BE
# created manually (Postico)
DB = connect(
    os.environ.get(
        'DATABASE_URL',
        'postgres://localhost:5432/weatherapp'
    )
)

# This is the parent for all database Classes.  All Classes inherit from
# this model (Class)
class BaseModel (peewee.Model):
    class Meta:
        database = DB

# This is the model for (definition of) the WeatherData table
class WeatherData (BaseModel):
    db_city = peewee.CharField()
    db_weather_API_response = JSONField()
    db_requested_time = peewee.DateTimeField(default=datetime.datetime.utcnow)

    def __str__ (self):
        return self.name
