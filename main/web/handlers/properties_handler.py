import BaseHTTPServer
import httplib
import os
from main.houses.persistence import Librarian
from main.web.renderer import Renderer

class PropertiesHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.success(FullPage().allProperties())
        elif self.path.startswith('/resources/'):
            resourcePath = self.resourcePath()

            if os.path.isfile(resourcePath):
                self.success(open(resourcePath).read())
            else:
                self.notFound('Unknown resource ' + self.path)
        else:
            self.notFound('Unknown resource ' + self.path)

    def do_POST(self):
        callArgs = self.path.split('/')[1:]
        if len(callArgs) != 3 or callArgs[0] != 'rate':
            self.badRequest('Expecting a rating update in the form /rate/property_id/action, received ' + self.path)
        else:
            if callArgs[2] != 'remove':
                self.badRequest('Supporting only remove at the moment')
            else:
                UserPreferences().removeProperty(callArgs[1])
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

    def resourcePath(self):
        return os.path.join(os.path.dirname(__file__), '..' + self.path)

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

    def removeProperty(self, propertyId):
        self.librarian.markAsNotInteresting(propertyId)
