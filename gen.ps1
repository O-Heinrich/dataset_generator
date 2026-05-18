param (
    [string]$p,
    [string]$f,
    [switch]$a = $false,
    [switch]$o = $false,
    [int]$n,
    [string]$e,
    [string]$d,
    [switch]$oneline = $false,
    [string]$l,
    [int]$seed
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

$Command = "python src/dataset_gen.py"
if (($PSBoundParameters.ContainsKey('p'))) {
    $Command = $Command + " -p " + $p
}
if ($PSBoundParameters.ContainsKey('f')) {
    $Command = $Command + " -f " + $f
}
if ($o) {
    $Command = $Command + " -o"
}
elseif ($a) {
    $Command = $Command + " -a"
}
if (($PSBoundParameters.ContainsKey('n'))) {
    $Command = $Command + " -n " + $n
}
if (($PSBoundParameters.ContainsKey('e'))) {
    $Command = $Command + " -e " + $e
}
if (($PSBoundParameters.ContainsKey('d'))) {
    $Command = $Command + " -d " + $d
}
if ($oneline) {
    $Command = $Command + " --oneline"
}
if (($PSBoundParameters.ContainsKey('l'))) {
    $Command = $Command + " -l " + $l
}
if (($PSBoundParameters.ContainsKey('seed'))) {
    $Command = $Command + " --seed " + $seed
}

Invoke-Expression $Command
deactivate