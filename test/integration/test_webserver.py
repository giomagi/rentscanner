import httplib
import BaseHTTPServer
import threading
import unittest
from main.web.webserver import PropertiesHandler, FullPage, UserPreferences
from test.support.mocks import MockRenderer, MockLibrarian

class Server(threading.Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(Server, self).__init__(group, target, name, args, kwargs, verbose)
        self.host = '192.168.1.2'
        self.port = 1234
        server_class = BaseHTTPServer.HTTPServer
        self.webserver = server_class((self.host, self.port), PropertiesHandler)

    def run(self):
        self.webserver.serve_forever()

    def stop(self):
        self.webserver.socket.close()
        self.webserver.shutdown()


class TestWebServer(unittest.TestCase):
    def setUp(self):
        self.webServerThread = Server()
        self.webServerThread.start()

    def tearDown(self):
        self.webServerThread.stop()

    def testGetRequestsOnAnySubpathReturnNotFound(self):
        conn = httplib.HTTPConnection(self.webServerThread.host, self.webServerThread.port)
        self.assertEqual(self.statusFor(conn, 'GET', '/something'), httplib.NOT_FOUND)

    #noinspection PyArgumentEqualDefault
    def testAGetRequestOnTheRootReturnsOk(self):
        conn = httplib.HTTPConnection(self.webServerThread.host, self.webServerThread.port)
        self.assertEqual(self.statusFor(conn, 'GET', '/'), httplib.OK)

    def testPostRequestsThatDontSpecifyARatingUpdateReturnBadRequest(self):
        conn = httplib.HTTPConnection(self.webServerThread.host, self.webServerThread.port)
        # expected request /rate/agent/id/action
        self.assertEqual(self.statusFor(conn, 'POST', '/rate/id/remove'), httplib.BAD_REQUEST)
        self.assertEqual(self.statusFor(conn, 'POST', '/zzz'), httplib.BAD_REQUEST)

    def testAWellFormedPostRequestReturnsOK(self):
        conn = httplib.HTTPConnection(self.webServerThread.host, self.webServerThread.port)
        self.assertEqual(self.statusFor(conn, 'POST', '/rate/agent/id/remove'), httplib.OK)

    def testRequestOnMethodsOtherThanGetAndPostReturnMethodNotSupported(self):
        conn = httplib.HTTPConnection(self.webServerThread.host, self.webServerThread.port)
        self.assertEqual(self.statusFor(conn, 'OPTIONS'), httplib.NOT_IMPLEMENTED)
        self.assertEqual(self.statusFor(conn, 'HEAD'), httplib.NOT_IMPLEMENTED)
        self.assertEqual(self.statusFor(conn, 'PUT'), httplib.NOT_IMPLEMENTED)
        self.assertEqual(self.statusFor(conn, 'DELETE'), httplib.NOT_IMPLEMENTED)
        self.assertEqual(self.statusFor(conn, 'TRACE'), httplib.NOT_IMPLEMENTED)
        self.assertEqual(self.statusFor(conn, 'CONNECT'), httplib.NOT_IMPLEMENTED)

    def statusFor(self, conn, method, path = '/'):
        return self.responseFor(conn, method, path).status

    def responseFor(self, conn, method, path = '/'):
        conn.request(method, path)
        return conn.getresponse()

class TestFullPage(unittest.TestCase):
    def testAGetRequestOnTheRootReturnsTheReport(self):
        expectedHtml = 'expected HTML'
        renderer = MockRenderer()

        renderer.mockedResponse = expectedHtml
        actualHtml = FullPage(renderer, MockLibrarian()).allProperties()

        self.assertEqual(actualHtml, expectedHtml)

class TestUserPreferences(unittest.TestCase):
    def testARemoveRequestIsPassedThroughToTheLibrarian(self):
        librarian = MockLibrarian()
        UserPreferences(MockRenderer(), librarian).removeProperty('AGENT', 'id')

        self.assertEqual(librarian.capturedRequest, ('remove', 'AGENT', 'id'))
