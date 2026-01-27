class Address:
    def __init__(self, street, housenumber, plz, town):
        self.street = street
        self.housenumber = int(housenumber)
        self.plz = plz
        self.town = town