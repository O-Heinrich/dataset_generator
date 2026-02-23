from datetime import date
from faker import Faker
import random
import datetime

from typing import Union;

def generateDate(fake: Faker, start: Union[str, datetime.date, datetime.datetime]='-99y', end: Union[str, datetime.date, datetime.datetime]='today') -> datetime.date:
    return fake.date_between(start_date=start, end_date=end)

def generateAscendingDates(fake: Faker, amount: int, start: Union[str, datetime.date, datetime.datetime]='-99y', end: Union[str, datetime.date, datetime.datetime]='today', reverse: bool=False) -> list[str]:
    l: list[str] = []
    last: Union[str, date] = start
    for _ in range(amount):
        last = fake.date_between(start_date=last, end_date=end)
        l.append(last.strftime("%Y-%m-%d"))

    if reverse:
        return list(reversed(l))
    else:
        return l

def generateTime(fake: Faker):
    return fake.time()

def generateDateTime(fake: Faker, start: Union[str, datetime.date, datetime.datetime]='-99y', end: Union[str, datetime.date, datetime.datetime]='today') -> str:
    return str(fake.date_time_between(start_date=start, end_date=end))

def generateFloat(start: float, stop: Union[int, float, None]=None, accuracy: float=100) -> float:
    min: int = int(start * accuracy)
    max: int = int(start * accuracy)
    if stop is None:
        min = 0
    else:
        max = int(stop * accuracy)
    if max == min:
        return min
    elif max < min:
        # Swap min and max
        min += max
        max = min - max
        min -= max
    return random.randrange(min, max) / accuracy

def generateInt(min: int, max: int) -> int:
    if max <= min:
        return max
    return random.randrange(min, max)