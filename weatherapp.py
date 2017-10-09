import tornado.log
import tornado.ioloop
import tornado.web
from jinja2 import Environment, PackageLoader

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

    def post(self):
        # Access the input field from the form
        city = self.get_body_argument('city')
        # call API
        # process data
        # send back to web page

# Make the Web Applicaton using Tornado
def make_app():
  return tornado.web.Application([
    (r"/", MainHandler),
    (r"/weather", WeatherHandler),
    ], autoreload=True)

# Main
if __name__ == "__main__":

    tornado.log.enable_pretty_logging()

    app = make_app()
    app.listen(8888, print('Hosting at 8888'))
    tornado.ioloop.IOLoop.current().start()
