from main.domain.configuration import Configuration
from main.houses.persistence import Librarian
from main.web.renderer import Renderer

class MockRenderer(Renderer):
    mockedResponse = ''

    def renderFullPage(self, properties, type):
        return self.mockedResponse

class MockLibrarian(Librarian):
    mockedPropertiesList = []
    capturedRequest = None

    def __init__(self):
        Librarian.__init__(self, Configuration.dummy())

    def retrieveNewProperties(self):
        return self.mockedPropertiesList

    def archiveProperties(self, properties):
        pass

    def markAsNotInteresting(self, propertyId):
        self.capturedRequest = ('remove', propertyId)


