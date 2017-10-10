# Import Tornado to make the app a web app
import tornado.log
import tornado.ioloop
import tornado.web
# Import Jinja -
from jinja2 import Environment, PackageLoader
# Import datetime - used to do date calculations
import datetime
# Import requests - used in calling the API
import requests
# Import model - used to find the model for the database file(s)
from models import WeatherData

# This retrieves the path where the HTML lives
ENV = Environment(
    loader=PackageLoader('weatherapp', 'templates')
)

# Home Page Handler - prompts the user for input field 'city'
class MainHandler(tornado.web.RequestHandler):

    def get(self):
        template = ENV.get_template('index.html')
        self.write(template.render())

# Weather Page Handler - retrieves the weather via an API call or from the
# database, displays the result to the user
class WeatherHandler(tornado.web.RequestHandler):

    # This 'get' method isn't used for anything but it's good
    # practice to have a get method for every handler and do something if
    # a user accesses it
    def get(self):
        template = ENV.get_template('weather.html')
        self.write(template.render())

    # You must use a 'post' method to receive input fields
    def post(self):
        # Retrieve the input field from the form
        form_data_city = self.get_body_argument('city')
        # Make the input consistent every time because it is used as a key to the
        # the record in the database
        form_data_city = form_data_city.title()
        # Calculate a date/time that is 15 minutes ago.  This is used to select
        # records from the DB that are greater than or equal to this date/time.
        too_old = datetime.datetime.utcnow() - datetime.timedelta(minutes=15)
        # Try to retrieve a cached weather record from the database for the
        # city that is 15 minutes or newer
        try:
            weather_data = WeatherData.select().where(WeatherData.db_city == form_data_city).where(WeatherData.db_requested_time >= too_old).get()
        # No cached data found, call the weather API, write new cache record
        # to the database.
        except:
            # Set API parameters
            url = "http://api.openweathermap.org/data/2.5/weather"
            querystring = {}
            querystring["q"] = form_data_city
            querystring["APPID"] = "f299452ee8305d7fe83e56f4699fdfdb"
            querystring["units"] = "imperial"
            # Call the API to get the current weather
            response = requests.request("GET", url, params=querystring)
            # Write cache data to the database
            weather_data = WeatherData.create(db_city=form_data_city,
            db_weather_API_response = response.json())

        # Display the weather page passing the data to be displayed
        template = ENV.get_template('weather.html')
        self.write(template.render({'data': weather_data.db_weather_API_response}))

# Make the Web Applicaton using Tornado
def make_app():
  return tornado.web.Application([
    # This processes any request that hits the URL with nothing after the '/'
    (r"/", MainHandler),
    # This processes any request that hits the URL/weather
    (r"/weather", WeatherHandler),
    # The following reference to the StaticFileHandler should
    # ALWAYS be here!!!  It's used so the CSS specified in the
    # <link rel="stylesheet" href="static/css/styles.css"> can be found
    (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static'}),
    ], autoreload=True)

# Main
if __name__ == "__main__":

    tornado.log.enable_pretty_logging()

    app = make_app()
    app.listen(8888, print('Hosting at 8888'))
    tornado.ioloop.IOLoop.current().start()
