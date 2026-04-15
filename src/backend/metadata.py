import re
from datetime import date, datetime, time, timedelta
from enums.datatypes import Datatype as Dt
from deprecated import deprecated
from typing import Any, Optional, Union

class Metadata:
    """Represents all additional data that can be attached to a Column, depending on the Columns Datatype."""

    def __init__(self, metadata: dict[str, Any]={}):
        """Takes a dictionary and parses it, by extracting applicable values from it"""
        self._nextkey: Optional[int] = metadata.get("nextkey", 0)

        self._min: Optional[int] = metadata.get("min", 0)
        self._max: Optional[int] = metadata.get("max")
        self._acc: Optional[int] = metadata.get("acc", 100)

        dateReg = r'^\d{4}\-\d\d\-\d\d$'
        self._start: Union[str, datetime] = metadata.get("start", "-99y")
        self._end: Union[str, datetime] = metadata.get("end", "now")
        if re.match(dateReg, self._start):
            self._start = datetime.strptime(self._start, "%Y-%m-%d")
        if re.match(dateReg, self._end):
            self._end = datetime.strptime(self._end, "%Y-%m-%d")
        self._startTime: str = metadata.get("startTime", "00:00:00")
        self._endTime: str = metadata.get("endTime", "23:59:59")
        self._timeRounding: int = metadata.get("timeRounding", 0)

        self._values: Optional[list[Any]] = metadata.get("values")

        self._regex: Optional[str] = metadata.get("regex")

        # allType, names and reverse may no longer be needed, need to check
        allType_str: Optional[str] = metadata.get("alltype")
        self._allType: Optional[Dt] = None
        if allType_str is not None:
            self._allType = Dt[allType_str.upper()]
        self._names: Optional[list[str]] = metadata.get("names")
        self._reverse: Optional[bool] = metadata.get("reverse", False)

        self._foreignKeyColumn: Optional[str] = metadata.get("fk")
        self._foreignColumn: Optional[str] = metadata.get("column")

        self._diff: Optional[int] = metadata.get("diff", 0)
        self._maxdiff: Optional[int] = metadata.get("maxdiff")
        if self._maxdiff is not None and self._maxdiff < self._diff:
            raise ValueError("maxdiff should not be lower than diff")
        self._timeDiff: dict[str, int] = metadata.get("timeDiff", {})
        self._timeMaxdiff: Optional[dict[str, int]] = metadata.get("timeMaxdiff")

    def nextkey(self) -> int:
        """
        Returns the next unique integer key value for Datatype PRIMARY_KEY.
        Does not increment the key value, for that use incrementKey()
        """
        if self._nextkey is None:
            raise KeyError()
        return self._nextkey
    
    def incrementKey(self) -> None:
        """Increments the next unique integer key value."""
        if self._nextkey is None:
            raise KeyError()
        self._nextkey += 1

    def min(self) -> int:
        """Returns the minimum integer value for Datatypes INTEGER, FLOAT and MONEY."""
        if self._min is None:
            raise KeyError()
        return self._min
    
    def max(self) -> int:
        """Returns the maximum integer value for Datatypes INTEGER, FLOAT and MONEY."""
        if self._max is None:
            raise KeyError()
        return self._max
    
    def acc(self) -> int:
        """Returns the accuracy for values of Datatype FLOAT."""
        if self._acc is None:
            raise KeyError()
        return self._acc
    
    def start(self) -> Union[str, datetime]:
        """Returns the earliest datetime for values of Datatypes DATE and DATE_TIME."""
        return self._start
    
    def end(self) -> Union[str, datetime]:
        """Returns the latest datetime for values of Datatypes DATE and DATE_TIME."""
        return self._end
    
    def startTime(self) -> str:
        """Returns the earliest time in string format for values of Datatypes TIME and DATE_TIME."""
        return self._startTime

    def endTime(self) -> str:
        """Returns the latest time in string format for values of Datatypes TIME and DATE_TIME."""
        return self._endTime
    
    def timeRounding(self) -> int:
        """Returns the number of minutes to be rounded to for values of Datatypes TIME and DATE_TIME"""
        return self._timeRounding

    def values(self) -> list[Any]:
        """Returns the list of possible values for values of Datatype VALUES."""
        if self._values is None:
            raise KeyError()
        return self._values
    
    def regex(self) -> str:
        """Returns the string representing the regex for values of Datatype REGEX."""
        if self._regex is None:
            raise KeyError()
        return self._regex
    
    @deprecated
    def allType(self) -> Dt:
        if self._allType is None:
            raise KeyError()
        return self._allType
    
    @deprecated
    def names(self) -> list[str]:
        if self._names is None:
            raise KeyError()
        return self._names
    
    @deprecated
    def namesAmount(self) -> int:
        if self._names is None:
            raise KeyError()
        return len(self._names)
    
    @deprecated
    def reverse(self) -> bool:
        if self._reverse is None:
            raise KeyError()
        return self._reverse
    
    def foreignKeyColumn(self) -> str:
        """
        Returns the name of the column from another table, which is the foreign key which ties the column to another column.
        The name is in the format tablename.columnname
        """
        if self._foreignKeyColumn is None:
            raise KeyError()
        return self._foreignKeyColumn
    
    def foreignColumn(self) -> str:
        """
        Returns the name of another column, which the column depends on.
        If the other column is in another table, then the name is in the format tablename.columnname
        """
        if self._foreignColumn is None:
            raise KeyError()
        return self._foreignColumn
    
    def diff(self) -> int:
        """Returns an integer representing the minimum difference for values of Datatypes LOWERTHAN_INTEGER, HIGHERTHAN_INTEGER, LOWERTHAN_FLOAT and HIGHERTHAN_FLOAT."""
        if self._diff is None:
            raise KeyError()
        return self._diff
    
    def getMaxWithMaxdiff(self, minimum) -> int:
        """Returns the highest possible value for values of Datatypes HIGHERTHAN_INTEGER and HIGHERTHAN_FLOAT."""
        if self._maxdiff is None:
            return self.max()
        return min(minimum + self._maxdiff, self._max)
    
    def getMinWithMaxdiff(self, maximum) -> int:
        """Returns the lowest possible value for values of Datatypes LOWERTHAN_INTEGER and LOWERTHAN_FLOAT."""
        if self._maxdiff is None:
            return self.min()
        return max(maximum - self._maxdiff, self._min)
    
    def dictToTimeDelta(self, dictionary: dict[str, int]) -> timedelta:
        """Returns a timedelta matching the given dictionary."""
        return timedelta(
            days=dictionary.get("days", 0),
            seconds=dictionary.get("seconds", 0),
            minutes=dictionary.get("minutes", 0),
            hours=dictionary.get("hours", 0),
            weeks=dictionary.get("weeks", 0)
        )
    
    def timeDiff(self) -> timedelta:
        """
        Returns a timedelta representing the minimum difference for values of Datatypes
        LOWERTHAN_DATE, HIGHERTHAN_DATE, LOWERTHAN_TIME, HIGHERTHAN_TIME, HIGHERTHAN_DATETIME, LOWERTHAN_DATETIME
        """
        return self.dictToTimeDelta(self._timeDiff)
    
    def getStartWithMaxdiff(self, end: Union[datetime, date]) -> Union[str, datetime]:
        """Returns the earliest possible datetime for values of Datatypes LOWERTHAN_DATE and LOWERTHAN_DATETIME"""
        if self._timeMaxdiff is None:
            return self.start()
        minimum: datetime
        if isinstance(end, datetime):
            minimum = end - self.dictToTimeDelta(self._timeMaxdiff)
        else:
            minimum  = datetime.combine(end - self.dictToTimeDelta(self._timeMaxdiff), datetime.min.time())
        if isinstance(self._start, str) or minimum > self._start:
            return minimum
        else:
            return self.start()
    
    def getEndWithMaxdiff(self, start: Union[datetime, date]) -> Union[str, datetime]:
        """Returns the latest possible datetime for values of Datatypes HIGHERTHAN_DATE and HIGHERTHAN_DATETIME"""
        if self._timeMaxdiff is None:
            return self.end()
        maximum: datetime
        if isinstance(start, datetime):
            maximum = start + self.dictToTimeDelta(self._timeMaxdiff)
        else:
            maximum = datetime.combine(start + self.dictToTimeDelta(self._timeMaxdiff), datetime.min.time())
        if isinstance(self._end, str) or maximum < self._end:
            return maximum
        else:
            return self.end()
        
    def getStartTimeWithMaxDiff(self, end: Union[datetime, time]) -> str:
        """Returns the earliest possible time for values of Datatype LOWERTHAN_TIME"""
        if self._timeMaxdiff is None:
            return self.startTime()
        endTime: time = end.time() if isinstance(end, datetime) else end
        minimum: datetime = datetime.combine(date.today(), endTime) - self.dictToTimeDelta(self._timeMaxdiff)
        if minimum > timeStringToDatetime(self.startTime()):
            return minimum.strftime("%H:%M:%S")
        else:
            return self.startTime()
        
    def getEndTimeWithMaxDiff(self, start: Union[datetime, time]) -> str:
        """Returns the latest possible time for values of Datatype HIGHERTHAN_TIME"""
        if self._timeMaxdiff is None:
            return self.endTime()
        startTime: time = start.time() if isinstance(start, datetime) else start
        maximum: datetime = datetime.combine(date.today(), startTime) + self.dictToTimeDelta(self._timeMaxdiff)
        if maximum < timeStringToDatetime(self.endTime()):
            return maximum.strftime("%H:%M:%S")
        else:
            return self.endTime()
        
def timeStringToDatetime(timestring: str) -> datetime:
    """Turns a string representing a time in 24 hours format %H:%M:%S into a datetime object with that time and the current date."""
    return datetime.strptime(date.today().strftime("%Y-%m-%d") + " " + timestring, "%Y-%m-%d %H:%M:%S")