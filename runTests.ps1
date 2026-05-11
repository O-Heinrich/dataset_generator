param (
    [switch]$c = $false
)

./generator_venv/Scripts/Activate.ps1
cd src
if ($c) {
    python -m coverage run -m unittest
    python -m coverage html
    rm .coverage
}
else {
    python -m unittest
}
cd ..
deactivate