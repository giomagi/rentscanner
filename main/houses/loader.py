from main.houses.agents.foxtons import Foxtons
from main.houses.agents.kfh import KFH
from main.houses.agents.knight_frank import KnightFrank
from main.houses.agents.webdadi import LawsonRutter, Chard, Dexters
from main.houses.agents.winkworth import Winkworth
from main.houses.persistence import Librarian
import sys

class Loader(object):
    def __init__(self, config):
        self.config = config

    def agents(self):
        return [Dexters, Chard, LawsonRutter, KFH, KnightFrank, Winkworth, Foxtons]

    def name(self, agent):
        asString = str(agent)
        return asString[asString.rindex('.') + 1:asString.rindex('\'')]

    def loadAll(self):
        for agent in self.agents():
            sys.stdout.write(self.name(agent) + ': ')
            sys.stdout.flush()

            agentInstance = agent()
            newProperties = agentInstance.properties(agentInstance.agentURIs())
            filteredProperties = self.filter(newProperties)
            Librarian(self.config).archiveProperties(filteredProperties)

            sys.stdout.write(str(len(filteredProperties)) + '/' + str(len(newProperties)) + '\n')

    def filter(self, properties):
        return [p for p in properties if self.isInteresting(p)]

    def isInteresting(self, property):
        return property.price.monthlyPrice() > self.config.minMonthlyPrice() and property.price.monthlyPrice() < self.config.maxMonthlyPrice() and property.address.postcode in self.config.interestingZones()
