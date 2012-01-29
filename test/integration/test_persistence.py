from datetime import datetime
import os
import unittest
import boto.sdb
import time
from main.domain.configuration import Configuration
from main.houses.persistence import Librarian
from test.support.test_utils import PropertyMaker

class TestPersistence(unittest.TestCase, PropertyMaker):
    def setUp(self):
        config = Configuration.test()
        self._cleanupTestDb(config)
        self.librarian = Librarian(config)

    def _cleanupTestDb(self, config):
        connection = boto.sdb.connect_to_region(config.awsRegion())
        for d in [connection.get_domain(config.propertiesDomain()), connection.get_domain(config.ratingsDomain())]:
            for i in d.select('select * from ' + d.name):
                d.delete_item(i)

    def _aLittlePauseToAllowForEventualConsistency(self):
        time.sleep(1)

    def testRoundtripsAProperty(self):
        aProperty = self.aProperty()

        self.librarian.archiveProperties([aProperty])
        self._aLittlePauseToAllowForEventualConsistency()
        properties = self.librarian.retrieveNewProperties()

        self.assertEqual(1, len(properties))
        self.assertEqual(aProperty, properties[0])

    def testAcquiringAnExistingPropertyUpdatesTheInformation(self):
        propertyOne = self.aProperty(price=1000, pubTime=datetime(2011, 9, 18, 21, 54, 32))

        self.librarian.archiveProperties([propertyOne])

        propertyTwo = self.aProperty(price=1250, pubTime=datetime(2011, 9, 18, 22, 54, 32))

        self.librarian.archiveProperties([propertyTwo])

        self._aLittlePauseToAllowForEventualConsistency()
        properties = self.librarian.retrieveNewProperties()

        self.assertEqual(1, len(properties))
        self.assertEqual(propertyTwo, properties[0])

    def testRetrievalForNewProperties(self):
        propertyOne = self.aProperty(propId='123abc')
        propertyTwo = self.aProperty(propId='333111')
        propertyThree = self.aProperty(propId='zza12ff')

        self.librarian.archiveProperties([propertyOne, propertyTwo])
        self.librarian.archiveProperties([propertyThree])

        self._aLittlePauseToAllowForEventualConsistency()
        properties = self.librarian.retrieveNewProperties()

        self.assertEqual([], self.librarian.retrieveDiscardedProperties())
        self.assertEqual([], self.librarian.retrieveSavedProperties('both'))

        self.assertEqual(3, len(properties))
        self.assertTrue(propertyOne in properties)
        self.assertTrue(propertyTwo in properties)
        self.assertTrue(propertyThree in properties)

    def testRetrievalForNotInterestingProperties(self):
        property = self.aProperty()

        self.librarian.archiveProperties([property])
        self.librarian.markAsNotInteresting(property.key())

        self._aLittlePauseToAllowForEventualConsistency()
        self.assertEqual([], self.librarian.retrieveNewProperties())
        self.assertEqual([], self.librarian.retrieveSavedProperties('both'))

        properties = self.librarian.retrieveDiscardedProperties()
        self.assertEqual(1, len(properties))
        self.assertEqual(property, properties[0])

    def testRetrievalForInterestingProperties(self):
        aProperty = self.aProperty()

        self.librarian.archiveProperties([aProperty])
        self.librarian.markAsInteresting(aProperty.key(), 'gio')

        self._aLittlePauseToAllowForEventualConsistency()
        properties = self.librarian.retrieveSavedProperties('gio')

        self.assertEqual([], self.librarian.retrieveNewProperties())
        self.assertEqual([], self.librarian.retrieveDiscardedProperties())
        self.assertEqual([], self.librarian.retrieveSavedProperties('sara'))
        self.assertEqual([], self.librarian.retrieveSavedProperties('both'))

        self.assertEqual(1, len(properties))
        self.assertEqual(aProperty, properties[0])

        self.librarian.markAsInteresting(aProperty.key(), 'sara')
        self._aLittlePauseToAllowForEventualConsistency()

        properties = self.librarian.retrieveSavedProperties('both')

        self.assertEqual([], self.librarian.retrieveNewProperties())
        self.assertEqual([], self.librarian.retrieveDiscardedProperties())
        self.assertEqual([], self.librarian.retrieveSavedProperties('sara'))
        self.assertEqual([], self.librarian.retrieveSavedProperties('gio'))

        self.assertEqual(1, len(properties))
        self.assertEqual(aProperty, properties[0])

    def testUpdatingARatedPropertyMaintainsUserPreferences(self):
        property = self.aProperty()

        self.librarian.archiveProperties([property])
        self.librarian.markAsNotInteresting(property.key())

        self.librarian.archiveProperties([(self.aProperty())])

        self._aLittlePauseToAllowForEventualConsistency()
        properties = self.librarian.retrieveNewProperties()
        self.assertEqual(0, len(properties))
