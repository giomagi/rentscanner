import BaseHTTPServer
from main.houses.foxtons import Foxtons
from main.houses.persistence import Librarian
from main.web.webserver import GetPropertiesHandler

if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class(('192.168.1.2', 1234), GetPropertiesHandler)

    Librarian().archiveProperties(Foxtons().properties())

    print "UP"

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

    print "DOWN"
