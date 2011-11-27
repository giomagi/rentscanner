import BaseHTTPServer
import httplib
import os
from main.domain.configuration import Configuration
from main.houses.persistence import Librarian
from main.web.renderer import Renderer

class PropertiesHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    # TODO: inject this
    config = Configuration.prod()
    
    def do_GET(self):
        reqPath = self.path.lower()

        if reqPath == '/':
            self.success(FullPage(Renderer(), Librarian(self.config)).newProperties())
        elif reqPath == '/newproperties':
            self.success(Fragment(Renderer(), Librarian(self.config)).newProperties())
        elif reqPath == '/savedproperties':
            self.success(Fragment(Renderer(), Librarian(self.config)).savedProperties())
        elif reqPath.startswith('/resources/'):
            resourcePath = self.resourcePath()

            if os.path.isfile(resourcePath):
                self.sendResource(open(resourcePath).read())
            else:
                self.notFound('Unknown resource ' + reqPath)
        else:
            self.notFound('Unknown resource ' + reqPath)

    def do_POST(self):
        callArgs = self.path.split('/')[1:]
        if len(callArgs) != 3 or callArgs[0] != 'rate':
            self.badRequest('Expecting a rating update in the form /rate/property_id/action, received ' + self.path)
        else:
            if callArgs[2] == 'remove':
                UserPreferences(Renderer(), Librarian(self.config)).removeProperty(callArgs[1])
                self.sendResponse(httplib.OK, '')
            elif callArgs[2] == 'save':
                UserPreferences(Renderer(), Librarian(self.config)).saveProperty(callArgs[1])
                self.sendResponse(httplib.OK, '')
            else:
                self.badRequest('Unsupported request, allowed: /rate/PROPERTY_ID/[save|remove]')

    def notFound(self, reason = ''):
        self.sendResponse(httplib.NOT_FOUND, reason)

    def badRequest(self, reason = ''):
        self.sendResponse(httplib.BAD_REQUEST, reason)

    def success(self, result):
        self.sendResponse(httplib.OK, result)

    def sendResource(self, resourceContent):
        self.sendResponse(httplib.OK, resourceContent, False)

    def sendResponse(self, code, result, encode=True):
        self.send_response(code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(result.encode('ascii', 'xmlcharrefreplace') if encode else result)

    def resourcePath(self):
        return os.path.join(os.path.dirname(__file__), '..' + self.path)

# TODO: rename to something sensible
class ConfigBasedResource:
    def __init__(self, renderer, librarian):
        self.renderer = renderer
        self.librarian = librarian

class Fragment(ConfigBasedResource):
    def newProperties(self):
        return self.renderer.renderFragment(self.librarian.retrieveNewProperties())

    def savedProperties(self):
        return self.renderer.renderFragment(self.librarian.retrieveSavedProperties())

class FullPage(ConfigBasedResource):
    def newProperties(self):
        return self.renderer.renderFullPage(self.librarian.retrieveNewProperties())


class UserPreferences(ConfigBasedResource):
    def removeProperty(self, propertyId):
        self.librarian.markAsNotInteresting(propertyId)

    def saveProperty(self, propertyId):
        self.librarian.markAsInteresting(propertyId)
