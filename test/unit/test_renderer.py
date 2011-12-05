import unittest
from main.houses.model import   Address
from main.web.renderer import Renderer
from test.support.test_utils import PropertyMaker

class TestRenderer(unittest.TestCase, PropertyMaker):
    def testRendersMenuControls(self):
        html = Renderer().renderFullPage([self.aProperty(link='http://some/url.go', img='http://image.link')], 'new')

        self.assertTrue('View New' in html)
        self.assertTrue('View Saved' in html)

    def testRendersItemContents(self):
        html = Renderer().renderFullPage([self.aProperty(link='http://some/url.go', img='http://image.link')], 'new')

        # TODO: use xpath
        self.assertTrue('<img src="/resources/agent.jpeg" width="100" alt="AGENT" />' in html)
        self.assertTrue('some place' in html)
        self.assertTrue('SW6' in html)
        self.assertTrue('1000' in html)
        self.assertTrue('<a href="http://some/url.go">' in html)
        self.assertTrue('description' in html)
        self.assertTrue('<img src="http://image.link" width="200" />' in html)

    def testRendersRatingButtons(self):
        html = Renderer().renderFullPage([self.aProperty(agent='AG', propId='xy')], 'new')

        # TODO: use xpath
        self.assertTrue('removeProperty(\'AG_xy\')' in html)
        self.assertTrue('saveProperty(\'AG_xy\')' in html)

    def testRendersTheFullPageIfRequested(self):
        html = Renderer().renderFullPage([self.aProperty(link='some_link')], 'new')

        self.assertTrue('<html>' in html)
        self.assertTrue('<head>' in html)
        self.assertTrue('<body>' in html)
        self.assertTrue('some_link' in html)

    def testRendersOnlyThePropertiesFragmentIfRequested(self):
        html = Renderer().renderFragment([self.aProperty(link='some_link')], 'new')

        self.assertTrue('<html>' not in html)
        self.assertTrue('<head>' not in html)
        self.assertTrue('<body>' not in html)
        self.assertTrue('some_link' in html)
