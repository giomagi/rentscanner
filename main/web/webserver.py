import BaseHTTPServer
import httplib
from main.houses.persistence import Librarian
from main.web.renderer import Renderer

class PropertiesHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    renderer = Renderer()
    librarian = Librarian()

    def do_GET(self):
        if self.path != '/':
            self.notFound('Unknown resource ' + self.path)

        self.success(self.renderer.render(self.librarian.retrieveProperties()))

    def do_POST(self):
        callArgs = self.path.split('/')
        if len(callArgs) != 4 or callArgs[0] != 'rate':
            self.badRequest('Expecting a rating update in the form /rate/agent/id/action, received ' + self.path)

        self.sendResponse(httplib.OK, '')

    def notFound(self, reason = ''):
        self.sendResponse(httplib.NOT_FOUND, reason)

    def badRequest(self, reason = ''):
        self.sendResponse(httplib.BAD_REQUEST, reason)

    def success(self, result):
        self.sendResponse(httplib.OK, result)

    def sendResponse(self, code, result):
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(result)


