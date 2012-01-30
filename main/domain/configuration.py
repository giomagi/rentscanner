import socket

class Configuration(object):
    @classmethod
    def dummy(cls):
        return Configuration({
            'env': '',
            'webServerAddress': '',
            'webServerPort': ''
        })

    @classmethod
    def test(cls):
        return Configuration({
            'env': 'test',
            'webServerAddress': '127.0.0.1',
            'webServerPort': 5678
        })

    @classmethod
    def prod(cls):
        return Configuration({
            'env' : 'prod',
            'webServerAddress': 'ec2-46-137-39-213.eu-west-1.compute.amazonaws.com',
            'webServerPort': 1234
        })

    @classmethod
    def getLocalIpAddress(cls):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('google.com', 0))
        return s.getsockname()[0]

    def __init__(self, props):
        self.props = props

    def minMonthlyPrice(self):
        return 1300

    def maxMonthlyPrice(self):
        return 2200

    def interestingZones(self):
        return "NW1", "NW3", "NW8", "SW1", "SW3", "SW5", "SW6", "SW7", "SW10", "SW11", "W1", "W2", "W8", "W11", "W14", "WC1", "WC2"

    def awsRegion(self):
        return 'eu-west-1'

    def propertiesDomain(self):
        return self.props['env'] + 'properties'

    def ratingsDomain(self):
        return self.props['env'] + 'ratings'

    def webServerAddress(self):
        return self.props['webServerAddress']

    def webServerPort(self):
        return self.props['webServerPort']

