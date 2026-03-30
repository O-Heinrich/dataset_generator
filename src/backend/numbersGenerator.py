from datetime import date, datetime, timedelta, time
from faker import Faker
import random

from typing import Union, Optional

def generateDate(fake: Faker, start: Union[str, date, datetime]='-99y', end: Union[str, date, datetime]='today') -> date:
    return fake.date_between(start_date=start, end_date=end)

def roundTime(t: time, timeRounding: int=0) -> time:
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
    start: datetime = datetime.strptime(startTime, "%H:%M:%S")
    end: datetime = datetime.strptime(endTime, "%H:%M:%S")# For some unknown reason Faker is buggy with this so just ignoring that one second# + timedelta(seconds=1)
    generated: time = fake.date_time_between(start_date=start, end_date=end).time()
    return roundTime(generated, timeRounding)

def generateDateTime(fake: Faker, start: Union[str, date, datetime]='-99y', end: Union[str, date, datetime]='today', startTime: Optional[str]=None, endTime: Optional[str]=None, timeRounding: int=0) -> datetime:
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
    minimum: int = int(start * accuracy)
    maximum: int = int(start * accuracy)
    if stop is None:
        minimum = 0
    else:
        maximum = int(stop * accuracy)
    if maximum == minimum:
        return minimum
    elif maximum < minimum:
        # Swap min and max
        minimum += maximum
        maximum = minimum - maximum
        minimum -= maximum
    return random.randrange(minimum, maximum) / accuracy

def generateInt(min: int, max: int) -> int:
    if max <= min:
        return max
    return random.randrange(min, max)