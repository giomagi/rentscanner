import BaseHTTPServer
from main.web.handlers.properties_handler import PropertiesHandler

class Server:
    def start(self):
        server_class = BaseHTTPServer.HTTPServer
        webserver = server_class(('192.168.1.2', 1234), PropertiesHandler)

        print "Web Server UP"
        try:
            webserver.serve_forever()
        except KeyboardInterrupt:
            pass

        webserver.server_close()
        print "Web Server DOWN"

  