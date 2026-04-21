from tkinter import Tk
from gui.app import App
from typeCheck import typeCheck
import argparse
import platform

# allow passing arguments on commmand line
parser = argparse.ArgumentParser()
parser.add_argument('-t', action="store_true", dest="no_type_check", default=False)
parsed: argparse.Namespace = parser.parse_args()
noTypeCheck: bool = parsed.no_type_check
# static type checking with mypy
if not noTypeCheck:
    typeCheck()

# create top level tkinter widget and initialize App
root = Tk()
root.title("dataset_generator")
if platform.system() == "Windows":
    root.state("zoomed")
app = App(root)
root.mainloop()