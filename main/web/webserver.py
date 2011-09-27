import BaseHTTPServer
from main.houses.persistence import Librarian
from main.web.renderer import Renderer

class GetPropertiesHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(Renderer().render(Librarian().retrieveProperties()))
