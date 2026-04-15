from tkinter import *
from gui.tableFrame import TableFrame
from gui.columnFrame import ColumnFrame
from enums.datatypes import Datatype as Dt
from enums.dialect import SqlDialect
from typing import Any, Optional
from backend.backend_api import generateData
from gui.labelWithExtras import LabelWithExtras
from tktooltip import ToolTip

class App:
    """
    Top Level of the GUI, containing all elements.
    It directly manages
    the scrollbars,
    the menu containing Entries for general Parameters and a Button to generate,
    the Tables and a Button to add new Tables.
    """

    def __init__(self, root) -> None:
        # Scrollbars
        horizontalScroll: Scrollbar = Scrollbar(root, orient=HORIZONTAL)
        horizontalScroll.pack(side=TOP, fill=X)
        verticalScroll: Scrollbar = Scrollbar(root, orient=VERTICAL)
        verticalScroll.pack(side=LEFT, fill=Y)
        self._canvas: Canvas = Canvas(root)
        self._canvas.pack(side=TOP, fill=BOTH, expand=True)
        horizontalScroll.configure(command=self._canvas.xview)
        verticalScroll.configure(command=self._canvas.yview)
        self._canvas.configure(xscrollcommand=horizontalScroll.set, yscrollcommand=verticalScroll.set)
        self._canvas.bind_all("<MouseWheel>", lambda e: self._canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self._frame: Frame = Frame(self._canvas)
        self._canvas.create_window((0, 0), window=self._frame, anchor="nw")
        self._frame.bind("<Configure>", self._resetScrollregion)

        self._menuFrame: Frame = Frame(self._frame)
        self._menuFrame.grid(column=1, row=0)

        self._tableCount: int = 0
        self._tables: list[TableFrame] = []

        # Button for creating new Tables
        Button(self._menuFrame, text="Neue Tabelle", command=self._createTable).grid(column=1, row=0)

        # Entries for general Parameters

        LabelWithExtras(self._menuFrame, text="Zielpfad", description="Datei, in welche das Ergebnis\nals SQL-Befehl in Textformat\ngeschrieben wird.\nGeneriert einen zufälligen\nNamen wenn nicht angegeben.").grid(column=1, row=1)
        self._targetPath: Entry = Entry(self._menuFrame)
        self._targetPath.grid(column=2, row=1)

        Label(self._menuFrame, text="Filemodus").grid(column=1, row=2)
        self._filemode: StringVar = StringVar(self._menuFrame)
        self._filemode.set("Erstellen")
        OptionMenu(self._menuFrame, self._filemode, "Erstellen", "Anhängen", "Überschreiben").grid(column=2, row=2)

        self._noNewLine: BooleanVar = BooleanVar(self._menuFrame)
        cb:Checkbutton = Checkbutton(self._menuFrame, text="Keine neuen Zeilen", variable=self._noNewLine)
        cb.grid(column=1, row=3)
        ToolTip(cb, msg="Wenn aktiviert, wird der\ngesamte SQL-Befehl in eine Zeile geschrieben")

        LabelWithExtras(self._menuFrame, text="Localization", description="EXPERIMENTAL FEATURE\nKann für Addressen zu Fehlern führen.").grid(column=1, row=4)
        self._localization: Entry = Entry(self._menuFrame)
        self._localization.grid(column=2, row=4)
        self._localization.insert(INSERT, "de_DE")

        LabelWithExtras(self._menuFrame, text="Encoding", description="Zeichencodierung für die zu erstellende Datei").grid(column=1, row=5)
        self._encoding: Entry = Entry(self._menuFrame)
        self._encoding.grid(column=2, row=5)
        self._encoding.insert(INSERT, "utf-8")

        Label(self._menuFrame, text="SQL-Dialekt").grid(column=1, row=6)
        self._dialect: StringVar = StringVar(self._menuFrame)
        self._dialect.set(SqlDialect.DEFAULT.name)
        OptionMenu(self._menuFrame, self._dialect, *([d.name for d in SqlDialect])).grid(column=2, row=6)

        # generate Button
        Button(self._menuFrame, text="Generate", command=self.execute).grid(column=1, row=7)
        self._generateTextLabel: Optional[Label] = None

    def _createTable(self) -> None:
        """Creates a new TableFrame."""
        newTable: TableFrame = TableFrame(self._frame, self._getKeyColumns, self._getTypeColumns, self._removeTable)
        newTable.grid(column=2 + self._tableCount, row=0)
        self._tables.append(newTable)
        self._tableCount += 1

    def _getKeyColumns(self, perspective_table: TableFrame, perspective_column: ColumnFrame) -> list[str]:
        """Return a list of names of Columns with a key type."""
        keys: list[str] = []
        for t in self._tables:
            name: str = ""
            if t != perspective_table:
                if not t.entryName.get():
                    continue
                name = t.entryName.get() + "."
            for c in t.columns:
                if c != perspective_column and c.cd != None and c.cd.type in [Dt.PRIMARY_KEY, Dt.FOREIGN_KEY] and c.entryName.get():
                    keys.append(name + c.entryName.get())
        return keys
    
    def _getTypeColumns(self, typ: Dt, perspective_table: TableFrame, perspective_column: ColumnFrame) -> list[str]:
        """Returns a list of names of Columns of the given type."""
        names: list[str] = []
        for t in self._tables:
            name: str = ""
            if t != perspective_table:
                if not t.entryName.get():
                    continue
                name = t.entryName.get() + "."
            for c in t.columns:
                if c != perspective_column and c.cd != None and c.cd.type == typ and c.entryName.get():
                    names.append(name + c.entryName.get())
        return names
    
    def isFilled(self) -> str:
        """
        Returns an empty string when all required Entries that are part of the GUI have a valid input, making all inputs valid to be sent to the backend.
        If something is missing or invalid, an error message is returned instead.
        """
        if self._tableCount == 0:
            return "Keine Tabellen vorhanden"
        for t in self._tables:
            f: str = t.isFilled()
            if f:
                return f
        return ""
    
    def _removeTable(self, table: TableFrame) -> None:
        """Removes a specified TableFrame."""
        self._tables.remove(table)

    def getFilePath(self) -> Optional[str]:
        """Returns the filepath that was input, or None if none was input."""
        if self._targetPath.get():
            return self._targetPath.get()
        return None

    def getFilemode(self) -> str:
        """Returns the filemode that was input, or None if none was input."""
        res: str = self._filemode.get()
        if res == "Erstellen":
            return "x"
        elif res == "Anhängen":
            return "a"
        elif res == "Überschreiben":
            return "w"
        else:
            raise NotImplementedError()

    def execute(self) -> None:
        """
        Checks if all inputs are valid.
        Turns inputs into a dictionary.
        Sends dictionary to backend to generate the data.
        Puts a text about the success of this on the screen.
        """
        f: str = self.isFilled()
        if f:
            self._generateLabel(f'Unvollständige Eingabe:\n{f}')
            return
        json: list[dict[str, Any]] = [t.readValues() for t in self._tables]
        resultPath: Optional[str] = generateData(
            json,
            targetFilePath=self.getFilePath(),
            filemode=self.getFilemode(),
            noNewLine=self._noNewLine.get(),
            localization=self._localization.get(),
            encoding=self._encoding.get(),
            dialect=SqlDialect[self._dialect.get()]
        )
        if resultPath:
            self._generateLabel(f'Query wurde erfolgreich generiert unter\n{resultPath}')
        else:
            self._generateLabel("Unbekannter Fehler")

    def _generateLabel(self, text: str) -> None:
        """Creates a Label containing the result text of pressing the generate Button."""
        if self._generateTextLabel is not None:
            self._generateTextLabel.destroy()
        self._generateTextLabel = Label(self._menuFrame, text=text)
        self._generateTextLabel.grid(column=1, row=8)

    def _resetScrollregion(self, event: Any=None):
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))