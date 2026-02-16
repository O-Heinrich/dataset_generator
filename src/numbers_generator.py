from datetime import date
from faker import Faker
from helpers import generateRandomList
import random

from typing import Union;

def generateDate(fake: Faker, start: str='-99y', end: str='today') -> str:
    return fake.date_between(start_date=start, end_date=end).strftime("%Y-%m-%d")

def generateDateList(fake: Faker, size: int, unique: bool=False, maxUniqueFailsMultiplier: int=3, start: str='-99y', end: str='today'):
    return generateRandomList(lambda: fake.date_between(start_date=start, end_date=end).strftime("%Y-%m-%d"), size, unique, maxUniqueFailsMultiplier)

def generateAscendingDates(fake: Faker, amount: int, start: str='-99y', end: str='today', reverse: bool=False) -> list[str]:
    l: list[str] = []
    last: Union[str, date] = start
    for _ in range(amount):
        last = fake.date_between(start_date=last, end_date=end)
        l.append(last.strftime("%Y-%m-%d"))

    if reverse:
        return list(reversed(l))
    else:
        return l

def generateAscendingDatesList(fake: Faker, size: int, amount: int, start: str='-99y', end: str='today', reverse: bool=False) -> list[str]:
    return generateRandomList(lambda: generateAscendingDates(fake, amount, start, end, reverse), size)

def generateTime(fake: Faker):
    return fake.time()

def generateTimeList(fake: Faker, size: int, unique: bool=False, maxUniqueFailsMultiplier: int=3) -> list[str]:
    return generateRandomList(lambda: fake.time(), size, unique, maxUniqueFailsMultiplier)

def generateDateTime(fake: Faker) -> str:
    return str(fake.date_time)

def generateDateTimeList(fake: Faker, size: int, unique: bool=False, maxUniqueFailsMultiplier: int=3) -> list[str]:
    return generateRandomList(lambda: str(fake.date_time()), size, unique, maxUniqueFailsMultiplier)

def generateFloat(start: float, stop: Union[int, float, None]=None, accuracy: float=100) -> float:
    min: int = int(start * accuracy)
    max: int = int(start * accuracy)
    if stop is None:
        min = 0
    else:
        if stop < start:
            raise ValueError("The stop value cannot be higher than the start value")
        max = int(stop * accuracy)
    return random.randrange(min, max) / accuracy

def generateFloatList(size: int, start: float, stop: Union[int, float, None]=None, accuracy: float=100) -> list[float]:
    return [generateFloat(start, stop, accuracy) for _ in range(size)]