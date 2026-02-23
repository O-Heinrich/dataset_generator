import re
import datetime
from datatypes import Datatype as Dt

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
        self._start: Optional[Union[str, datetime.datetime]] = metadata.get("start", "-99y")
        self._end: Optional[Union[str, datetime.datetime]] = metadata.get("end", "now")
        if re.match(dateReg, self._start):
            self._start = datetime.datetime.strptime(self._start, "%Y-%m-%d")
        if re.match(dateReg, self._end):
            self._end = datetime.datetime.strptime(self._end, "%Y-%m-%d")

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
    
    def start(self) -> Union[str, datetime.datetime]:
        if self._start is None:
            raise KeyError()
        return self._start
    
    def end(self) -> Union[str, datetime.datetime]:
        if self._end is None:
            raise KeyError()
        return self._end
    
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