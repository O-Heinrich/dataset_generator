#!/bin/bash

if command -v python3 >/dev/null 2>&1
then
    python3 -m venv ./generator_venv
elif command -v python >/dev/null 2>&1
then
    python -m venv ./generator_venv
else
    echo "Could not find a Python installation"
    exit 1
fi
source ./generator_venv/bin/activate
pip install wonderwords
pip install Faker==40.4.0
pip install rstr
pip install mypy==1.18.2
pip install tkcalendar
pip install tkTimePicker
pip install tkinter-tooltip
pip install parameterized
pip install coverage
deactivate

sed -i 's/\r//g' start.sh
sed -i 's/\r//g' gen.sh
sed -i 's/\r//g' runTests.sh

cd src
srcPath=$(pwd)
cd ../generator_venv/lib
pythonPath=$(find . -type d -name "python*" | head -1)
cd $pythonPath
cd site-packages
echo $srcPath > paths.pth
cd ../../../..
exit 0
