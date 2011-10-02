from datetime import datetime
import os
import unittest
from main.houses.model import Property, Price, Address
from main.houses.persistence import Librarian

class TestPersistence(unittest.TestCase):
    def setUp(self):
        self.cleanLibrary()

    def testRoundtripsAProperty(self):
        aProperty = Property('AGENT', Price(1000, 'month'), Address('some place', 'SW6'), 'http://property_link',
                             '123abc', datetime(2011, 9, 18, 21, 54, 32))

        librarian = Librarian()
        librarian.archiveProperties([aProperty])
        properties = librarian.retrieveProperties()

        self.assertEqual(1, len(properties))
        self.assertEqual(aProperty, properties[0])

    def testRoundtripsMultipleProperties(self):
        propertyOne = Property('AGENT', Price(1000, 'month'), Address('some place', 'SW6'), 'http://property_link',
                               '123abc', datetime(2011, 9, 18, 21, 54, 32))
        propertyTwo = Property('AGENT', Price(1200, 'month'), Address('another place', 'NW1'), 'http://property_link_2',
                               '333111', datetime(2011, 9, 18, 21, 54, 36))
        propertyThree = Property('AGENT', Price(1000, 'week'), Address('a different place', 'WC1N'), 'http://linkz',
                                 'zza12ff', datetime(2011, 9, 18, 22, 54, 32))

        librarian = Librarian()
        librarian.archiveProperties([propertyOne, propertyTwo])
        librarian.archiveProperties([propertyThree])
        properties = librarian.retrieveProperties()

        self.assertEqual(3, len(properties))
        self.assertTrue(propertyOne in properties)
        self.assertTrue(propertyTwo in properties)
        self.assertTrue(propertyThree in properties)

    def testAcquiringAnExistingPropertyUpdatesTheInformation(self):
        propertyOne = Property('AGENT', Price(1000, 'month'), Address('some place', 'SW6'), 'http://property_link',
                               '123abc', datetime(2011, 9, 18, 21, 54, 32))

        librarian = Librarian()
        librarian.archiveProperties([propertyOne])

        propertyTwo = Property('AGENT', Price(1250, 'month'), Address('some place', 'SW6'), 'http://property_link',
                               '123abc', datetime(2011, 9, 18, 22, 54, 32))

        librarian = Librarian()
        librarian.archiveProperties([propertyTwo])

        properties = librarian.retrieveProperties()

        self.assertEqual(1, len(properties))
        self.assertEqual(propertyTwo, properties[0])

    def testAPropertyMarkedAsNotInterestingDoesntGetRetrieved(self):
        propertyOne = Property('AGENT', Price(1000, 'month'), Address('some place', 'SW6'), 'http://property_link',
                               '123abc', datetime(2011, 9, 18, 21, 54, 32))

        librarian = Librarian()
        librarian.archiveProperties([propertyOne])
        librarian.markAsNotInteresting('AGENT', '123abc')

        properties = librarian.retrieveProperties()
        self.assertEqual(0, len(properties))

    def testUpdatingARatedPropertyMaintainsUserPreferences(self):
        librarian = Librarian()
        librarian.archiveProperties([
            (Property('AGENT', Price(1000, 'month'), Address('some place', 'SW6'), 'http://property_link',
                      '123abc', datetime(2011, 9, 18, 21, 54, 32)))])

        librarian.markAsNotInteresting('AGENT', '123abc')

        librarian.archiveProperties([
            (Property('AGENT', Price(1000, 'month'), Address('some place', 'SW6'), 'http://property_link',
                      '123abc', datetime(2011, 9, 18, 21, 54, 32)))])
        
        properties = librarian.retrieveProperties()
        self.assertEqual(0, len(properties))

    def cleanLibrary(self):
        if os.path.exists(Librarian.LIBRARY_LOCATION):
            os.remove(Librarian.LIBRARY_LOCATION)