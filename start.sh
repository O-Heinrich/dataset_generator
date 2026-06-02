#!/bin/bash

if [ ! -d "generator_venv" ]; then
    echo "Did not find the virtual environment. Please use install.sh first."
    exit 1
fi
source ./generator_venv/bin/activate
python src/gui_gen.py -t                # Run without mypy type checking
deactivate
exit 0
