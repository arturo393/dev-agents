param(
    [string]$SourceDir = (Split-Path -Parent $PSCommandPath),
    [string]$OutDir = "$env:USERPROFILE\.config\opencode\agents",
    [string]$FoundationFile = "$SourceDir\shared\foundation.md"
)

if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }

# Load shared foundation
$foundation = ""
if (Test-Path $FoundationFile) {
    $foundation = "`n" + (Get-Content -LiteralPath $FoundationFile -Raw) + "`n"
}

$files = Get-ChildItem -Path $SourceDir -Recurse -Filter "*.agent.md"
$count = 0

foreach ($f in $files) {
    $content = Get-Content -LiteralPath $f.FullName -Raw
    $lines = $content -split "`n"

    $inFront = $false
    $frontLines = @()
    $bodyStart = 0
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i].TrimEnd("`r")
        if ($line -eq '---') {
            if (-not $inFront) { $inFront = $true; continue }
            else { $bodyStart = $i + 1; break }
        }
        if ($inFront) { $frontLines += $line }
    }

    $baseName = $f.Name -replace '\.agent\.md$', ''
    $bodyLines = $lines[$bodyStart..($lines.Count-1)] | ForEach-Object { $_ -replace "`r$", '' }
    $body = ($bodyLines -join "`n").TrimStart()

    $output = "---`n" + ($frontLines -join "`n") + "`n---`n`n" + $foundation + $body
    $outPath = Join-Path $OutDir "$baseName.md"
    Set-Content -LiteralPath $outPath -Value $output -NoNewline
    $count++
}

Write-Output "Synced $count agents (foundation injected) from $SourceDir → $OutDir"
