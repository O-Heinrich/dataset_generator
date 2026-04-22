from tkinter import Frame, Button, Label, Entry, Toplevel, filedialog, X, LEFT, RIGHT, E
from tktooltip import ToolTip
from gui.entryInterface import EntryInterface

class FilepathEntry(Frame, EntryInterface):
    """A Widget, which contains all elements to enter a filepath in the GUI."""

    def __init__(self, root: Frame, window: Toplevel) -> None:
        super().__init__(root)
        self._filepaths: dict[str, Entry] = {}
        Button(self, text="Dateien importieren", command=lambda: self._addFilepaths(window)).pack()

    def _addFilepaths(self, window: Toplevel) -> None:
        window.withdraw()
        filenames: list[str] = list(filedialog.askopenfilenames())
        for filename in filenames:
            self._addFilepath(filename)
        window.deiconify()

    def _addFilepath(self, filename) -> None:
        frame: Frame = Frame(self)
        frame.pack(fill=X)
        Label(frame, text=filename).pack(side=LEFT, fill=X)
        Button(frame, text="löschen", command=lambda: self._removeValue(filename, frame)).pack(side=RIGHT, anchor=E)
        e: Entry = Entry(frame)
        e.pack(side=RIGHT, anchor=E)
        ToolTip(e, msg="Seperator, leerlassen für newline")
        self._filepaths[filename] = e

    def get(self) -> dict[str, str]:
        return {n:e.get() for n, e in self._filepaths.items()}

    def _removeValue(self, name: str, frame: Frame) -> None:
        del self._filepaths[name]
        frame.destroy()