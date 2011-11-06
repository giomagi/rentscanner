from datetime import datetime
import os
import unittest
from main.houses.model import Property, Price, Address
from main.houses.persistence import Librarian
from test.support.test_utils import PropertyMaker

class TestPersistence(PropertyMaker):
    def setUp(self):
        self.cleanLibrary()

    def testRoundtripsAProperty(self):
        aProperty = self.aProperty()

        librarian = Librarian()
        librarian.archiveProperties([aProperty])
        properties = librarian.retrieveNewProperties()

        self.assertEqual(1, len(properties))
        self.assertEqual(aProperty, properties[0])

    def testRoundtripsMultipleProperties(self):
        propertyOne = self.aProperty(propId='123abc')
        propertyTwo = self.aProperty(propId='333111')
        propertyThree = self.aProperty(propId='zza12ff')

        librarian = Librarian()
        librarian.archiveProperties([propertyOne, propertyTwo])
        librarian.archiveProperties([propertyThree])
        properties = librarian.retrieveNewProperties()

        self.assertEqual(3, len(properties))
        self.assertTrue(propertyOne in properties)
        self.assertTrue(propertyTwo in properties)
        self.assertTrue(propertyThree in properties)

    def testAcquiringAnExistingPropertyUpdatesTheInformation(self):
        propertyOne = self.aProperty(price=1000, pubTime=datetime(2011, 9, 18, 21, 54, 32))

        librarian = Librarian()
        librarian.archiveProperties([propertyOne])

        propertyTwo = self.aProperty(price=1250, pubTime=datetime(2011, 9, 18, 22, 54, 32))

        librarian = Librarian()
        librarian.archiveProperties([propertyTwo])

        properties = librarian.retrieveNewProperties()

        self.assertEqual(1, len(properties))
        self.assertEqual(propertyTwo, properties[0])

    def testAPropertyMarkedAsNotInterestingDoesntGetRetrieved(self):
        property = self.aProperty()

        librarian = Librarian()
        librarian.archiveProperties([property])
        librarian.markAsNotInteresting(property.key())

        properties = librarian.retrieveNewProperties()
        self.assertEqual(0, len(properties))
    
    def testAPropertyMarkedAsInterestingIsRetrievedWithTheInterestingOnes(self):
        aProperty = self.aProperty()

        librarian = Librarian()
        librarian.archiveProperties([aProperty])
        librarian.markAsInteresting(aProperty.key())
        properties = librarian.retrieveSavedProperties()

        self.assertEqual(1, len(properties))
        self.assertEqual(aProperty, properties[0])

    def testUpdatingARatedPropertyMaintainsUserPreferences(self):
        librarian = Librarian()
        property = self.aProperty()

        librarian.archiveProperties([property])
        librarian.markAsNotInteresting(property.key())

        librarian.archiveProperties([(self.aProperty())])
        
        properties = librarian.retrieveNewProperties()
        self.assertEqual(0, len(properties))

    def cleanLibrary(self):
        self.cleanPersistenceFile(Librarian.PROPERTIES_LOCATION)
        self.cleanPersistenceFile(Librarian.RATINGS_LOCATION)

    def cleanPersistenceFile(self, file):
        if os.path.exists(file):
            os.remove(file)
