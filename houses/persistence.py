import shelve

class Librarian:
    LIBRARY_LOCATION = "/var/gio/rentscanner/properties.data"

    def __init__(self):
        self.propertiesRegister = shelve.open(self.LIBRARY_LOCATION)

    def archiveProperties(self, properties):
        for property in properties:
            self.propertiesRegister[property.key()] = property

    def retrieveProperties(self):
        return self.propertiesRegister.values()
