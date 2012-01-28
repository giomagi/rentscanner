from exceptions import Exception
import locale
import datetime

TIME_FORMAT = '%Y%m%d %H%M%S'

class Rating(object):
    @classmethod
    def NOT_RATED(cls):
        return 'NOT_RATED'

    @classmethod
    def NOT_INTERESTING(cls):
        return 'NOT_INTERESTING'

    @classmethod
    def INTERESTING(cls):
        return 'INTERESTING'

class Property:
    def __init__(self, agent, price, location, link, agentId, publicationDateTime, description, image):
        self.price = price
        self.address = location
        self.agent = agent
        self.agentId = agentId
        self.publicationDateTime = publicationDateTime
        self.link = link
        self.description = description
        self.image = image

    @classmethod
    def unmarshal(cls, propertyAsDictionary):
        return Property(propertyAsDictionary['agent'],
                        Price(locale.atoi(propertyAsDictionary['price']), 'month'),
                        Address(propertyAsDictionary['fulladdress'], propertyAsDictionary['postcode']),
                        propertyAsDictionary['link'],
                        propertyAsDictionary['agentId'],
                        datetime.datetime.strptime(propertyAsDictionary['publicationDateTime'], TIME_FORMAT),
                        propertyAsDictionary['description'],
                        propertyAsDictionary['image'],)

    def marshal(self):
        return {'price' : self.price.monthlyPrice(),
                'fulladdress' : self.address.address,
                'postcode' : self.address.postcode,
                'agent' : self.agent,
                'agentId' : self.agentId,
                'publicationDateTime' : self.publicationDateTime.strftime(TIME_FORMAT),
                'link' : self.link,
                'description' : self.description,
                'image' : self.image}

    @classmethod
    def _key_from(cls, propertyAsDictionary):
        return propertyAsDictionary['agent'] + '_' + propertyAsDictionary['agentId']

    def key(self):
        return self.agent + '_' + str(self.agentId)

    def __str__(self):
        return str(self.address) + ' at ' + str(self.price)

    # TODO: add a valuetype superclass that provides equality methods
    def __eq__(self, other):
        if not isinstance(other, Property):
            return False

        return self.price == other.price and self.address == other.address and self.agent == other.agent and self.agentId == other.agentId and self.publicationDateTime == other.publicationDateTime and self.link == other.link

    def __ne__(self, other):
        return not self.__eq__(other)


class Price:
    def __init__(self, amount, period):
        self.amount = amount
        self.period = self._validatePeriod(period.lower())

    def monthlyPrice(self):
        if self.period == 'week':
            return int(self.amount) * 52 / 12
        else:
            return int(self.amount)

    def _validatePeriod(self, period):
        if period in ('week', 'p/w', 'pw'):
            return 'week'
        elif period in ('month', 'pcm'):
            return 'month'
        else:
            raise Exception, 'Period not supported: ' + period

    # TODO: add a valuetype superclass that provides equality methods
    def __str__(self):
        return str(self.monthlyPrice())

    def __eq__(self, other):
        if not isinstance(other, Price):
            return False

        return self.amount == other.amount and self.period == other.period

    def __ne__(self, other):
        return not self.__eq__(other)


class Address:
    def __init__(self, address, postcode):
        self.postcode = self._validate(postcode)
        self.address = address

    def __str__(self):
        return self.address + ' (' + self.postcode + ')'

    def _validate(self, postcode):
        return postcode if postcode[len(postcode) - 1:].isdigit() else postcode[:len(postcode) - 1]

    # TODO: add a valuetype superclass that provides equality methods
    def __eq__(self, other):
        if not isinstance(other, Address):
            return False

        return self.address == other.address and self.postcode == other.postcode

    def __ne__(self, other):
        return not self.__eq__(other)
