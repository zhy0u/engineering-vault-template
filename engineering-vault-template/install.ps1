# Install your own copy of the vault from this template.
# Usage:
#   powershell -ExecutionPolicy Bypass -File install.ps1                          # creates %USERPROFILE%\engineering-vault
#   powershell -ExecutionPolicy Bypass -File install.ps1 -Path D:\my-vault
#   powershell -ExecutionPolicy Bypass -File install.ps1 -Path D:\my-vault -Github  # also a private GitHub repo
# It never overwrites: if the target folder exists and is not empty it stops.
param(
    [string]$Path = (Join-Path $env:USERPROFILE "engineering-vault"),
    [switch]$Github,
    [string]$Repo = ""
)
$ErrorActionPreference = "Continue"
$src = Join-Path $PSScriptRoot "vault-template"
if (-not (Test-Path $src)) { Write-Host "vault-template folder not found next to install.ps1"; exit 1 }

if ((Test-Path $Path) -and (Get-ChildItem $Path -Force | Select-Object -First 1)) {
    Write-Host "$Path already exists and is not empty. Pick another -Path."; exit 1
}
New-Item -ItemType Directory -Force -Path $Path | Out-Null
Copy-Item -Path (Join-Path $src "*") -Destination $Path -Recurse -Force
Write-Host "Copied the template to $Path"

$args2 = @("-ExecutionPolicy", "Bypass", "-File", (Join-Path $Path "scripts\bootstrap.ps1"))
if ($Github) { $args2 += "-Github" }
if ($Repo -ne "") { $args2 += @("-Repo", $Repo) }
powershell @args2
if ($LASTEXITCODE -ne 0) { Write-Host "bootstrap did not finish; fix the message above and run: powershell -File `"$Path\scripts\bootstrap.ps1`""; exit 1 }

Write-Host ""
Write-Host "Next (optional extras, each asks first):"
Write-Host "  powershell -ExecutionPolicy Bypass -File `"$Path\scripts\setup-new-machine.ps1`""
