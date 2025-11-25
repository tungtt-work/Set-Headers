# PowerShell script to install git hooks
# This will copy hooks from hooks/ directory to .git/hooks/

$ErrorActionPreference = "Stop"

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$GitHooksDir = Join-Path $ProjectRoot ".git\hooks"

# Check if we're in a git repository
if (-not (Test-Path (Join-Path $ProjectRoot ".git"))) {
    Write-Host "Error: Not a git repository. Please run 'git init' first." -ForegroundColor Red
    exit 1
}

# Create .git/hooks directory if it doesn't exist
if (-not (Test-Path $GitHooksDir)) {
    New-Item -ItemType Directory -Path $GitHooksDir -Force | Out-Null
}

# Install pre-commit hook
$PreCommitHook = Join-Path $ScriptDir "pre-commit"
if (Test-Path $PreCommitHook) {
    Copy-Item $PreCommitHook $GitHooksDir -Force
    Write-Host "✓ Installed pre-commit hook" -ForegroundColor Green
} else {
    Write-Host "Warning: pre-commit hook not found in hooks/ directory" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Git hooks installed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "To test the hook, try:" -ForegroundColor Cyan
Write-Host "  git add <file>"
Write-Host "  git commit -m 'test'"
Write-Host ""

