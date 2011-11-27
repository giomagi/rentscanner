import unittest
from main.houses.model import   Address
from main.web.renderer import Renderer
from test.support.test_utils import PropertyMaker

class TestRenderer(unittest.TestCase, PropertyMaker):
    def testRendersMenuControls(self):
        html = Renderer().renderFullPage([self.aProperty(link='http://some/url.go', img='http://image.link')])

        self.assertTrue('<button type="button" onclick="showNewProperties()">show new</button>' in html)
        self.assertTrue('<button type="button" onclick="showSavedProperties()">show saved</button>' in html)

    def testRendersItemContents(self):
        html = Renderer().renderFullPage([self.aProperty(link='http://some/url.go', img='http://image.link')])

        # TODO: use xpath
        self.assertTrue('<img width="100" src="/resources/agent.jpeg" alt="AGENT" />' in html)
        self.assertTrue('some place' in html)
        self.assertTrue('SW6' in html)
        self.assertTrue('1000' in html)
        self.assertTrue('<a href="http://some/url.go">' in html)
        self.assertTrue('description' in html)
        self.assertTrue('<img width="200" src="http://image.link" />' in html)

    def testRendersRatingButtons(self):
        html = Renderer().renderFullPage([self.aProperty(agent='AG', propId='xy')])

        # TODO: use xpath
        self.assertTrue('removeProperty(\'AG_xy\')' in html)
        self.assertTrue('saveProperty(\'AG_xy\')' in html)

    def testRendersTheFullPageIfRequested(self):
        html = Renderer().renderFullPage([self.aProperty(link='some_link')])

        self.assertTrue('<html>' in html)
        self.assertTrue('<head>' in html)
        self.assertTrue('<body>' in html)
        self.assertTrue('some_link' in html)

    def testRendersOnlyThePropertiesFragmentIfRequested(self):
        html = Renderer().renderFragment([self.aProperty(link='some_link')])

        self.assertTrue('<html>' not in html)
        self.assertTrue('<head>' not in html)
        self.assertTrue('<body>' not in html)
        self.assertTrue('some_link' in html)
