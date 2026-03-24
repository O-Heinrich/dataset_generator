from tkinter import *
from gui.columnDetails import allTypes, ColumnDetails, ParameterDetails
from typing import Optional, Callable, Self, Union, Any
from gui.listEntry import ListEntry
from gui.timeDictEntry import TimeDictEntry
from gui.columnEntry import ColumnEntry
from gui.labelWithExtras import LabelWithExtras
from gui.datetimeEntry import DatetimeEntry
from enums.inputType import InputType as It
from enums.datatypes import Datatype as Dt

class ColumnFrame(Frame):
    def __init__(self,
                 root: Frame,
                 keyColumnLambda: Callable[[Self], list[str]],
                 columnLambda: Callable[[Dt, Self], list[str]],
                 cleanupFunc: Callable[[Self], None]
                 ) -> None:
        super().__init__(root)
        self._keyColumnLambda: Callable[[], list[str]] = lambda: keyColumnLambda(self)
        self._columnLambda: Callable[[Dt], list[str]] = lambda dt: columnLambda(dt, self)
        self._cleanupFunc: Callable[[], None] = lambda: cleanupFunc(self)
        self._validateInt: str = (self.register(lambda P: str.isdigit(P) or P == ""))
        self._validateFloat: str = (self.register(lambda P: P == "" or (all(char in "0123456789." for char in P[1:]) and P[0] in "0123456789.-" and P.count(".") <= 1)))

        Button(self, text="Spalte löschen", command=self.removeSelf).grid(column=0, row=0)

        LabelWithExtras(self, text="Spaltenname:", required=True).grid(column=1, row=0)
        validateName: str = (self.register(lambda P: str(P).replace("_", "").isalnum() and str(P).isascii()))
        self.entryName: Entry = Entry(self, validate="all", validatecommand=(validateName, "%P"))
        self.entryName.grid(column=2, row=0)

        typeOptions: list[str] = list(allTypes.keys())
        self.entryType: StringVar = StringVar(self)
        self.entryType.set("")
        LabelWithExtras(self, text="Spaltentyp:", required=True).grid(column=3, row=0)
        OptionMenu(self, self.entryType, *typeOptions, command=self.onTypeChoice).grid(column=4, row=0)
        self.lastTyp: Optional[str] = None

        self.cd: Optional[ColumnDetails] = None
        self.parameterLabels: list[LabelWithExtras] = []
        self.parameterEntries: dict[str, Union[Entry, ColumnEntry, ListEntry, TimeDictEntry, DatetimeEntry]] = {}
        self.radiobuttons: list[Radiobutton] = []
        self.radioValue: Optional[StringVar] = None
        self.extraParameterLabels: list[LabelWithExtras] = []
        self.extraParameterEntries: dict[str, Union[Entry, ColumnEntry, ListEntry, TimeDictEntry, DatetimeEntry]] = {}
        self.popupButton: Optional[Button] = None
        self.window: Optional[Toplevel] = None
        self.windowFrame: Optional[Frame] = None

    def onTypeChoice(self, var: Union[StringVar, str]) -> None:
        typ: str = var.get() if isinstance(var, StringVar) else var
        if typ == self.lastTyp:
            return
        self.lastTyp = typ
        clearWidgets([self.parameterLabels, self.parameterEntries, self.radiobuttons, self.extraParameterLabels, self.extraParameterEntries])
        if self.window:
            self.window.destroy()
        self.window = Toplevel()
        self.windowFrame = Frame(self.window)

        self.cd = allTypes.get(typ)
        if not self.cd:
            raise KeyError()
        columnCount: int = 1
        for p in self.cd.parameters:
            pn: Optional[ParameterDetails] = self.cd.parameters.get(p)
            assert pn
            par: ParameterDetails = pn
            label: LabelWithExtras = LabelWithExtras(self.windowFrame, p, required=par.required, description=par.description)
            label.grid(column=columnCount, row=0)
            self.parameterLabels.append(label)

            self.createEntry(par, columnCount, self.parameterEntries)
            columnCount += 1
        if self.cd.subtypes:
            rowCount: int = 1
            self.radioValue = StringVar(value="NORMAL")
            rd: Radiobutton = Radiobutton(self.windowFrame, text="Normal", variable=self.radioValue, value="NORMAL", command=lambda: clearWidgets([self.extraParameterLabels, self.extraParameterEntries]))
            self.radiobuttons.append(rd)
            rd.grid(column=0, row=rowCount)
            for st in self.cd.subtypes:
                rowCount += 1
                rdb: Radiobutton = Radiobutton(self.windowFrame, text=st, variable=self.radioValue, value=st, command=self.createSubEntries)
                self.radiobuttons.append(rdb)
                rdb.grid(column=0, row=rowCount)

        if self.popupButton:
            self.popupButton.destroy()
            self.popupButton = None
        if len(self.parameterLabels) + len(self.radiobuttons) + len(self.extraParameterLabels) > 0:
            self.popupButton = Button(self, text="Optionen", command=self.popupParameters)
            self.popupButton.grid(column=5, row=0)
            self.windowFrame.grid(column=0, row=0)
            Button(self.windowFrame, text="Schließen", command=self.window.withdraw).grid(column=0, row=0)
            self.window.protocol("WM_DELETE_WINDOW", self.window.withdraw)
            self.window.withdraw()
        else:
            self.window.destroy()
            self.window = None
            self.windowFrame = None

    def createEntry(self, p: ParameterDetails, column: int, entrydict: dict[str, Union[Entry, ColumnEntry, ListEntry, TimeDictEntry, DatetimeEntry]]) -> None:
        assert self.window and self.windowFrame
        entry: Union[Entry, ColumnEntry, ListEntry, TimeDictEntry, DatetimeEntry]
        if p.typ == It.STRING:
            entry = Entry(self.windowFrame)
        elif p.typ == It.INTEGER:
            entry = Entry(self.windowFrame, validate="all", validatecommand=(self._validateInt, "%P"))
        elif p.typ == It.FLOAT:
            entry = Entry(self.windowFrame, validate="all", validatecommand=(self._validateFloat, "%P"))
        elif p.typ == It.TABLE_KEY:
            entry = ColumnEntry(self.windowFrame, self._keyColumnLambda)
        elif p.typ == It.TABLE_COLUMN:
            ocd: Optional[ColumnDetails] = self.cd
            assert ocd
            entry = ColumnEntry(self.windowFrame, lambda: self._columnLambda(ocd.type))
        elif p.typ == It.LIST_STRING:
            entry = ListEntry(self.windowFrame)
        elif p.typ == It.TIMEDICT:
            entry = TimeDictEntry(self.windowFrame)
        elif p.typ == It.DATE:
            entry = DatetimeEntry(self.windowFrame, date=True)
        elif p.typ == It.TIME:
            entry = DatetimeEntry(self.windowFrame, time=True)
        else:
            raise NotImplementedError()
        entry.grid(column=column, row=1)
        if p.default:
            if p.typ in [It.STRING, It.INTEGER, It.FLOAT]:
                assert isinstance(entry, Entry)
                entry.insert(INSERT, str(p.default))
            elif p.typ == It.TIMEDICT:
                assert isinstance(entry, TimeDictEntry)
                entry.insertDict(p.default)
            elif p.typ in [It.DATE, It.TIME]:
                assert isinstance(entry, DatetimeEntry)
                entry.insertDatetime(p.default)
            else:
                raise NotImplementedError()
        entrydict[p.name] = entry

    def createSubEntries(self) -> None:
        assert self.window and self.windowFrame
        clearWidgets([self.extraParameterLabels, self.extraParameterEntries])
        columnCount: int = 1 + len(self.parameterEntries)
        assert self.cd and self.radioValue
        ocd: Optional[ColumnDetails] = self.cd.subtypes.get(self.radioValue.get())
        assert ocd
        cd: ColumnDetails = ocd
        for p in cd.parameters:
            opar: Optional[ParameterDetails] = cd.parameters.get(p)
            assert opar
            par: ParameterDetails = opar
            label:LabelWithExtras = LabelWithExtras(self.windowFrame, p, required=par.required, description=par.description)
            label.grid(column=columnCount, row=0)
            self.extraParameterLabels.append(label)
            self.createEntry(par, columnCount, self.extraParameterEntries)
            columnCount += 1

    def isFilled(self) -> str:
        if not self.entryName.get():
            return "Fehlender Spaltenname"
        if not self.entryType.get():
            return f'Spalte {self.entryName.get()} hat keinen Typ'
        if not self.cd:
            return "Unbekannter Fehler"
        cd: ColumnDetails = self.cd
        for p in cd.parameters.values():
            if p.required and not self.parameterEntries[p.name].get():
                return f'Spalte {self.entryName.get()} benötigt Parameter {p.name}'
        if cd.subtypes:
            if not self.radioValue:
                return "Unbekannter Fehler"
            if self.radioValue.get() == "NORMAL":
                return ""
            for p in cd.subtypes[self.radioValue.get()].parameters.values():
                if p.required and not self.extraParameterEntries[p.name].get():
                    return f'Spalte {self.entryName.get()} benötigt Parameter {p.name}'
        return ""

    def popupParameters(self) -> None:
        assert self.window
        self.window.deiconify()

    def readKey(self) -> str:
        return self.entryName.get()

    def readValue(self) -> Union[str, dict[str, Any]]:
        ocd: Optional[ColumnDetails] = allTypes.get(self.entryType.get())
        assert ocd
        cd: ColumnDetails = ocd
        result: dict[str, Any] = {"type": cd.type.name}
        for p in cd.parameters.values():
            if p.name in self.parameterEntries and self.parameterEntries[p.name].get():
                self._insertDictValue(p.typ, p.name, self.parameterEntries[p.name].get(), result)
        
        if self.radioValue and self.radioValue.get() != "NORMAL":
            scd: ColumnDetails = cd.subtypes[self.radioValue.get()]
            result["type"] = scd.type.name
            for p in scd.parameters.values():
                self._insertDictValue(p.typ, p.name, self.extraParameterEntries[p.name].get(), result)

        if len(result) == 1:
            return result["type"]
        return result

    def _insertDictValue(self, pt: It, name: str, v: Any, dict: dict[str, Any]) -> None:
        if not v:
            pass
        elif pt in [It.STRING, It.TABLE_KEY, It.TABLE_COLUMN, It.DATE, It.TIME]:
            dict[name] = str(v)
        elif pt == It.INTEGER:
            dict[name] = int(v)
        elif pt == It.FLOAT:
            dict[name] = float(v)
        elif pt == It.TIMEDICT:
            dict[name] = v.toDict()
        elif pt == It.LIST_STRING:
            dict[name] = v
        else:
            raise NotImplementedError()

    def removeSelf(self) -> None:
        self._cleanupFunc()
        self.destroy()

def clearWidgets(widgets: list[Union[list, dict]]) -> None:
    for l in widgets:
        for w in (l if isinstance(l, list) else l.values()):
            assert isinstance(w, Widget)
            w.destroy()
        l.clear()
