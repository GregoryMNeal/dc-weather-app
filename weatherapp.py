import datetime

import tornado.log
import tornado.ioloop
import tornado.web
from jinja2 import Environment, PackageLoader
import requests

# This retrieves the directory where the html lives
ENV = Environment(
    loader=PackageLoader('weatherapp', 'templates')
)

# Home Page Handler
class MainHandler(tornado.web.RequestHandler):

    def get(self):
        template = ENV.get_template('index.html')
        self.write(template.render())

# Home Page Handler
class WeatherHandler(tornado.web.RequestHandler):
    # It's good practice to have a get method for every page
    def get(self):
        template = ENV.get_template('weather.html')
        self.write(template.render())
    # You must use a 'post' method to receive input fields
    def post(self):
        # Retrieve the input field from the form
        form_data_city = self.get_body_argument('city')
        # Create variable for select statement
        too_old = datetime.datetime.utcnow() - datetime.timedelta(minutes=15)
        # Retrieve cached weather from the database for the city
        try:
            weather_data = WeatherData.select().where(WeatherData.db_city == form_data_city).where(WeatherData.db_requested_time >= too_old).get()
            # dictionary: weather_data.db_weather_API_response
        except:
            # Set API parameters
            url = "http://api.openweathermap.org/data/2.5/weather"
            querystring = {}
            querystring["q"] = form_data_city
            querystring["APPID"] = "f299452ee8305d7fe83e56f4699fdfdb"
            # Call the API to get current weather
            response = requests.request("GET", url, params=querystring)
            # Write cache data to db
            weather_data = WeatherData.create(db_city=form_data_city,
            db_weather_API_response = response.json())
        # Process the response
        print(response.json())
        # Render the weather page passing data to be displayed
        template = ENV.get_template('weather.html')
        self.write(template.render({'data': weather_data.db_weather_API_response, 'myname': 'Greg'}))

# Make the Web Applicaton using Tornado
def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/weather", WeatherHandler),
    # The following reference to the StaticFileHandler should
    # ALWAYS be here.
    (r"/static/(.*)", tornado.web.StaticFileHandler, {'path': 'static'}),
    ], autoreload=True)

# Main
if __name__ == "__main__":

    tornado.log.enable_pretty_logging()

    app = make_app()
    app.listen(8888, print('Hosting at 8888'))
    tornado.ioloop.IOLoop.current().start()
