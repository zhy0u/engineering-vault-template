# Setup on a new computer after cloning the vault.
# Usage: powershell -ExecutionPolicy Bypass -File <vault>\scripts\setup-new-machine.ps1
# Safe to run again. It asks before each optional step and never deletes anything.
$ErrorActionPreference = "Continue"
$Vault = Split-Path $PSScriptRoot -Parent
Set-Location $Vault
Write-Host "Vault folder: $Vault"

function Ask($q) { $a = Read-Host "$q [y/N]"; return ($a -match '^(y|yes)$') }

# 1. Tools
$missing = @()
foreach ($t in @(
    @{n="git";    w="Git.Git"},
    @{n="python"; w="Python.Python.3.12"},
    @{n="claude"; w="Anthropic.ClaudeCode"})) {
    if (Get-Command $t.n -ErrorAction SilentlyContinue) { Write-Host "ok      $($t.n)" }
    else { Write-Warning "$($t.n) not found.  Install: winget install $($t.w)"; $missing += $t.n }
}
if ($missing -contains "git") { Write-Host "Install git, open a NEW terminal, run this script again."; exit 1 }

# 2. git identity (use your personal one, not an employer's)
$name = git config user.name; $mail = git config user.email
if (-not $name -or -not $mail) {
    Write-Warning "git user.name / user.email not set. Run:"
    Write-Host "  git config --global user.name 'Your Name'"
    Write-Host "  git config --global user.email 'you@example.com'"
} else { Write-Host "ok      git identity: $name <$mail>" }

# 3. Index hook (stored in .git/config, so it is needed once per clone)
git config core.hooksPath scripts/githooks
Write-Host "ok      core.hooksPath = $(git config core.hooksPath)"

# 4. Build the index once so it matches the files on this machine
if ($missing -notcontains "python") {
    python scripts\build_index.py
    python scripts\lint.py
}

# 5. Optional: user-level auto-capture hook in ~/.claude (not part of the repo)
if (($missing -notcontains "python") -and (Test-Path "_meta\user-level\install_user_level.py")) {
    if (Ask "Install the auto-capture hook in ~/.claude (other projects' Claude Code sessions will save general knowledge here)?") {
        python _meta\user-level\install_user_level.py --yes
    }
}

# 6. Optional: daily sync task
if (Ask "Create a daily 18:00 scheduled task that runs scripts\sync.ps1 (commit + pull + push)?") {
    $cmd = "powershell.exe -NoProfile -ExecutionPolicy Bypass -File `"$Vault\scripts\sync.ps1`""
    schtasks /Create /SC DAILY /ST 18:00 /TN "engineering-vault daily sync" /TR $cmd /F
}

Write-Host ""
Write-Host "Manual steps left:"
Write-Host "  1. Obsidian > Open folder as vault > $Vault"
Write-Host "  2. Settings > Community plugins > Turn on community plugins (Obsidian Git is already in the folder; switch it on)"
Write-Host "  3. Restart Obsidian once (autoSaveInterval = 1440 minutes)"
Write-Host "  4. cd $Vault ; claude   (choose 'trust this folder' the first time)"
