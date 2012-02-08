import boto.sdb
from main.domain.configuration import Configuration
from main.houses.model import Rating, Property

ratingsCache = {}

def initRatingsCacheIfEmpty(propertiesDomain, ratingsDomain):
    global ratingsCache
    if not ratingsCache:
        print 'Loading ratings cache, you should see this message in the logs only once per run'
        ratingsCache = dict([(propKey, ratingsDomain.get_item(propKey)['rating']) for propKey in [Property._key_from(prop) for prop in propertiesDomain.select('select * from ' + propertiesDomain.name)] if ratingsDomain.get_item(propKey)])


class Librarian(object):
    def __init__(self, config):
        connection = boto.sdb.connect_to_region(config.awsRegion())
        self.properties = connection.get_domain(config.propertiesDomain())
        self.ratings = connection.get_domain(config.ratingsDomain())
        initRatingsCacheIfEmpty(self.properties, self.ratings)

    def archiveProperties(self, properties):
        for i in xrange(0, len(properties), 25):
            self.properties.batch_put_attributes(dict((p.key(), p.marshal()) for p in properties[i : i + 25]))

    def retrieveNewProperties(self):
        return [Property.unmarshal(p) for p in self.properties.select('select * from ' + self.properties.name) if Property._key_from(p) not in ratingsCache]

    def retrievePropertiesWithRating(self, desiredRating):
        return [Property.unmarshal(p) for p in self.properties.select('select * from ' + self.properties.name) if Property._key_from(p) in ratingsCache and ratingsCache[Property._key_from(p)] == desiredRating]

    def retrieveSavedProperties(self, who):
        return self.retrievePropertiesWithRating(who)

    def retrieveDiscardedProperties(self):
        return self.retrievePropertiesWithRating(Rating.NOT_INTERESTING())

    def markAs(self, propertyId, rating):
        self.ratings.put_attributes(propertyId, {'rating' : rating})
        ratingsCache[propertyId] = rating

    def markAsNotInteresting(self, propertyId):
        self.markAs(propertyId, Rating.NOT_INTERESTING())

    def markAsInteresting(self, propertyId, who):
        self.markAs(propertyId, who if who == 'seen' or propertyId not in ratingsCache or ratingsCache[propertyId] == who else 'both')
