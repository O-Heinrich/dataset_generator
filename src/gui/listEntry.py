from tkinter import Frame, Button, Label, Entry, END, LEFT, RIGHT, E, X
from gui.entryInterface import EntryInterface

class ListEntry(Frame, EntryInterface):
    """A Widget, which contains all elements to enter a list of strings in the GUI."""

    def __init__(self, root: Frame) -> None:
        super().__init__(root)
        headFrame: Frame = Frame(self)
        headFrame.pack()
        self._entry: Entry = Entry(headFrame)
        self._entry.pack(side=LEFT, padx=15)
        Button(headFrame, text="Hinzufügen", command=self._write).pack(side=LEFT)
        self._entries: list[Label] = []

    def _write(self) -> None:
        inp: str = self._entry.get()
        frame: Frame = Frame(self)
        frame.pack(fill=X)
        newLabel = Label(frame, text=inp)
        newLabel.pack(side=LEFT, padx=15)
        b: Button = Button(frame, text="löschen", command=lambda: self._removeValue(newLabel, frame))
        b.pack(side=RIGHT, anchor=E)
        self._entries.append(newLabel)
        self._entry.delete(0, END)

    def get(self) -> list[str]:
        """Return the list that is currently input into this ListEntry."""
        return [e["text"] for e in self._entries]
    
    def _removeValue(self, label: Label, f: Frame) -> None:
        self._entries.remove(label)
        f.destroy()