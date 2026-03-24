from tkinter import *
from gui.timeDict import TimeDict

class TimeDictEntry(Frame):
    def __init__(self, root: Frame) -> None:
        super().__init__(root)
        vcdm: str = (self.register(lambda P: str.isdigit(P) or P == ""))
        Label(self, text="Tage").grid(column=0, row=0)
        self._days: Entry = Entry(self, validate="all", validatecommand=(vcdm, "%P"))
        self._days.grid(column=1, row=0)

        Label(self, text="Wochen").grid(column=0, row=1)
        self._weeks: Entry = Entry(self, validate="all", validatecommand=(vcdm, "%P"))
        self._weeks.grid(column=1, row=1)

        Label(self, text="Stunden").grid(column=0, row=2)
        self._hours: Entry = Entry(self, validate="all", validatecommand=(vcdm, "%P"))
        self._hours.grid(column=1, row=2)

        Label(self, text="Minuten").grid(column=0, row=3)
        self._minutes: Entry = Entry(self, validate="all", validatecommand=(vcdm, "%P"))
        self._minutes.grid(column=1, row=3)

        Label(self, text="Sekunden").grid(column=0, row=4)
        self._seconds: Entry = Entry(self, validate="all", validatecommand=(vcdm, "%P"))
        self._seconds.grid(column=1, row=4)

    def get(self) -> TimeDict:
        return TimeDict(
            days=0 if not self._days.get() else int(self._days.get()),
            weeks=0 if not self._weeks.get() else int(self._weeks.get()),
            hours=0 if not self._hours.get() else int(self._hours.get()),
            minutes=0 if not self._minutes.get() else int(self._minutes.get()),
            seconds=0 if not self._seconds.get() else int(self._seconds.get())
        )
    
    def insertDict(self, dict: TimeDict) -> None:
        self._days.insert(INSERT, str(dict.days))
        self._weeks.insert(INSERT, str(dict.weeks))
        self._hours.insert(INSERT, str(dict.hours))
        self._minutes.insert(INSERT, str(dict.minutes))
        self._seconds.insert(INSERT, str(dict.seconds))