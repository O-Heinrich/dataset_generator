from typing import Union

class Address:
    def __init__(self, street: str, housenumber: Union[int, str], plz: str, town: str):
        self.street: str = street
        self.housenumber: str = str(housenumber)
        self.plz: str = plz
        self.town: str = town

    def streetHousenumber(self) -> str:
        return self.street + " " + self.housenumber