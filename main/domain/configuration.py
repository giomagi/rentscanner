class Configuration(object):
    @classmethod
    def dummy(cls):
        return Configuration({
            'propertiesArchive' : '',
            'ratingsArchive' : '',
            'webServerAddress' : '',
            'webServerPort' : ''
        })

    @classmethod
    def test(cls):
        return Configuration({
            'propertiesArchive' : '/var/gio/rentscanner/test/properties.data',
            'ratingsArchive' : '/var/gio/rentscanner/test/ratings.data',
            'webServerAddress' : '192.168.1.77',
            'webServerPort' : 5678
        })

    @classmethod
    def prod(cls):
        return Configuration({
            'propertiesArchive' : '/var/gio/rentscanner/properties.data',
            'ratingsArchive' : '/var/gio/rentscanner/ratings.data',
            'webServerAddress' : '192.168.1.77',
            'webServerPort' : 1234
        })

    def __init__(self, props):
        self.props = props

    def minMonthlyPrice(self):
        return 1300

    def maxMonthlyPrice(self):
        return 2200

    def interestingZones(self):
        return "NW1", "NW3", "NW8", "SW1", "SW3", "SW5", "SW6", "SW7", "SW10", "SW11", "W1", "W2", "W8", "W11", "W14", "WC1", "WC2"

    def propertiesArchive(self):
        return self.props['propertiesArchive']

    def ratingsArchive(self):
        return self.props['ratingsArchive']

    def webServerAddress(self):
        return self.props['webServerAddress']

    def webServerPort(self):
        return self.props['webServerPort']
