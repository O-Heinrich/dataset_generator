class TimeDict:
    def __init__(self, days: int=0, weeks: int=0, hours: int=0, minutes: int=0, seconds: int=0):
        self.days: int = days
        self.weeks: int = weeks
        self.hours: int = hours
        self.minutes: int = minutes
        self.seconds: int = seconds

    def toDict(self) -> dict[str, int]:
        return {"days":self.days,"weeks":self.weeks,"hours":self.hours,"minutes":self.minutes,"seconds":self.seconds}