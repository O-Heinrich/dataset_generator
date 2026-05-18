#!/bin/bash

if [ ! -d "generator_venv" ]; then
    echo "Did not find the virtual environment. Please use install.sh first."
    exit 1
fi
source ./generator_venv/bin/activate
python src/gui_gen.py -t
deactivate
exit 0
