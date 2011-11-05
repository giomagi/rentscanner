from main.houses.foxtons import Foxtons
from main.houses.agents.knight_frank import KnightFrank
from main.houses.agents.winkworth import Winkworth
from main.houses.persistence import Librarian

class Loader():
    def __init__(self):
        self.interestingZones = ("NW1", "NW3", "NW8", "SW1", "SW3", "SW5", "SW6", "SW7", "SW10", "SW11", "W1", "W2", "W8", "W11", "W14", "WC1", "WC2")

    def loadAll(self):
        for agent in [Foxtons, Winkworth, KnightFrank]:
            print 'Start ' + str(agent)
            newProperties = agent().properties()
            print 'Found ' + str(len(newProperties)) + ' properties'
            Librarian().archiveProperties(self.filter(newProperties))
            print 'Done ' + str(agent)

    def filter(self, properties):
        filtered = [p for p in properties if self.isInteresting(p)]
        print 'Left ' + str(len(filtered)) + ' properties after filtering'
        return filtered

    def isInteresting(self, property):
        return property.price.monthlyPrice() > 1300 and property.price.monthlyPrice() < 2200 and property.address.postcode in self.interestingZones
