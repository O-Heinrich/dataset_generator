#!/bin/bash

if [ ! -d "generator_venv" ]; then
    echo "Did not find the virtual environment. Please use install.sh first."
    exit 1
fi

c=false

print_usage() {
    printf "Usage:\nFlags:\n-c: Generate coverage report\n"
}

while getopts 'c' flag; do
    case "${flag}" in
        c) c=true ;;
        *) print_usage
            exit 1 ;;
    esac
done

source ./generator_venv/bin/activate
cd src
if $c;
then
    python -m coverage run -m unittest
    python -m coverage html
    rm .coverage
else
    python -m unittest
fi
cd ..
deactivate
exit 0
