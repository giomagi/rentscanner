from main.houses.persistence import Librarian
from main.web.renderer import Renderer

class MockRenderer(Renderer):
    mockedResponse = ''

    def render(self, properties):
        return self.mockedResponse

class MockLibrarian(Librarian):
    mockedPropertiesList = []

    def retrieveProperties(self):
        return self.mockedPropertiesList

    def archiveProperties(self, properties):
        pass