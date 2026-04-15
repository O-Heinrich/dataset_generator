from typing import Union

class Address:
    """Represents an address consisting of a street, housenumber, plz and town."""
    
    def __init__(self, street: str, housenumber: Union[int, str], plz: str, town: str):
        self.street: str = street
        self.housenumber: str = str(housenumber)
        self.plz: str = plz
        self.town: str = town

    def streetHousenumber(self) -> str:
        """Returns a string representation of this addresses street and housenumber combined"""
        return self.street + " " + self.housenumber