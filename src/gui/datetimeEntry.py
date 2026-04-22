from tkinter import Frame
from tkcalendar import Calendar
from tktimepicker import AnalogPicker, constants
from typing import Optional, Any, Union
from datetime import date, time
from gui.entryInterface import EntryInterface

class DatetimeEntry(Frame, EntryInterface):
    """A Widget, which contains all elements to enter a datetime, date or time in the GUI."""

    def __init__(self, root: Frame, date: bool=False, time: bool=False) -> None:
        assert date or time
        assert not (date and time)
        super().__init__(root)
        self._calendar: Optional[Calendar] = None
        if date:
            self._calendar = Calendar(self)
            self._calendar.grid(column=0, row=0)
        self._clock: Optional[AnalogPicker] = None
        if time:
            self._clock = AnalogPicker(self)
            self._clock.grid(column=0, row=0)

    def get(self) -> str:
        """Return a string representation of the datetime, date or time that is currently input into this DatetimeEntry."""
        assert self._calendar or self._clock
        if self._calendar:
            d: Any = self._calendar.selection_get()
            assert isinstance(d, date)
            return d.strftime("%Y-%m-%d")
        elif self._clock:
            t: time = time(hour=self._clock.hours(), minute=self._clock.minutes())
            return t.strftime("%H:%M:%S")
        else:
            raise NotImplementedError()
        
    def insertDatetime(self, dt: Union[date, time]) -> None:
        """Set the input of this DatetimeEntry to the given date or time."""
        if isinstance(dt, date):
            assert self._calendar
            self._calendar.destroy()
            self._calendar = Calendar(self, year=dt.year, month=dt.month, day=dt.day)
            self._calendar.grid(column=0, row=0)
        elif isinstance(dt, time):
            assert self._clock
            if dt.hour >= 12:
                self._clock.destroy()
                self._clock = AnalogPicker(self, period=constants.PM)
                self._clock.grid(column=0, row=0)
            self._clock.setHours(dt.hour % 12)
            self._clock.setMinutes(dt.minute)