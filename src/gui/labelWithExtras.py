from tkinter import Frame, Label
from tktooltip import ToolTip

class LabelWithExtras(Frame):
    """A Widget containing a Label, which additionally may have a symbol highlighting it's mandatory or a description on hover."""

    def __init__(self, root: Frame, text: str, required: bool=False, description: str="") -> None:
        super().__init__(root)
        label: Label = Label(self, text=text)
        label.grid(column=1, row=0)
        if required:
            Label(self, text="*", fg="red").grid(column=0, row=0)
        if description:
            ToolTip(label, msg=description)