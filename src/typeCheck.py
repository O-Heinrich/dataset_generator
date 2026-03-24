import os
import subprocess
import platform

def typeCheck() -> None:
    # get python venv path
    python_path: str = ""
    if platform.system() == "Windows":
        scripts_path: str = os.path.join(".", "generator_venv", "Scripts", "python.exe")
        if os.path.exists(scripts_path):
            python_path = scripts_path
        else:
            python_path = os.path.join(".", "generator_venv", "bin", "python.exe")
    else:
        # assume linux, don't care about mac
        python_path = os.path.join(".", "generator_venv", "bin", "python")

    # type check
    type_check_return_code: int = subprocess.call([python_path, "-m", "mypy", "--config-file", "./mypy.ini", "./src/"])
    if type_check_return_code != 0:
        exit(type_check_return_code)