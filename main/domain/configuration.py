class Configuration:
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

    def propertiesArchive(self):
        return self.props['propertiesArchive']

    def ratingsArchive(self):
        return self.props['ratingsArchive']

    def webServerAddress(self):
        return self.props['webServerAddress']

    def webServerPort(self):
        return self.props['webServerPort']
