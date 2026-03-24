from tkinter import *

class ListEntry(Frame):
    def __init__(self, root: Frame) -> None:
        super().__init__(root)
        self._entry: Entry = Entry(self)
        self._entry.grid(column=0, row=0)
        Button(self, text="Hinzufügen", command=self.write).grid(column=1, row=0)
        self.entries: list[Label] = []

    def write(self) -> None:
        inp: str = self._entry.get()
        newLabel = Label(self, text=inp)
        newLabel.grid(column=0, row=1+len(self.entries))
        b: Button = Button(self, text="remove")
        b.config(command=lambda:[newLabel.destroy, b.destroy])
        b.grid(column=1, row=1+len(self.entries))
        self.entries.append(newLabel)
        self._entry.delete(0, END)

    def get(self) -> list[str]:
        return [e["text"] for e in self.entries]