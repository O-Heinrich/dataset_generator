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
from datetime import datetime, time, date
from typing import Any, Optional, Union

class Column:
    """Represents one column in a TableModel and consists of a name, a Datatype and Metadata."""

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
        """
        Generates and returns a single generated value.
        If this Column has ColumnListeners listening to it, id shall not be None and the value is passed to those ColumnListeners.
        The fKeys dictionary is a mapping of names of FOREIGN_KEY Columns, to their relevant generated id.
        The fKeys dictionary is modified if this Column has the Datatypoe FOREIGN_KEY.
        """
        value = self._generateValue(fake, fKeys, id)
        if len(self.listeners) >= 1:
            if id is None:
                raise KeyError("ID cannot be None")
            for l in self.listeners:
                l.add(id, value)
        return value

    def _generateValue(self, fake: Faker, fKeys: dict[str, int]={}, thisId: Optional[int]=None) -> Any:
        """Generates a single value for this Column."""
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
            key: int = self.metadata.nextkey()
            self.metadata.incrementKey()
            return key

        # Types depending on another column
        elif self.type.value >= 2000:
            if self.listener is None:
                raise TypeError()
            if self.type == Dt.FOREIGN_KEY:
                fKey: int = self.listener.randomKey()
                fKeys[self.metadata.foreignColumn()] = fKey # Register this FOREIGN_KEYs value to the fKeys dictionary.
                return fKey
            val: Any = None
            if self.ownTable:
                if thisId is None:
                    raise KeyError("No key given")
                val = self.listener.get(thisId)
            else:
                fk: Optional[int] = fKeys.get(self.metadata.foreignKeyColumn())
                if fk is None:
                    raise KeyError(f'No key given for column {self.name}')
                val = self.listener.get(fk)
            diff: int = self.metadata.diff()

            if self.type == Dt.LOWERTHAN_DATE:
                assert isinstance(val, (datetime, date))
                return numg.generateDate(fake, start=self.metadata.getStartWithMaxdiff(val), end=val - self.metadata.timeDiff())
            elif self.type == Dt.HIGHERTHAN_DATE:
                assert isinstance(val, (datetime, date))
                return numg.generateDate(fake, start=val + self.metadata.timeDiff(), end=self.metadata.getEndWithMaxdiff(val))
            elif self.type == Dt.LOWERTHAN_TIME:
                assert isinstance(val, (datetime, time))
                if isinstance(val, time):
                    val = datetime.combine(date.today(), val)
                return numg.generateTime(fake, startTime=self.metadata.getStartTimeWithMaxDiff(val), endTime=(val - self.metadata.timeDiff()).strftime("%H:%M:%S"), timeRounding=self.metadata.timeRounding())
            elif self.type == Dt.HIGHERTHAN_TIME:
                assert isinstance(val, (datetime, time))
                if isinstance(val, time):
                    val = datetime.combine(date.today(), val)
                return numg.generateTime(fake, startTime=(val + self.metadata.timeDiff()).strftime("%H:%M:%S"), endTime=self.metadata.getEndTimeWithMaxDiff(val), timeRounding=self.metadata.timeRounding())
            elif self.type == Dt.LOWERTHAN_DATETIME or self.type == Dt.HIGHERTHAN_DATETIME:
                assert isinstance(val, (datetime, date))
                s: Union[datetime, date, str]
                e: Union[datetime, date, str]
                if self.type == Dt.LOWERTHAN_DATETIME:
                    s = self.metadata.getStartWithMaxdiff(val)
                    e = val - self.metadata.timeDiff()
                else:
                    s = val + self.metadata.timeDiff()
                    e = self.metadata.getEndWithMaxdiff(val)
                return numg.generateDateTime(fake, start=s, end=e, timeRounding=self.metadata.timeRounding())
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
        """Returns the unique integer key, that will be generated for this Column next."""
        if self.type == Dt.PRIMARY_KEY:
            return self.metadata.nextkey()
        raise TypeError("Can only predict key for primary key columns")

    def addListener(self, listener):
        """Adds a ColumnListener, that will listen to this Columns values."""
        self.listeners.append(listener)

    def listenTo(self, listener):
        """Registers the ColumnListener, which listens to the Column, that this Column depends on, if this Column has a dependend Datatype."""
        self.listener = listener

    def __str__(self):
        """Returns the name of this Column."""
        return self.name