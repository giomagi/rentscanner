import BaseHTTPServer
import Cookie
import httplib
import os
from main.domain.configuration import Configuration
from main.houses.persistence import Librarian, LoadLogger
from main.web.renderer import Renderer, LogRenderer

class PropertiesHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    # TODO: inject this
    config = Configuration.prod()

    def _userFromCookie(self):
        return Cookie.SimpleCookie(self.headers['Cookie'])['user'].value.lower() if 'Cookie' in self.headers and 'user' in Cookie.SimpleCookie(self.headers['Cookie']) else None

    def do_GET(self):
        reqPath = self.path.lower()

        user = self._userFromCookie()

        if reqPath == '/':
            self.success(FullPage(Renderer(user), Librarian(self.config)).newProperties())
        elif reqPath == '/newproperties':
            self.success(Fragment(Renderer(user), Librarian(self.config)).newProperties())
        elif reqPath == '/giolikes':
            self.success(Fragment(Renderer(user), Librarian(self.config)).savedProperties('gio'))
        elif reqPath == '/saralikes':
            self.success(Fragment(Renderer(user), Librarian(self.config)).savedProperties('sara'))
        elif reqPath == '/bothlike':
            self.success(Fragment(Renderer(user), Librarian(self.config)).savedProperties('both'))
        elif reqPath == '/seen':
            self.success(Fragment(Renderer(user), Librarian(self.config)).savedProperties('seen'))
        elif reqPath == '/discardedproperties':
            self.success(Fragment(Renderer(user), Librarian(self.config)).discardedProperties())
        elif reqPath == '/loadlog':
            self.success(LoadLogPage(LogRenderer(), LoadLogger(self.config)).log())
        elif reqPath.startswith('/resources/'):
            resourcePath = self.resourcePath()

            if os.path.isfile(resourcePath):
                self.sendResource(open(resourcePath).read())
            else:
                self.notFound('Unknown resource ' + reqPath)
        else:
            self.notFound('Unknown resource ' + reqPath)

    def do_POST(self):
        user = self._userFromCookie()

        callArgs = self.path.split('/')[1:]
        if len(callArgs) != 3 or callArgs[0] != 'rate':
            self.badRequest('Expecting a rating update in the form /rate/property_id/action, received ' + self.path)
        else:
            if callArgs[2] == 'remove':
                UserPreferences(Renderer(user), Librarian(self.config)).removeProperty(callArgs[1])
                self.sendResponse(httplib.OK, '')
            elif callArgs[2] == 'save':
                UserPreferences(Renderer(user), Librarian(self.config)).saveProperty(callArgs[1], user)
                self.sendResponse(httplib.OK, '')
            elif callArgs[2] == 'seen':
                UserPreferences(Renderer(user), Librarian(self.config)).archiveProperty(callArgs[1], user)
                self.sendResponse(httplib.OK, '')
            else:
                self.badRequest('Unsupported request, allowed: /rate/PROPERTY_ID/[save|remove]')

    def notFound(self, reason=''):
        self.sendResponse(httplib.NOT_FOUND, reason)

    def badRequest(self, reason=''):
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


class GeneratedResource(object):
    def __init__(self, renderer, librarian):
        self.renderer = renderer
        self.librarian = librarian


class Fragment(GeneratedResource):
    def newProperties(self):
        return self.renderer.renderFragment(self.librarian.retrieveNewProperties(), 'new')

    def savedProperties(self, who):
        return self.renderer.renderFragment(self.librarian.retrieveSavedProperties(who), 'saved')

    def discardedProperties(self):
        return self.renderer.renderFragment(self.librarian.retrieveDiscardedProperties(), 'trashed')


class FullPage(GeneratedResource):
    def newProperties(self):
        return self.renderer.renderFullPage(self.librarian.retrieveNewProperties(), 'new')


class LoadLogPage(object):
    def __init__(self, logRenderer, loadLogger):
        self.logRenderer = logRenderer
        self.loadLogger = loadLogger

    def log(self):
        return self.logRenderer.renderLogPage(self.loadLogger.lastLoad())


class UserPreferences(GeneratedResource):
    def removeProperty(self, propertyId):
        self.librarian.markAsNotInteresting(propertyId)

    def saveProperty(self, propertyId, who):
        self.librarian.markAsInteresting(propertyId, who)

    def archiveProperty(self, propertyId, who):
        self.librarian.markAsSeen(propertyId)
