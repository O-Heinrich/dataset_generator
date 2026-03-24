import re
from datetime import date, datetime, time, timedelta
from enums.datatypes import Datatype as Dt

from typing import Any
from typing import Optional
from typing import Union

class Metadata:
    def __init__(self, metadata: dict[str, Any]={}):
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
        if self._nextkey is None:
            raise KeyError()
        return self._nextkey
    
    def incrementKey(self) -> None:
        if self._nextkey is None:
            raise KeyError()
        self._nextkey += 1

    def min(self) -> int:
        if self._min is None:
            raise KeyError()
        return self._min
    
    def max(self) -> int:
        if self._max is None:
            raise KeyError()
        return self._max
    
    def acc(self) -> int:
        if self._acc is None:
            raise KeyError()
        return self._acc
    
    def start(self) -> Union[str, datetime]:
        return self._start
    
    def end(self) -> Union[str, datetime]:
        return self._end
    
    def startTime(self) -> str:
        return self._startTime

    def endTime(self) -> str:
        return self._endTime
    
    def timeRounding(self) -> int:
        return self._timeRounding

    def values(self) -> list[Any]:
        if self._values is None:
            raise KeyError()
        return self._values
    
    def regex(self) -> str:
        if self._regex is None:
            raise KeyError()
        return self._regex
    
    def allType(self) -> Dt:
        if self._allType is None:
            raise KeyError()
        return self._allType
    
    def names(self) -> list[str]:
        if self._names is None:
            raise KeyError()
        return self._names
    
    def namesAmount(self) -> int:
        if self._names is None:
            raise KeyError()
        return len(self._names)
    
    def reverse(self) -> bool:
        if self._reverse is None:
            raise KeyError()
        return self._reverse
    
    def foreignKeyColumn(self) -> str:
        if self._foreignKeyColumn is None:
            raise KeyError()
        return self._foreignKeyColumn
    
    def foreignColumn(self) -> str:
        if self._foreignColumn is None:
            raise KeyError()
        return self._foreignColumn
    
    def diff(self) -> int:
        if self._diff is None:
            raise KeyError()
        return self._diff
    
    def getMaxWithMaxdiff(self, minimum) -> int:
        if self._maxdiff is None:
            return self.max()
        return min(minimum + self._maxdiff, self._max)
    
    def getMinWithMaxdiff(self, maximum) -> int:
        if self._maxdiff is None:
            return self.min()
        return max(maximum - self._maxdiff, self._min)
    
    def dictToTimeDelta(self, dictionary: dict[str, int]) -> timedelta:
        return timedelta(
            days=dictionary.get("days", 0),
            seconds=dictionary.get("seconds", 0),
            minutes=dictionary.get("minutes", 0),
            hours=dictionary.get("hours", 0),
            weeks=dictionary.get("weeks", 0)
        )
    
    def timeDiff(self) -> timedelta:
        return self.dictToTimeDelta(self._timeDiff)
    
    def getStartWithMaxdiff(self, end: Union[datetime, date]) -> Union[str, datetime]:
        if self._timeMaxdiff is None:
            return self.start()
        min: datetime = datetime.combine(end - self.dictToTimeDelta(self._timeMaxdiff), datetime.min.time())
        if isinstance(self._start, str) or min > self._start:
            return min
        else:
            return self.start()
    
    def getEndWithMaxdiff(self, start: Union[datetime, date]) -> Union[str, datetime]:
        if self._timeMaxdiff is None:
            return self.end()
        max: datetime = datetime.combine(start + self.dictToTimeDelta(self._timeMaxdiff), datetime.min.time())
        if isinstance(self._end, str) or max < self._end:
            return max
        else:
            return self.end()