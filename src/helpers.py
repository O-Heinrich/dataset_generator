from exceptions import TooManyUniqueFailsException

from typing import Callable;
from typing import Union;
from typing import Any;

def generateRandomList(randomGenerator: Callable[[], Any], size: int, unique: bool=False, maxUniqueFailsMultiplier: int=3) -> list[Any]:
    if not unique:
        return [randomGenerator() for _ in range(size)]

    result: set[Any] = set()
    count: int = 0
    while len(result) < size:
        result.add(randomGenerator())
        count += 1
        if count > size * maxUniqueFailsMultiplier:
            raise TooManyUniqueFailsException()
    return list(result)

def stringify(any: Any, sep: str=", ") -> str:
    if type(any) is str:
        return f'"{any}"'
    elif type(any) is list[Any]:
        return sep.join([stringify(x) for x in any])
    else:
        return str(any)