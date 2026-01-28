from faker import Faker
from wonderwords import RandomWord
from datatypes import Datatype as Dt
import generators.nameGenerator as ng
import generators.address_generator as ag
import generators.numbers_generator as numg
import random

class Column:
    def __init__(self, name, type, metadata={}):
        if not isinstance(type, Dt) or not isinstance(metadata, dict):
            raise TypeError()
        self.name = name
        self.type = type
        self.metadata = metadata

    def getGenerator(self, fake):
        if not isinstance(fake, Faker):
            raise TypeError()
        if self.type == Dt.FIRST_NAME:
            return lambda: ng.generateFirstName(fake)
        elif self.type == Dt.LAST_NAME:
            return lambda: ng.generateLastName(fake)
        elif self.type == Dt.FULL_NAME:
            return lambda: ng.generateFullName(fake)
        elif self.type == Dt.COMPANY_NAME:
            return lambda: ag.generateCompanyName(fake)
        elif self.type == Dt.STREET:
            return lambda: ag.generateAddress(fake).street
        elif self.type == Dt.STREET_HOUSENUMBER:
            return lambda: ag.generateAddress(fake).streetHousenumber()
        elif self.type == Dt.HOUSENUMBER:
            return lambda: ag.generateAddress(fake).housenumber
        elif self.type == Dt.TOWN:
            return lambda: ag.generateAddress(fake).town
        elif self.type == Dt.PLZ:
            return lambda: ag.generateAddress(fake).plz
        elif self.type == Dt.FULL_ADDRESS:
            return lambda: ag.generateAddress(fake)
        elif self.type == Dt.MONEY:
            return lambda min, max: numg.generateFloat(min, max)
        elif self.type == Dt.INTEGER:
            return lambda min, max: random.randrange(min, max)
        elif self.type == Dt.FLOAT:
            return lambda min, max, acc: numg.generateFloat(min, max, acc)
        elif self.type == Dt.DATE:
            return lambda: numg.generateDate(fake)
        elif self.type == Dt.TIME:
            return lambda: numg.generateTime(fake)
        elif self.type == Dt.DATE_TIME:
            return lambda: numg.generateDateTime(fake)
        elif self.type == Dt.VALUES:
            values = self.metadata.get("values")
            if values is None or not isinstance(values, list):
                raise ValueError("For Values Type there must be metadata for the values")
            return lambda: values[random.randrange(len(values))]
        elif self.type == Dt.FORMAT_STRING:
            return #TODO
        elif self.type == Dt.RANDOM_STRING:
            r = RandomWord()
            return lambda: r.word()
        else:
            raise NotImplementedError()

    def getListGenerator(self, fake):
        unique = self.metadata.get("unique", False)
        maxUniqueFailsMultiplier = self.metadata.get("mufm", 3)
        
        if not isinstance(fake, Faker):
            raise TypeError()
        if self.type == Dt.FIRST_NAME:
            return lambda size: ng.generateFirstNameList(fake, size, unique, maxUniqueFailsMultiplier)
        elif self.type == Dt.LAST_NAME:
            return lambda size: ng.generateLastNameList(fake, size, unique, maxUniqueFailsMultiplier)
        elif self.type == Dt.FULL_NAME:
            return lambda size: ng.generateFullNameList(fake, size, unique, maxUniqueFailsMultiplier)
        elif self.type == Dt.COMPANY_NAME:
            return lambda size: ag.generateCompanyNameList(fake, size, unique, maxUniqueFailsMultiplier)
        elif self.type == Dt.STREET:
            return lambda size: [c.street for c in ag.generateAddressList(fake, size)]
        elif self.type == Dt.STREET_HOUSENUMBER:
            return lambda size: [c.streetHousenumber() for c in ag.generateAddressList(fake, size)]
        elif self.type == Dt.HOUSENUMBER:
            return lambda size: [c.housenumber for c in ag.generateAddressList(fake, size)]
        elif self.type == Dt.TOWN:
            return lambda size: [c.town for c in ag.generateAddressList(fake, size)]
        elif self.type == Dt.PLZ:
            return lambda size: [c.plz for c in ag.generateAddressList(fake, size)]
        elif self.type == Dt.FULL_ADDRESS:
            return lambda size: ag.generateAddressList(fake, size)
        elif self.type == Dt.MONEY:
            return lambda size, min, max: numg.generateFloatList(size, min, max)
        elif self.type == Dt.INTEGER:
            return lambda size, min, max: [random.randrange(min, max) for _ in range(size)]
        elif self.type == Dt.FLOAT:
            return lambda size, min, max, acc: numg.generateFloatList(size, min, max, acc)
        elif self.type == Dt.DATE:
            return lambda size: numg.generateDateList(fake, size, unique, maxUniqueFailsMultiplier)
        elif self.type == Dt.TIME:
            return lambda size: numg.generateTimeList(fake, size, unique, maxUniqueFailsMultiplier)
        elif self.type == Dt.DATE_TIME:
            return lambda size: numg.generateDateTimeList(fake, size, unique, maxUniqueFailsMultiplier)
        elif self.type == Dt.VALUES:
            values = self.metadata.get("values")
            if values is None or not isinstance(values, list):
                raise ValueError("For Values Type there must be metadata for the values")
            return lambda size: [values[random.randrange(len(values))] for _ in range(size)]
        elif self.type == Dt.FORMAT_STRING:
            return #TODO
        elif self.type == Dt.RANDOM_STRING:
            r = RandomWord()
            return lambda size: [r.word() for _ in range(size)]
        else:
            raise NotImplementedError()