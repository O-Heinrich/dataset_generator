from tkinter import Frame, Entry, Label, INSERT
from gui.timeDict import TimeDict
from typing import Optional

class TimeDictEntry(Frame):
    """A Widget, which contains all elements to enter a TimeDict in the GUI."""

    def __init__(self, root: Frame, doDate: bool=True, doTime: bool=True) -> None:
        super().__init__(root)
        vcdm: str = (self.register(lambda P: str.isdigit(P) or P == ""))

        self._days: Optional[Entry] = None
        self._weeks: Optional[Entry] = None
        self._hours: Optional[Entry] = None
        self._minutes: Optional[Entry] = None
        self._seconds: Optional[Entry] = None

        if doDate:
            Label(self, text="Tage").grid(column=0, row=0)
            self._days = Entry(self, validate="all", validatecommand=(vcdm, "%P"))
            self._days.grid(column=1, row=0)

            Label(self, text="Wochen").grid(column=0, row=1)
            self._weeks = Entry(self, validate="all", validatecommand=(vcdm, "%P"))
            self._weeks.grid(column=1, row=1)

        if doTime:
            Label(self, text="Stunden").grid(column=0, row=2)
            self._hours = Entry(self, validate="all", validatecommand=(vcdm, "%P"))
            self._hours.grid(column=1, row=2)

            Label(self, text="Minuten").grid(column=0, row=3)
            self._minutes = Entry(self, validate="all", validatecommand=(vcdm, "%P"))
            self._minutes.grid(column=1, row=3)

            Label(self, text="Sekunden").grid(column=0, row=4)
            self._seconds = Entry(self, validate="all", validatecommand=(vcdm, "%P"))
            self._seconds.grid(column=1, row=4)

    def get(self) -> TimeDict:
        """Return the TimeDict that is currently input into this TimeDictEntry."""
        return TimeDict(
            days=0 if not (self._days and self._days.get()) else int(self._days.get()),
            weeks=0 if not (self._weeks and self._weeks.get()) else int(self._weeks.get()),
            hours=0 if not (self._hours and self._hours.get()) else int(self._hours.get()),
            minutes=0 if not (self._minutes and self._minutes.get()) else int(self._minutes.get()),
            seconds=0 if not (self._seconds and self._seconds.get()) else int(self._seconds.get())
        )
    
    def insertDict(self, dict: TimeDict) -> None:
        """Set the input of this TimeDictEntry to the given TimeDict."""
        if self._days:
            self._days.insert(INSERT, str(dict.days))
        if self._weeks:
            self._weeks.insert(INSERT, str(dict.weeks))
        if self._hours:
            self._hours.insert(INSERT, str(dict.hours))
        if self._minutes:
            self._minutes.insert(INSERT, str(dict.minutes))
        if self._seconds:
            self._seconds.insert(INSERT, str(dict.seconds))