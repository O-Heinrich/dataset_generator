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
python src/gui_gen.py -t            # Run without mypy type checking
deactivate