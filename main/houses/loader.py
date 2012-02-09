import datetime
from main.houses.agents.douglas_and_gordon import DouglasAndGordon
from main.houses.agents.faron_sutaria import FaronSutaria
from main.houses.agents.foxtons import Foxtons
from main.houses.agents.kfh import KFH
from main.houses.agents.knight_frank import KnightFrank
from main.houses.agents.marsh_and_parsons import MarshAndParsons
from main.houses.agents.webdadi import Chard, Dexters, LawsonRutter
from main.houses.agents.winkworth import Winkworth
from main.houses.persistence import Librarian, LoadLogger

class Loader(object):
    def __init__(self, config):
        self.config = config

    def agents(self):
        return [FaronSutaria, MarshAndParsons, DouglasAndGordon, Dexters, Chard, LawsonRutter, KFH, KnightFrank, Winkworth, Foxtons]

    def name(self, agent):
        asString = str(agent)
        return asString[asString.rindex('.') + 1:asString.rindex('\'')]

    def loadAll(self):
        loadingStats = {'startTime' : datetime.datetime.now()}

        for agent in self.agents():
            agentInstance = agent()
            allProperties, errors = agentInstance.properties(agentInstance.agentURIs())
            filteredProperties = self.filter(allProperties)
            Librarian(self.config).archiveProperties(filteredProperties)

            loadingStats[self.name(agent)] = {'found' : len(allProperties),
                                              'loaded' : len(filteredProperties),
                                              'errors' : errors}

        loadingStats['endTime'] = datetime.datetime.now()
        LoadLogger(self.config).log(loadingStats)

    def filter(self, properties):
        return [p for p in properties if self.isInteresting(p)]

    def isInteresting(self, property):
        return self.config.minMonthlyPrice() < property.price.monthlyPrice() < self.config.maxMonthlyPrice() and property.address.postcode in self.config.interestingZones()
