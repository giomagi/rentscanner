import unittest
import datetime
from main.houses.model import Property, Price, Address
from main.web.renderer import Renderer

class TestRenderer(unittest.TestCase):
    def testRenderedItemContents(self):
        html = Renderer().render([Property('AGENT',
                                           Price(100, 'month'),
                                           Address('some place', 'SW6'),
                                           'http://some/url.go',
                                           123,
                                           datetime.datetime(2011, 9, 27))])

        # TODO: use xpath
        self.assertTrue('AGENT' in html)
        self.assertTrue('some place' in html)
        self.assertTrue('SW6' in html)
        self.assertTrue('100' in html)
        self.assertTrue('<a href="http://some/url.go">' in html)

    def testAPropertyCanBeDeletedFromTheUI(self):
        html = Renderer().render([Property('AGENT',
                                           Price(100, 'month'),
                                           Address('some place', 'SW6'),
                                           'http://some/url.go',
                                           123,
                                           datetime.datetime(2011, 9, 27))])

        self.assertTrue('<a href="rate/AGENT/123/remove">not interested</a>' in html)
