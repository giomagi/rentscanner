import boto.sdb
import sys
from main.houses.model import Rating, Property

ratingsCache = {}

def initRatingsCacheIfEmpty(propertiesDomain, ratingsDomain):
    global ratingsCache
    if not ratingsCache:
        sys.stdout.write('Loading ratings cache, you should see this message in the logs only once per run... ')
        sys.stdout.flush()
        ratingsCache = dict([(propKey, ratingsDomain.get_item(propKey)['rating']) for propKey in [Property._key_from(prop) for prop in propertiesDomain.select('select * from ' + propertiesDomain.name)] if ratingsDomain.get_item(propKey)])
        sys.stdout.write('done')
        sys.stdout.flush()

class LoadLogger(object):
    def __init__(self, config):
        self.loggingDomain = boto.sdb.connect_to_region(config.awsRegion()).get_domain(config.logginDomain())

    def log(self, stats):
        self.loggingDomain.put_attributes('latest', stats)
        self.loggingDomain.put_attributes(stats['startTime'].strftime('%Y%m%d%H%M'), stats)


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
        self.markAs(propertyId, who if propertyId not in ratingsCache or ratingsCache[propertyId] == who else 'both')

    def markAsSeen(self, propertyId):
        self.markAs(propertyId, 'seen')
