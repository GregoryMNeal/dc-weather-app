# This migration does the intial database setup.  You should do a
# export PYTHONPATH=`pwd` from within the top director of the project
# before invoking program.
import models

# This creates the database tables using the Class definitions in
# models.py
def forward ():
    models.DB.create_tables([models.WeatherData])

if __name__ == '__main__':

    forward()
