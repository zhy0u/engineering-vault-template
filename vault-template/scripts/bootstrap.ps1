# One-time setup of a NEW vault: git init, first commit, optionally create a private GitHub repo with gh and push.
# Usage (from the vault folder):
#   powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1                    # local git only
#   powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1 -Github            # also create a PRIVATE repo <you>/engineering-vault and push
#   powershell -ExecutionPolicy Bypass -File scripts\bootstrap.ps1 -Github -Repo you/my-notes
param(
    [switch]$Github,
    [string]$Repo = ""
)

$ErrorActionPreference = "Continue"
Set-Location (Split-Path $PSScriptRoot -Parent)
Write-Host "Vault folder: $(Get-Location)"

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "git not found. Install with: winget install Git.Git   (then open a NEW terminal)"; exit 1
}
if (-not (git config user.name) -or -not (git config user.email)) {
    Write-Host "git user.name / user.email not set. Run:"
    Write-Host "  git config --global user.name 'Your Name'"
    Write-Host "  git config --global user.email 'you@example.com'"
    exit 1
}

if (-not (Test-Path ".git")) { git init -b main }
git config core.hooksPath scripts/githooks

$py = $null
foreach ($c in @("python", "python3", "py")) { if (Get-Command $c -ErrorAction SilentlyContinue) { $py = $c; break } }
if ($py) {
    & $py scripts\build_index.py
    & $py scripts\lint.py
} else {
    Write-Warning "Python not found; indexes will not be generated. Install with: winget install Python.Python.3.12"
}

git add -A
if (git status --porcelain) { git commit -m "vault: initial structure, templates, scripts and Claude config" }

if ($Github) {
    if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
        Write-Host "gh not found. Install with: winget install GitHub.cli   then: gh auth login"; exit 1
    }
    gh auth status
    if ($LASTEXITCODE -ne 0) { Write-Host "gh is not logged in. Run: gh auth login"; exit 1 }
    if ($Repo -eq "") { $Repo = "$(gh api user -q .login)/engineering-vault" }

    gh repo view $Repo 2>$null | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Repo $Repo already exists; adding it as origin and pushing."
        if (-not ((git remote) -contains "origin")) { git remote add origin "https://github.com/$Repo.git" }
        git push -u origin main
    } else {
        gh repo create $Repo --private --source . --remote origin --push --description "Personal engineering knowledge vault (Obsidian)"
    }
    if ($LASTEXITCODE -ne 0) { Write-Host "Creating or pushing the repo failed."; exit 1 }
    gh repo view $Repo --json visibility,url
}

Write-Host ""
git status -sb
Write-Host "Done. Open this folder in Obsidian and enable community plugins when prompted."
