from tkinter import *
from gui.columnDetails import ALL_TYPES, ColumnDetails, ParameterDetails
from typing import Optional, Callable, Self, Union, Any
from gui.listEntry import ListEntry
from gui.timeDictEntry import TimeDictEntry
from gui.columnEntry import ColumnEntry
from gui.labelWithExtras import LabelWithExtras
from gui.datetimeEntry import DatetimeEntry
from gui.filepathEntry import FilepathEntry
from enums.inputType import InputType as It
from enums.datatypes import Datatype as Dt
from gui.entryInterface import EntryInterface

class ColumnFrame(Frame):
    """
    A Frame containing all Widgets for a single Column, including
    a delete Button,
    an Entry field for the name,
    an OptionMenu for the Datatype,
    Radiobuttons to choose between regular and independend types (subtypes)
    and Entry Widgets for Parameters, depending on the inserted Datatype, which can be opened in a seperate Popup Window.
    """

    def __init__(self,
                 root: Frame,
                 keyColumnLambda: Callable[[Self], list[str]], # Function, that returns all valid key Column names
                 columnLambda: Callable[[Dt, Self], list[str]], # Function, that returns all valid Column names
                 cleanupFunc: Callable[[Self], None] # Function to be called, when this Frame is destroyed
                 ) -> None:
        super().__init__(root)
        self._keyColumnLambda: Callable[[], list[str]] = lambda: keyColumnLambda(self)
        self._columnLambda: Callable[[Dt], list[str]] = lambda dt: columnLambda(dt, self)
        self._cleanupFunc: Callable[[], None] = lambda: cleanupFunc(self)
        # validators
        self._validateInt: str = (self.register(lambda P: P == "" or (all(char in "0123456789" for char in P[1:]) and P[0] in "0123456789-")))
        self._validateFloat: str = (self.register(lambda P: P == "" or (all(char in "0123456789." for char in P[1:]) and P[0] in "0123456789.-" and P.count(".") <= 1)))

        # delete Button
        Button(self, text="Spalte löschen", command=self._removeSelf).pack(side=LEFT, padx=5)

        # Entry for name
        LabelWithExtras(self, text="Spaltenname:", required=True).pack(side=LEFT, padx=5)
        validateName: str = (self.register(lambda P: str(P).replace("_", "").isalnum() and str(P).isascii()))
        self.entryName: Entry = Entry(self, validate="all", validatecommand=(validateName, "%P"))
        self.entryName.pack(side=LEFT, padx=5)

        # Entry for Datatype
        typeOptions: list[str] = list(ALL_TYPES.keys())
        self.entryType: StringVar = StringVar(self)
        self.entryType.set("")
        LabelWithExtras(self, text="Spaltentyp:", required=True).pack(side=LEFT, padx=5)
        OptionMenu(self, self.entryType, *typeOptions, command=self._onTypeChoice).pack(side=LEFT, padx=5)
        self.lastTyp: Optional[str] = None

        # Parameters
        self.cd: Optional[ColumnDetails] = None
        self.parameterLabels: list[LabelWithExtras] = []
        self.parameterEntries: dict[str, Union[Entry, EntryInterface]] = {}
        # Radiobuttons for subtypes
        self.radiobuttons: list[Radiobutton] = []
        self.radioValue: Optional[StringVar] = None
        self.extraParameterLabels: list[LabelWithExtras] = []
        self.extraParameterEntries: dict[str, Union[Entry, EntryInterface]] = {}
        # Popup Window
        self.popupButton: Optional[Button] = None
        self.window: Optional[Toplevel] = None
        self.windowFrame: Optional[Frame] = None

    def _onTypeChoice(self, var: Union[StringVar, str]) -> None:
        """Executed on changing the Datatype for this Column, to update the Radiobuttons and Parameters"""
        typ: str = var.get() if isinstance(var, StringVar) else var
        if typ == self.lastTyp:
            return
        self.lastTyp = typ

        # cleanup
        clearWidgets([self.parameterLabels, self.parameterEntries, self.radiobuttons, self.extraParameterLabels, self.extraParameterEntries])
        if self.window:
            self.window.destroy()
        # create new Popup Window
        self.window = Toplevel()
        self.windowFrame = Frame(self.window)

        self.cd = ALL_TYPES.get(typ)
        if not self.cd:
            raise KeyError()
        # create Entries for Parameters
        columnCount: int = 1
        for p in self.cd.parameters:
            opar: Optional[ParameterDetails] = self.cd.parameters.get(p)
            assert opar
            par: ParameterDetails = opar

            label: LabelWithExtras = LabelWithExtras(self.windowFrame, p, required=par.required, description=par.description)
            label.grid(column=columnCount, row=1)
            self.parameterLabels.append(label)

            self._createEntry(par, columnCount, 2, self.parameterEntries)
            columnCount += 1

        # create Radiobuttons for subtypes
        if self.cd.subtypes:
            rdFrame: Frame = Frame(self.windowFrame)
            rdFrame.grid(column=0, row=3)
            self.radioValue = StringVar(value="NORMAL")
            rd: Radiobutton = Radiobutton(rdFrame, text="Normal", variable=self.radioValue, value="NORMAL", command=lambda: clearWidgets([self.extraParameterLabels, self.extraParameterEntries]))
            self.radiobuttons.append(rd)
            rd.pack(anchor=W)
            for st in self.cd.subtypes:
                rdb: Radiobutton = Radiobutton(rdFrame, text=st, variable=self.radioValue, value=st, command=self._createSubEntries)
                self.radiobuttons.append(rdb)
                rdb.pack(anchor=W)

        # Button for Popup Window
        if self.popupButton:
            self.popupButton.destroy()
            self.popupButton = None
        if len(self.parameterLabels) + len(self.radiobuttons) + len(self.extraParameterLabels) > 0:
            self.popupButton = Button(self, text="Optionen", command=self._popupParameters)
            self.popupButton.pack(side=LEFT, padx=5)
            self.windowFrame.grid(column=0, row=0)
            Button(self.windowFrame, text="Schließen", command=self.window.withdraw).grid(column=0, row=0, sticky=W)
            self.window.protocol("WM_DELETE_WINDOW", self.window.withdraw)
            self.window.withdraw()
        else:
            self.window.destroy()
            self.window = None
            self.windowFrame = None

    def _createEntry(self, p: ParameterDetails, column: int, row: int, entrydict: dict[str, Union[Entry, EntryInterface]]) -> None:
        """
        Creates an Entry Widget to enter a Parameter with the given Parameterdetails.
        Adds the new Entry to this Frames Popup Window and to the given entrydict.
        """
        assert self.window and self.windowFrame
        entry: Union[Entry, EntryInterface]
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
            entry = TimeDictEntry(self.windowFrame, doDate=False)
        elif p.typ == It.DATEDICT:
            entry = TimeDictEntry(self.windowFrame, doTime=False)
        elif p.typ == It.DATETIMEDICT:
            entry = TimeDictEntry(self.windowFrame)
        elif p.typ == It.DATE:
            entry = DatetimeEntry(self.windowFrame, date=True)
        elif p.typ == It.TIME:
            entry = DatetimeEntry(self.windowFrame, time=True)
        elif p.typ == It.FILE_PATH:
            entry = FilepathEntry(self.windowFrame, self.window)
        else:
            raise NotImplementedError()
        entry.grid(column=column, row=row, padx=10, pady=10)
        if p.default:
            if p.typ in [It.STRING, It.INTEGER, It.FLOAT]:
                assert isinstance(entry, Entry)
                entry.insert(INSERT, str(p.default))
            elif p.typ in [It.TIMEDICT, It.DATEDICT, It.DATETIMEDICT]:
                assert isinstance(entry, TimeDictEntry)
                entry.insertDict(p.default)
            elif p.typ in [It.DATE, It.TIME]:
                assert isinstance(entry, DatetimeEntry)
                entry.insertDatetime(p.default)
            else:
                raise NotImplementedError()
        entrydict[p.name] = entry

    def _createSubEntries(self) -> None:
        """Executed on changing the subtype for this Column with the Radiobuttons, to update the Parameters with potential new Parameters"""
        assert self.window and self.windowFrame
        # cleanup
        clearWidgets([self.extraParameterLabels, self.extraParameterEntries])

        columnCount: int = 1
        assert self.cd and self.radioValue
        ocd: Optional[ColumnDetails] = self.cd.subtypes.get(self.radioValue.get())
        assert ocd
        cd: ColumnDetails = ocd
        # create Entries for Parameters
        for p in cd.parameters:
            opar: Optional[ParameterDetails] = cd.parameters.get(p)
            assert opar
            par: ParameterDetails = opar

            label: LabelWithExtras = LabelWithExtras(self.windowFrame, p, required=par.required, description=par.description)
            label.grid(column=columnCount, row=3)
            self.extraParameterLabels.append(label)

            self._createEntry(par, columnCount, 4, self.extraParameterEntries)
            columnCount += 1

    def isFilled(self) -> str:
        """
        Returns an empty string when all required Entries that are part of this Frame have a valid input, making this Column valid to be sent to the backend.
        If something is missing or invalid, an error message is returned instead.
        """
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

    def _popupParameters(self) -> None:
        """Opens the Popup Window for the Radiobuttons and Parameters."""
        assert self.window
        self.window.deiconify()

    def readKey(self) -> str:
        """Returns the name that was input for this Column."""
        return self.entryName.get()

    def readValue(self) -> Union[str, dict[str, Any]]:
        """
        Returns a dictionary according to the json required by the backend for each Column.
        May return just the name of the Datatype, if no Parameters where given,
        otherwise the dictionary contains the type, aswell as all Parameters that have a valid input.
        """
        ocd: Optional[ColumnDetails] = ALL_TYPES.get(self.entryType.get())
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
                if p.name in self.extraParameterEntries and self.extraParameterEntries[p.name].get():
                    self._insertDictValue(p.typ, p.name, self.extraParameterEntries[p.name].get(), result)

        if len(result) == 1:
            return result["type"]
        return result

    def _insertDictValue(self, pt: It, name: str, v: Any, dict: dict[str, Any]) -> None:
        """Insert the value into the given dictionary, and cast it depending on the given InputType."""
        if v is None:
            # Ignore attempts to insert a None value into the dictionary
            pass
        elif pt in [It.STRING, It.TABLE_KEY, It.TABLE_COLUMN, It.DATE, It.TIME]:
            dict[name] = str(v)
        elif v == "":
            # Empty inputs are ignored
            pass
        elif pt == It.INTEGER:
            dict[name] = int(v)
        elif pt == It.FLOAT:
            dict[name] = float(v)
        elif pt in [It.TIMEDICT, It.DATEDICT, It.DATETIMEDICT]:
            dict[name] = v.toDict()
        elif pt in [It.LIST_STRING, It.FILE_PATH]:
            dict[name] = v
        else:
            raise NotImplementedError()

    def _removeSelf(self) -> None:
        """Deletes this ColumnFrame and calls the cleanup function before."""
        self._cleanupFunc()
        self.destroy()

def clearWidgets(widgets: list[Union[list, dict]]) -> None:
    """Destroys all widgets in the given lists and dictionaries and clears all the given lists and dictionaries."""
    for l in widgets:
        for w in (l if isinstance(l, list) else l.values()):
            assert isinstance(w, Widget)
            w.destroy()
        l.clear()
