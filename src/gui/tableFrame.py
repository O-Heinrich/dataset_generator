from tkinter import *
from gui.columnFrame import ColumnFrame
from typing import Callable, Self, Union
from gui.labelWithExtras import LabelWithExtras
from enums.datatypes import Datatype as Dt

class TableFrame(Frame):
    """
    A Frame containing all Widgets for a single Table, including
    a delete Button,
    an Entry field for the name and the amount of datasets to generate,
    a Button to add Columns
    and Frames for each Column.
    """

    def __init__(self,
                 root: Widget,
                 keyColumnLambda: Callable[[Self, ColumnFrame], list[str]], # Function, that returns all valid key Column names
                 columnLambda: Callable[[Dt, Self, ColumnFrame], list[str]], # Function, that returns all valid Column names
                 cleanupFunc: Callable[[Self], None] # Function to be called, when this Frame is destroyed
                 ) -> None:
        super().__init__(root)
        self._keyColumnLambda: Callable[[ColumnFrame], list[str]] = lambda column: keyColumnLambda(self, column)
        self._columnLambda: Callable[[Dt, ColumnFrame], list[str]] = lambda dt, column: columnLambda(dt, self, column)
        self._cleanupFunc: Callable[[], None] = lambda: cleanupFunc(self)

        innerFrame: Frame = Frame(self)
        innerFrame.pack(anchor=W)

        # Entry for name
        LabelWithExtras(innerFrame, text="Tabellenname:", required=True).grid(column=0, row=0, sticky=W)
        validateName: str = (self.register(lambda P: str(P).replace("_", "").isalnum() and str(P).isascii()))
        self.entryName: Entry = Entry(innerFrame, validate="all", validatecommand=(validateName, "%P"))
        self.entryName.grid(column=1, row=0, sticky=W)

        # Entry for amount of datasets to generate
        vcmd: str = (self.register(lambda P: str.isdigit(P) or P == ""))
        Label(innerFrame, text="Anzahl Datensätze:").grid(column=0, row=1, sticky=W)
        self.entryAmount: Entry = Entry(innerFrame, validate="all", validatecommand=(vcmd, "%P"))
        self.entryAmount.grid(column=1, row=1, sticky=W)
        self.entryAmount.insert(INSERT, "20")

        # Adding Columns
        Button(innerFrame, text="Neue Spalte", command=self._newColumn).grid(column=0, row=3, sticky=W)
        self.columns: list[ColumnFrame] = []

        # delete Button
        Button(innerFrame, text="Tabelle löschen", command=self._removeSelf).grid(column=1, row=3, sticky=E)

        # Columns
        Label(self, text="Tabellenspalten:").pack(anchor=W)

    def _newColumn(self) -> None:
        """Creates a new ColumnFrame."""
        newColumn = ColumnFrame(self, self._keyColumnLambda, self._columnLambda, self._removeColumn)
        newColumn.pack(anchor=W)
        self.columns.append(newColumn)

    def isFilled(self) -> str:
        """
        Returns an empty string when all required Entries that are part of this Frame have a valid input, making this Table valid to be sent to the backend.
        If something is missing or invalid, an error message is returned instead.
        """
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
        """
        Returns a dictionary according to the json required by the backend for each Table.
        The dictionary contains the name, columns and amount of datasets for this Table.
        """
        return {
            "table": self.entryName.get(),
            "columns": {e.readKey(): e.readValue() for e in self.columns},
            "amount": int(self.entryAmount.get()) if self.entryAmount.get() else 20
        }

    def _removeColumn(self, column: ColumnFrame) -> None:
        """Removes a specified ColumnFrame from this Frame."""
        self.columns.remove(column)

    def _removeSelf(self) -> None:
        """Deletes this TableFrame and calls the cleanup function before."""
        self._cleanupFunc()
        self.destroy()