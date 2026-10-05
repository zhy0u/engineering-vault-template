# Fallback sync when Obsidian is not running: commit everything, then pull and push.
# Usage: powershell -ExecutionPolicy Bypass -File scripts\sync.ps1
param([string]$Message = "")

$ErrorActionPreference = "Continue"
Set-Location (Split-Path $PSScriptRoot -Parent)

if ($Message -eq "") { $Message = "vault: sync " + (Get-Date -Format "yyyy-MM-dd HH:mm") }

git add -A
if (git status --porcelain) { git commit -m $Message }

$hasOrigin = git remote
if ($hasOrigin -contains "origin") {
    git pull --rebase --autostash
    if ($LASTEXITCODE -ne 0) { Write-Error "pull failed; resolve manually"; exit 1 }
    git push
} else {
    Write-Host "No origin remote; committed locally only."
}
