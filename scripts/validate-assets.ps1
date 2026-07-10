param(
    [string]$Root = "."
)

$ErrorActionPreference = "Stop"
$failures = New-Object System.Collections.Generic.List[string]

$thresholds = Join-Path $Root "config/quality-thresholds.yaml"
if (-not (Test-Path $thresholds)) {
    $failures.Add("Missing quality threshold source: config/quality-thresholds.yaml")
}

$gateReadme = Join-Path $Root "gates/README.md"
if (-not (Test-Path $gateReadme)) {
    $failures.Add("Missing Gate model: gates/README.md")
}
else {
    $gateText = Get-Content -Raw -LiteralPath $gateReadme
    foreach ($status in @("PASS", "FAIL", "WARN", "UNKNOWN", "NOT_APPLICABLE", "NOT_EXECUTED")) {
        if ($gateText -notmatch $status) {
            $failures.Add("Gate model missing status: $status")
        }
    }
}

$activePaths = @("commands", "skills", "global-settings/.claude/commands")
foreach ($path in $activePaths) {
    $full = Join-Path $Root $path
    if (-not (Test-Path $full)) { continue }
    $files = Get-ChildItem -Path $full -Filter "*.md" -Recurse -File -ErrorAction SilentlyContinue
    $matches = $files | Select-String -Pattern "extends\s+BaseMapper|继承\s+`?BaseMapper" -ErrorAction SilentlyContinue
    foreach ($m in $matches) {
        $failures.Add("Active asset still recommends BaseMapper: $($m.Path):$($m.LineNumber)")
    }
}

$formalFiles = @(
    "commands/formal-review.md",
    "global-settings/.claude/commands/formal-review.md"
)
foreach ($file in $formalFiles) {
    $full = Join-Path $Root $file
    if (Test-Path $full) {
        $text = Get-Content -Raw -LiteralPath $full
        if ($text -match "优先使用.*通过|避免P0|不通过.*慎用") {
            $failures.Add("formal-review still contains weak-decision wording: $file")
        }
    }
}

if ($failures.Count -gt 0) {
    $failures | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Host "Asset validation passed."
