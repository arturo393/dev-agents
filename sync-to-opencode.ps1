param(
    [string]$Destination = "$env:USERPROFILE\.config\opencode\agents"
)

$Source = Split-Path -Parent $PSCommandPath

Write-Host "Syncing dev-agents → $Destination" -ForegroundColor Cyan

$files = @()
$files += Get-ChildItem (Join-Path $Source "uqomm/agents") -Filter "*.agent.md"
$files += Get-ChildItem (Join-Path $Source "personal") -Filter "*.agent.md"
$files += Get-ChildItem (Join-Path $Source "shared/experts") -Filter "*.agent.md"

if (-not (Test-Path $Destination)) {
    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
}

foreach ($f in $files) {
    $destName = $f.Name -replace '\.agent\.md$', '.md'
    Copy-Item -LiteralPath $f.FullName -Destination (Join-Path $Destination $destName) -Force
    Write-Host "  [OK] $destName" -ForegroundColor Green
}

Write-Host "`nDone. $( $files.Count ) agents synced." -ForegroundColor Cyan
