from tkinter import *
from typing import Callable, Union, Optional

class ColumnEntry(Frame):
    def __init__(self, root: Frame, columnLambda: Callable[[], list[str]]) -> None:
        super().__init__(root)
        self._columnLambda: Callable[[], list[str]] = columnLambda
        self._variable: Optional[StringVar]
        self._entry: Union[Entry, OptionMenu]
        self.recalculate()

    def get(self) -> str:
        if isinstance(self._entry, Entry):
            return self._entry.get()
        else:
            return self._variable.get() if self._variable else ""
        
    def recalculate(self) -> None:
        values: list[str] = self._columnLambda()
        if len(values) == 0:
            self._variable = None
            self._entry = Entry(self)
        else:
            self._variable = StringVar(self)
            self._variable.set("")
            self._entry = OptionMenu(self, self._variable, *(values))
        self._entry.grid(column=0, row=0)