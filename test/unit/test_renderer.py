from main.houses.model import   Address
from main.web.renderer import Renderer
from test.support.test_utils import PropertyMaker

class TestRenderer(PropertyMaker):
    def testRenderedItemContents(self):
        html = Renderer().render([self.aProperty(link='http://some/url.go', img='http://image.link')])

        # TODO: use xpath
        self.assertTrue('AGENT' in html)
        self.assertTrue('some place' in html)
        self.assertTrue('SW6' in html)
        self.assertTrue('1000' in html)
        self.assertTrue('<a href="http://some/url.go">' in html)
        self.assertTrue('description' in html)
        self.assertTrue('<img src="http://image.link" />' in html)
