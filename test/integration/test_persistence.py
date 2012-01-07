from datetime import datetime
import os
import unittest
from main.domain.configuration import Configuration
from main.houses.persistence import Librarian
from test.support.test_utils import PropertyMaker

class TestPersistence(unittest.TestCase, PropertyMaker):
    def setUp(self):
        config = Configuration.test()
        self.removeIfExists(config.propertiesArchive())
        self.removeIfExists(config.ratingsArchive())

        self.librarian = Librarian(config)

    def testRoundtripsAProperty(self):
        aProperty = self.aProperty()

        self.librarian.archiveProperties([aProperty])
        properties = self.librarian.retrieveNewProperties()

        self.assertEqual(1, len(properties))
        self.assertEqual(aProperty, properties[0])

    def testAcquiringAnExistingPropertyUpdatesTheInformation(self):
        propertyOne = self.aProperty(price=1000, pubTime=datetime(2011, 9, 18, 21, 54, 32))

        self.librarian.archiveProperties([propertyOne])

        propertyTwo = self.aProperty(price=1250, pubTime=datetime(2011, 9, 18, 22, 54, 32))

        self.librarian.archiveProperties([propertyTwo])

        properties = self.librarian.retrieveNewProperties()

        self.assertEqual(1, len(properties))
        self.assertEqual(propertyTwo, properties[0])

    def testRetrievalForNewProperties(self):
        propertyOne = self.aProperty(propId='123abc')
        propertyTwo = self.aProperty(propId='333111')
        propertyThree = self.aProperty(propId='zza12ff')

        self.librarian.archiveProperties([propertyOne, propertyTwo])
        self.librarian.archiveProperties([propertyThree])
        properties = self.librarian.retrieveNewProperties()

        self.assertEqual([], self.librarian.retrieveDiscardedProperties())
        self.assertEqual([], self.librarian.retrieveSavedProperties())

        self.assertEqual(3, len(properties))
        self.assertTrue(propertyOne in properties)
        self.assertTrue(propertyTwo in properties)
        self.assertTrue(propertyThree in properties)

    def testRetrievalForNotInterestingProperties(self):
        property = self.aProperty()

        self.librarian.archiveProperties([property])
        self.librarian.markAsNotInteresting(property.key())

        self.assertEqual([], self.librarian.retrieveNewProperties())
        self.assertEqual([], self.librarian.retrieveSavedProperties())

        properties = self.librarian.retrieveDiscardedProperties()
        self.assertEqual(1, len(properties))
        self.assertEqual(property, properties[0])

    def testRetrievalForInterestingProperties(self):
        aProperty = self.aProperty()

        self.librarian.archiveProperties([aProperty])
        self.librarian.markAsInteresting(aProperty.key())
        properties = self.librarian.retrieveSavedProperties()

        self.assertEqual([], self.librarian.retrieveNewProperties())
        self.assertEqual([], self.librarian.retrieveDiscardedProperties())

        self.assertEqual(1, len(properties))
        self.assertEqual(aProperty, properties[0])

    def testUpdatingARatedPropertyMaintainsUserPreferences(self):
        property = self.aProperty()

        self.librarian.archiveProperties([property])
        self.librarian.markAsNotInteresting(property.key())

        self.librarian.archiveProperties([(self.aProperty())])

        properties = self.librarian.retrieveNewProperties()
        self.assertEqual(0, len(properties))

    def removeIfExists(self, file):
        if os.path.exists(file):
            os.remove(file)
