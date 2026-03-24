from tkinter import *
from gui.columnFrame import ColumnFrame
from typing import Callable, Self, Union
from gui.labelWithExtras import LabelWithExtras
from enums.datatypes import Datatype as Dt

class TableFrame(Frame):
    def __init__(self,
                 root: Widget,
                 keyColumnLambda: Callable[[Self, ColumnFrame], list[str]],
                 columnLambda: Callable[[Dt, Self, ColumnFrame], list[str]],
                 cleanupFunc: Callable[[Self], None]
                 ) -> None:
        super().__init__(root)
        self._keyColumnLambda: Callable[[ColumnFrame], list[str]] = lambda column: keyColumnLambda(self, column)
        self._columnLambda: Callable[[Dt, ColumnFrame], list[str]] = lambda dt, column: columnLambda(dt, self, column)
        self._cleanupFunc: Callable[[], None] = lambda: cleanupFunc(self)

        LabelWithExtras(self, text="Tabellenname:", required=True).grid(column=0, row=0)
        validateName: str = (self.register(lambda P: str(P).replace("_", "").isalnum() and str(P).isascii()))
        self.entryName: Entry = Entry(self, validate="all", validatecommand=(validateName, "%P"))
        self.entryName.grid(column=1, row=0)

        vcmd: str = (self.register(lambda P: str.isdigit(P) or P == ""))
        Label(self, text="Anzahl Datensätze:").grid(column=0, row=1)
        self.entryAmount: Entry = Entry(self, validate="all", validatecommand=(vcmd, "%P"))
        self.entryAmount.grid(column=1, row=1)
        self.entryAmount.insert(INSERT, "20")

        Label(self, text="Tabellenspalten:").grid(column=0, row=2)
        Button(self, text="Neue Spalte", command=self.newColumn).grid(column=1, row=2)
        Button(self, text="Tabelle löschen", command=self.removeSelf).grid(column=2, row=2)
        self.columns: list[ColumnFrame] = []

    def newColumn(self) -> None:
        newColumn = ColumnFrame(self, self._keyColumnLambda, self._columnLambda, self.removeColumn)
        newColumn.grid(column=1, row=3+len(self.columns))
        self.columns.append(newColumn)

    def isFilled(self) -> str:
        if not self.entryName.get():
            return "Fehlender Tabellenname"
        if len(self.columns) == 0:
            return f'Tabelle {self.entryName.get()} hat keine Spalten'
        for c in self.columns:
            f: str = c.isFilled()
            if f:
                return f'In Tabelle {self.entryName.get()}: {f}'
        return ""
    
    def readValues(self) -> dict[str, Union[str, dict, int]]:
        return {
            "table": self.entryName.get(),
            "columns": {e.readKey(): e.readValue() for e in self.columns},
            "amount": int(self.entryAmount.get()) if self.entryAmount.get() else 20
        }

    def removeColumn(self, column: ColumnFrame) -> None:
        self.columns.remove(column)

    def removeSelf(self) -> None:
        self._cleanupFunc()
        self.destroy()