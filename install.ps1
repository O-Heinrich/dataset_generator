python -m venv generator_venv
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

cd src
$srcPath = (Get-Item .).FullName
cd ../generator_venv/lib
$pythonPath = Get-ChildItem -Directory | Where-Object {$_.Name -match "^python.*"}
if ($pythonPath) {
    cd $pythonPath
}
cd site-packages
echo $srcPath > paths.pth
cd ../../..
if ($pythonPath) {
    cd ..
}