import httplib
import BaseHTTPServer
import threading
import unittest
from main.web.webserver import PropertiesHandler, FullPage, UserPreferences
from test.support.mocks import MockRenderer, MockLibrarian

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
