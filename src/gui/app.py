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
    def __init__(self, root) -> None:
        horizontalScroll: Scrollbar = Scrollbar(root, orient=HORIZONTAL)
        horizontalScroll.pack(side=TOP, fill=X)
        verticalScroll: Scrollbar = Scrollbar(root, orient=VERTICAL)
        verticalScroll.pack(side=LEFT, fill=Y)
        self.canvas: Canvas = Canvas(root)
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)
        horizontalScroll.configure(command=self.canvas.xview)
        verticalScroll.configure(command=self.canvas.yview)
        self.canvas.configure(xscrollcommand=horizontalScroll.set, yscrollcommand=verticalScroll.set)
        self.canvas.bind_all("<MouseWheel>", lambda e: self.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self._frame: Frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self._frame, anchor="nw")
        self._frame.bind("<Configure>", self.reset_scrollregion)

        self._menuFrame: Frame = Frame(self._frame)
        self._menuFrame.grid(column=1, row=0)

        self._tableCount: int = 0
        self._tables: list[TableFrame] = []

        Button(self._menuFrame, text="Neue Tabelle", command=self._createTable).grid(column=1, row=0)

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

        Button(self._menuFrame, text="Generate", command=self.execute).grid(column=1, row=7)
        self._generateTextLabel: Optional[Label] = None

    def _createTable(self) -> None:
        newTable: TableFrame = TableFrame(self._frame, self.getKeyColumns, self.getTypeColumns, self.removeTable)
        newTable.grid(column=2 + self._tableCount, row=0)
        self._tables.append(newTable)
        self._tableCount += 1

    def getKeyColumns(self, perspective_table: TableFrame, perspective_column: ColumnFrame) -> list[str]:
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
    
    def getTypeColumns(self, typ: Dt, perspective_table: TableFrame, perspective_column: ColumnFrame) -> list[str]:
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
        if self._tableCount == 0:
            return "Keine Tabellen vorhanden"
        for t in self._tables:
            f: str = t.isFilled()
            if f:
                return f
        return ""
    
    def removeTable(self, table: TableFrame) -> None:
        self._tables.remove(table)

    def getFilePath(self) -> Optional[str]:
        if self._targetPath.get():
            return self._targetPath.get()
        return None

    def getFilemode(self) -> str:
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
        if self._generateTextLabel is not None:
            self._generateTextLabel.destroy()
        self._generateTextLabel = Label(self._menuFrame, text=text)
        self._generateTextLabel.grid(column=1, row=8)

    def reset_scrollregion(self, event: Any=None):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))