from faker import Faker
from wonderwords import RandomWord
from enums.datatypes import Datatype as Dt
import backend.nameGenerator as ng
import backend.addressGenerator as ag
import backend.numbersGenerator as numg
import random
from rstr import xeger
from backend.columnListener import ColumnListener
from backend.metadata import Metadata

from typing import Any
from typing import Optional

class Column:
    nextkey = "nextkey"

    def __init__(self, name: str, type: Dt, metadata: dict[str, Any]={}):
        self.name: str = name
        self.type: Dt = type
        self.metadata: Metadata = Metadata(metadata)
        self.randomword: Optional[RandomWord] = None
        if type == Dt.RANDOM_STRING:
            self.randomword = RandomWord()
        self.listeners: list[ColumnListener] = []
        self.listener: Optional[ColumnListener] = None
        self.ownTable: bool = False
        
    def getValue(self, fake: Faker, id: Optional[int]=None, fKeys: dict[str, int]={}) -> Any:
        value = self.generateValue(fake, fKeys, id)
        if len(self.listeners) >= 1:
            if id is None:
                raise KeyError("ID cannot be None")
            for l in self.listeners:
                l.add(id, value)
        return value

    def generateValue(self, fake: Faker, fKeys: dict[str, int]={}, thisId: Optional[int]=None) -> Any:
        if self.type == Dt.FIRST_NAME:
            return ng.generateFirstName(fake)
        elif self.type == Dt.LAST_NAME:
            return ng.generateLastName(fake)
        elif self.type == Dt.FULL_NAME:
            return ng.generateFullName(fake)
        elif self.type == Dt.COMPANY_NAME:
            return ag.generateCompanyName(fake)
        elif self.type == Dt.STREET:
            return ag.generateAddress(fake).street
        elif self.type == Dt.STREET_HOUSENUMBER:
            return ag.generateAddress(fake).streetHousenumber()
        elif self.type == Dt.HOUSENUMBER:
            return ag.generateAddress(fake).housenumber
        elif self.type == Dt.TOWN:
            return ag.generateAddress(fake).town
        elif self.type == Dt.PLZ:
            return ag.generateAddress(fake).plz
        elif self.type == Dt.MONEY:
            return numg.generateFloat(self.metadata.min(), self.metadata.max())
        elif self.type == Dt.INTEGER:
            return random.randrange(self.metadata.min(), self.metadata.max())
        elif self.type == Dt.FLOAT:
            return numg.generateFloat(self.metadata.min(), self.metadata.max(), self.metadata.acc())
        elif self.type == Dt.DATE:
            return numg.generateDate(fake, start=self.metadata.start(), end=self.metadata.end())
        elif self.type == Dt.TIME:
            return numg.generateTime(fake, startTime=self.metadata.startTime(), endTime=self.metadata.endTime(), timeRounding=self.metadata.timeRounding())
        elif self.type == Dt.DATE_TIME:
            return numg.generateDateTime(fake, start=self.metadata.start(), end=self.metadata.end(), startTime=self.metadata.startTime(), endTime=self.metadata.endTime(), timeRounding=self.metadata.timeRounding())
        elif self.type == Dt.VALUES:
            values = self.metadata.values()
            if values is None or not isinstance(values, list) or len(values) < 1:
                raise ValueError("For Values Type there must be metadata for the values")
            return random.choice(values)
        elif self.type == Dt.FORMAT_STRING:
            reg: Optional[str] = self.metadata.regex()
            if reg is None:
                raise ValueError("No Regex given")
            return xeger(reg)
        elif self.type == Dt.RANDOM_STRING:
            if self.randomword is None:
                raise TypeError()
            return self.randomword.word()
        elif self.type == Dt.PRIMARY_KEY:
            id = self.metadata.nextkey()
            self.metadata.incrementKey()
            return id

        # Types depending on another column
        elif self.type.value >= 2000:
            if self.listener is None:
                raise TypeError()
            if self.type == Dt.FOREIGN_KEY:
                fKey: int = self.listener.randomKey()
                fKeys[self.metadata.foreignColumn()] = fKey
                return fKey
            val: Any = None
            if self.ownTable:
                if thisId is None:
                    raise KeyError(f'No key given')
                val = self.listener.get(thisId)
            else:
                fk: Optional[int] = fKeys.get(self.metadata.foreignKeyColumn())
                if fk is None:
                    raise KeyError(f'No key given for column {self.name}')
                val = self.listener.get(fk)
            diff: int = self.metadata.diff()

            if self.type == Dt.LOWERTHAN_DATE:
                return numg.generateDate(fake, start=self.metadata.getStartWithMaxdiff(val), end=val - self.metadata.timeDiff())
            elif self.type == Dt.HIGHERTHAN_DATE:
                return numg.generateDate(fake, start=val + self.metadata.timeDiff(), end=self.metadata.getEndWithMaxdiff(val))
            elif self.type == Dt.LOWERTHAN_INTEGER:
                return numg.generateInt(self.metadata.getMinWithMaxdiff(val), val - diff)
            elif self.type == Dt.HIGHERTHAN_INTEGER:
                return numg.generateInt(val + diff, self.metadata.getMaxWithMaxdiff(val))
            elif self.type == Dt.LOWERTHAN_FLOAT:
                return numg.generateFloat(self.metadata.getMinWithMaxdiff(val), val - diff, self.metadata.acc())
            elif self.type == Dt.HIGHERTHAN_FLOAT:
                return numg.generateFloat(val + diff, self.metadata.getMaxWithMaxdiff(val), self.metadata.acc())
            else:
                raise NotImplementedError()
            
        else:
            raise NotImplementedError()
    
    def predictKey(self) -> int:
        if self.type == Dt.PRIMARY_KEY:
            return self.metadata.nextkey()
        raise TypeError("Can only predict key for primary key columns")

    def addListener(self, listener):
        self.listeners.append(listener)

    def listenTo(self, listener):
        self.listener = listener

    def __str__(self):
        return self.name