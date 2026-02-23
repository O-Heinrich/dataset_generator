import datetime

from typing import Any;

def stringify(any: Any, sep: str=", ") -> str:
    if type(any) is str:
        return f'"{any}"'
    elif isinstance(any, list):
        return sep.join([stringify(x) for x in any])
    elif isinstance(any, datetime.date):
        return any.strftime("%Y-%m-%d")
    else:
        return str(any)