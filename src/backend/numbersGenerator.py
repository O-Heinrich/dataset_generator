from datetime import date, datetime, timedelta, time
from faker import Faker
import random

from typing import Union, Optional

def generateDate(fake: Faker, start: Union[str, date, datetime]='-99y', end: Union[str, date, datetime]='today') -> date:
    return fake.date_between(start_date=start, end_date=end)

def generateTime(fake: Faker, startTime: str="00:00:00", endTime: str="23:59:59", timeRounding: int=0) -> time:
    start: datetime = datetime.strptime(startTime, "%H:%M:%S")
    end: datetime = datetime.strptime(endTime, "%H:%M:%S")# For some unknown reason Faker is buggy with this so just ignoring that one second# + timedelta(seconds=1)
    generated: time = fake.date_time_between(start_date=start, end_date=end).time()
    if timeRounding < 0:
        raise NotImplementedError()
    if timeRounding != 0:
        newminute: int = generated.minute
        newhour: int = generated.hour
        if timeRounding % 60 == 0:
            newminute = 0
            hourRounding: int = int(timeRounding / 60)
            newhour = generated.hour - generated.hour % hourRounding
        elif timeRounding < 60:
            newminute = generated.minute - generated.minute % timeRounding
        else:
            raise NotImplementedError()
        return time(hour=newhour, minute=newminute, second=0)
    return generated

def generateDateTime(fake: Faker, start: Union[str, date, datetime]='-99y', end: Union[str, date, datetime]='today', startTime: Optional[str]=None, endTime: Optional[str]=None, timeRounding: int=0) -> datetime:
    if startTime is None and endTime is None:
        if timeRounding == 0:
            return fake.date_time_between(start_date=start, end_date=end)
        else:
            return datetime.combine(generateDate(fake, start=start, end=end), generateTime(fake, timeRounding=timeRounding))
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