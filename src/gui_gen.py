from tkinter import *
from gui.app import App
from typeCheck import typeCheck
import argparse
import platform

parser = argparse.ArgumentParser()
parser.add_argument('-t', action="store_true", dest="no_type_check", default=False)
parsed: argparse.Namespace = parser.parse_args()
noTypeCheck: bool = parsed.no_type_check

if not noTypeCheck:
    typeCheck()

root = Tk()
if platform.system() == "Windows":
    root.state("zoomed")
app = App(root)
root.mainloop()