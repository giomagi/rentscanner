import httplib
import BaseHTTPServer
import threading
import unittest
from main.domain.configuration import Configuration
from main.web.handlers.properties_handler import PropertiesHandler

class Server(threading.Thread):

    def __init__(self, config, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(Server, self).__init__(group, target, name, args, kwargs, verbose)
        server_class = BaseHTTPServer.HTTPServer
        self.webserver = server_class((config.webServerAddress(), config.webServerPort()), PropertiesHandler)

    def run(self):
        self.webserver.serve_forever()

    def stop(self):
        self.webserver.socket.close()
        self.webserver.shutdown()


class TestWebServer(unittest.TestCase):
    def setUp(self):
        config = Configuration.test()
        self.address = config.webServerAddress()
        self.port = config.webServerPort()

        self.webServerThread = Server(config)
        self.webServerThread.start()

    def tearDown(self):
        self.webServerThread.stop()

    def testGetRequestsOnAnInvalidSubpathReturnNotFound(self):
        conn = httplib.HTTPConnection(self.address, self.port)
        self.assertEqual(self.statusFor(conn, 'GET', '/something'), httplib.NOT_FOUND)

    def testAGetRequestOnAValidSubpathReturnsOk(self):
        conn = httplib.HTTPConnection(self.address, self.port)
        self.assertEqual(self.statusFor(conn, 'GET', '/newProperties'), httplib.OK)
        self.assertEqual(self.statusFor(conn, 'GET', '/savedProperties'), httplib.OK)

    #noinspection PyArgumentEqualDefault
    def testAGetRequestOnTheRootReturnsOk(self):
        conn = httplib.HTTPConnection(self.address, self.port)
        self.assertEqual(self.statusFor(conn, 'GET', '/'), httplib.OK)

    def testPostRequestsThatDontSpecifyARatingUpdateReturnBadRequest(self):
        conn = httplib.HTTPConnection(self.address, self.port)
        # expected request /rate/agent_id/action
        self.assertEqual(self.statusFor(conn, 'POST', '/rate/remove'), httplib.BAD_REQUEST)
        self.assertEqual(self.statusFor(conn, 'POST', '/zzz'), httplib.BAD_REQUEST)

    def testAWellFormedPostRequestReturnsOK(self):
        conn = httplib.HTTPConnection(self.address, self.port)
        self.assertEqual(self.statusFor(conn, 'POST', '/rate/agent_id/remove'), httplib.OK)
        self.assertEqual(self.statusFor(conn, 'POST', '/rate/agent_id/save'), httplib.OK)

    def testRequestOnMethodsOtherThanGetAndPostReturnMethodNotSupported(self):
        conn = httplib.HTTPConnection(self.address, self.port)
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
