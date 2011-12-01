import BaseHTTPServer
from main.web.handlers.properties_handler import PropertiesHandler

class Server(object):
    def __init__(self, config):
        self.address = config.webServerAddress()
        self.port = config.webServerPort()

    def start(self):
        server_class = BaseHTTPServer.HTTPServer
        webserver = server_class((self.address, self.port), PropertiesHandler)

        print "Web Server UP"
        try:
            webserver.serve_forever()
        except KeyboardInterrupt:
            pass

        webserver.server_close()
        print "Web Server DOWN"

  