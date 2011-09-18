import cPickle
import os

# TODO: close file after r/w (or open at startup and keep it so
# TODO: use shelve or a real (nosql) db?
class Librarian:
    LIBRARY_LOCATION = "/var/gio/rentscanner/properties.pkl"

    def __init__(self):
        pass

    def archiveProperties(self, properties):
        for property in properties:
            cPickle.dump(property, self._openLibraryForWrite())

    def retrieveProperties(self):
        return [cPickle.load(self._openLibraryForRead())]

    def _openLibraryForWrite(self):
        return self.openLibrary("w")

    def _openLibraryForRead(self):
        return self.openLibrary("r")

    def openLibrary(self, mode):
        if not os.path.exists(self.LIBRARY_LOCATION):
            folder = os.path.split(self.LIBRARY_LOCATION)[0]
            if not os.path.exists(folder):
                os.makedirs(folder)

            return open(self.LIBRARY_LOCATION, mode)

        return open(self.LIBRARY_LOCATION, "a" if mode == "w" else "r")
