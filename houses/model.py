from exceptions import Exception

class Property:
    def __init__(self, price, location):
        if price[1] == 'week':
            self.price = int(price[0]) * 52 / 12
        else:
            self.price = int(price[0])

        self.address = location

    def __str__(self):
        return str(self.address) + " at " + str(self.price)


class Address:
    LondonPostCodes = ("E1", "E1W", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10", "E11", "E12", "E13", "E14", "E15", "E16", "E17", "E18", "E19", "E20",
                       "EC1", "EC2", "EC3", "EC4",
                       "N1", "N2", "N3", "N4", "N5", "N6", "N7", "N8", "N9", "N10", "N11", "N12", "N13", "N14", "N15", "N16", "N17", "N18", "N19", "N20", "N21", "N22",
                       "NW1", "NW2", "NW3", "NW4", "NW5", "NW6", "NW7", "NW8", "NW9", "NW10", "NW11",
                       "SE1", "SE2", "SE3", "SE4", "SE5", "SE6", "SE7", "SE8", "SE9", "SE10", "SE11", "SE12", "SE13", "SE14", "SE15", "SE16", "SE17", "SE18", "SE19", "SE20", "SE21", "SE22", "SE23", "SE24", "SE25", "SE26", "SE27", "SE28",
                       "SW1", "SW2", "SW3", "SW4", "SW5", "SW6", "SW7", "SW8", "SW9", "SW10", "SW11", "SW12", "SW13", "SW14", "SW15", "SW16", "SW17", "SW18", "SW19", "SW20",
                       "W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8", "W9", "W10", "W11", "W12", "W13", "W14",
                       "WC1", "WC2")

    def __init__(self, address, postcode):
        self._validate(postcode)

        self.postcode = postcode
        self.address = address

    def __str__(self):
        return self.address + " (" + self.postcode + ")"

    def _validate(self, postcode):
        code = postcode if postcode[len(postcode) - 1:].isdigit() else postcode[:len(postcode) - 1]
        if code not in self.LondonPostCodes:
            raise Exception, postcode + " is not a valid London post code"
