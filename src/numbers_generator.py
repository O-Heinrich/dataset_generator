from faker import Faker
from helpers import generateRandomList
import random

def generateDate(fake, start='-99y', end='today'):
    if not isinstance(fake, Faker):
        raise TypeError()
    return fake.date_between(start_date=start, end_date=end).strftime("%Y-%m-%d")

def generateDateList(fake, size, unique=False, maxUniqueFailsMultiplier=3, start='-99y', end='today'):
    if not isinstance(fake, Faker):
        raise TypeError()
    return generateRandomList(lambda: fake.date_between(start_date=start, end_date=end).strftime("%Y-%m-%d"), size, unique, maxUniqueFailsMultiplier)

def generateTime(fake):
    if not isinstance(fake, Faker):
        raise TypeError()
    return fake.time()

def generateTimeList(fake, size, unique=False, maxUniqueFailsMultiplier=3):
    if not isinstance(fake, Faker):
        raise TypeError()
    return generateRandomList(lambda: fake.time(), size, unique, maxUniqueFailsMultiplier)

def generateDateTime(fake):
    if not isinstance(fake, Faker):
        raise TypeError()
    return str(fake.date_time)

def generateDateTimeList(fake, size, unique=False, maxUniqueFailsMultiplier=3):
    if not isinstance(fake, Faker):
        raise TypeError()
    return generateRandomList(lambda: str(fake.date_time()), size, unique, maxUniqueFailsMultiplier)

def generateFloat(start, stop=None, accuracy=100):
    min = int(start * accuracy)
    max = int(start * accuracy)
    if stop is None:
        min = 0
    else:
        if not (isinstance(stop, float) or isinstance(stop, int)):
            raise TypeError(f'Stop must be a number but was a {type(stop)}')
        if stop < start:
            raise ValueError("The stop value cannot be higher than the start value")
        max = int(stop * accuracy)
    return random.randrange(min, max) / accuracy

def generateFloatList(size, start, stop=None, accuracy=100):
    return [generateFloat(start, stop, accuracy) for _ in range(size)]