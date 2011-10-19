import BaseHTTPServer
import httplib
from main.houses.persistence import Librarian
from main.web.renderer import Renderer

class PropertiesHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != '/':
            self.notFound('Unknown resource ' + self.path)

        self.success(FullPage().allProperties())

    def do_POST(self):
        callArgs = self.path.split('/')[1:]
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

class FullPage():
    def __init__(self, renderer = Renderer(), librarian = Librarian()):
        self.renderer = renderer
        self.librarian = librarian

    def allProperties(self):
        return self.renderer.render(self.librarian.retrieveInterestingProperties())


class UserPreferences():
    def __init__(self, renderer = Renderer(), librarian = Librarian()):
        self.renderer = renderer
        self.librarian = librarian

    def removeProperty(self, agentName, agentId):
        self.librarian.markAsNotInteresting(agentName, agentId)
