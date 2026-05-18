param (
    [switch]$c = $false
)

if (Test-Path -Path './generator_venv/Scripts') {
    ./generator_venv/Scripts/Activate.ps1
}
elseif (Test-Path -Path './generator_venv/bin') {
    ./generator_venv/bin/Activate.ps1
}
else {
    Write-Output "Virtual Environment has neither Scripts nor bin directory"
    exit 1
}
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