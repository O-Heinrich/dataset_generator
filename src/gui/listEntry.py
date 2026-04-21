from tkinter import Frame, Button, Label, Entry, END

class ListEntry(Frame):
    """A Widget, which contains all elements to enter a list of strings in the GUI."""

    def __init__(self, root: Frame) -> None:
        super().__init__(root)
        self._entry: Entry = Entry(self)
        self._entry.grid(column=0, row=0)
        Button(self, text="Hinzufügen", command=self._write).grid(column=1, row=0)
        self.entries: list[Label] = []

    def _write(self) -> None:
        inp: str = self._entry.get()
        newLabel = Label(self, text=inp)
        newLabel.grid(column=0, row=1+len(self.entries))
        b: Button = Button(self, text="remove")
        b.config(command=lambda:[newLabel.destroy, b.destroy])
        b.grid(column=1, row=1+len(self.entries))
        self.entries.append(newLabel)
        self._entry.delete(0, END)

    def get(self) -> list[str]:
        """Return the list that is currently input into this ListEntry."""
        return [e["text"] for e in self.entries]