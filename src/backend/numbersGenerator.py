from datetime import date, datetime, timedelta, time
from faker import Faker
import random
from typing import Union, Optional

def generateDate(fake: Faker, start: Union[str, date, datetime]='-99y', end: Union[str, date, datetime]='today') -> date:
    """
    Generates a random date using the given Faker.
    The start and end can be date, datetime or string objects according to https://faker.readthedocs.io/en/master/providers/faker.providers.date_time.html
    """
    return fake.date_between(start_date=start, end_date=end)

def roundTime(t: time, timeRounding: int=0) -> time:
    """
    Rounds a time object and returns a new time object, rounded to the full number of minutes given by timeRounding.
    Does nothing if timeRounding is 0 and raises a NotImplementedError if timeRounding is negative, or if it is higher than 60 but not a multiple of 60.
    If timeRounding is a multiple of 60 it will round to full hours.
    """
    if timeRounding < 0:
        raise NotImplementedError()
    if timeRounding != 0:
        newMinute: int
        newHour: int = t.hour
        if timeRounding % 60 == 0:
            newMinute = 0
            hourRounding: int = int(timeRounding / 60)
            newHour = t.hour - t.hour % hourRounding
        elif timeRounding < 60:
            newMinute = t.minute - t.minute % timeRounding
        else:
            raise NotImplementedError()
        return time(hour=newHour, minute=newMinute, second=0)
    return t

def generateTime(fake: Faker, startTime: str="00:00:00", endTime: str="23:59:59", timeRounding: int=0) -> time:
    """
    Generates a random time using the given Faker.
    The startTime and endTime have to be strings in the 24 hour format %H:%M:%S
    and the timeRounding has to be a positive integer representing the minutes to be rounded to.
    """
    start: datetime = datetime.strptime(startTime, "%H:%M:%S")
    end: datetime = datetime.strptime(endTime, "%H:%M:%S")
    if abs(end - start) == timedelta(seconds=1):
        if random.getrandbits(1):
            return roundTime(start.time(), timeRounding)
        else:
            return roundTime(end.time(), timeRounding)
    generated: time = fake.date_time_between(start_date=start, end_date=end).time()
    return roundTime(generated, timeRounding)

def generateDateTime(fake: Faker, start: Union[str, date, datetime]='-99y', end: Union[str, date, datetime]='today', startTime: Optional[str]=None, endTime: Optional[str]=None, timeRounding: int=0) -> datetime:
    """
    Generates a random datetime using the given Faker.
    The start and end can be date, datetime or string objects according to https://faker.readthedocs.io/en/master/providers/faker.providers.date_time.html
    If startTime and endTime are omitted, any time can be generated,
    otherwise the time part of the generated datetime is between those values.
    If given the startTime and endTime have to be strings in the 24 hour format %H:%M:%S
    and the timeRounding has to be a positive integer representing the minutes to be rounded to.
    """
    if startTime is None and endTime is None:
        generated: datetime = fake.date_time_between(start_date=start, end_date=end)
        if timeRounding == 0:
            return generated
        else:
            return datetime.combine(generated.date(), roundTime(generated.time(), timeRounding))
    else:
        d: date = generateDate(fake, start=start, end=end)
        t: time
        if startTime is not None and endTime is not None:
            t = generateTime(fake, startTime=startTime, endTime=endTime, timeRounding=timeRounding)
        elif startTime is not None:
            t = generateTime(fake, startTime=startTime, timeRounding=timeRounding)
        elif endTime is not None:
            t = generateTime(fake, endTime=endTime, timeRounding=timeRounding)
        else:
            raise NotImplementedError()
        return datetime.combine(d, t)

def generateFloat(start: float, stop: Union[int, float, None]=None, accuracy: float=100) -> float:
    """
    Generates a random floating point value, between the given start and stop values,
    where the lower one is inclusive and the higher is exclusive.
    If stop is ommitted, generates a value between 0 and start.
    If start is equal to stop returns that value.
    Accuracy describes how fine the values will be rounded (higher accuracy means more precise value).
    The result value can be represented as a fraction, where the denominator will not be higher than the accuracy.
    If accuracy is a power of 10 with 10^n, n will represent the number digits after the decimal point.
    """
    minimum: int = int(start * accuracy)
    maximum: int = int(start * accuracy)
    if stop is None:
        minimum = 0
    else:
        maximum = int(stop * accuracy)
    if maximum == minimum:
        return minimum / accuracy
    if maximum < minimum:
        # Swap min and max
        minimum += maximum
        maximum = minimum - maximum
        minimum -= maximum
    return random.randrange(minimum, maximum) / accuracy

def generateInt(min: int, max: int) -> int:
    """
    Generates a random integer value from min (inclusive) to max (exclusive).
    If the range would be empty, because max is not higher than min, just returns max.
    """
    if max <= min:
        return max
    return random.randrange(min, max)