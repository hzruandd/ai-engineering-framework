param(
    [string]$Root = "."
)

$ErrorActionPreference = "Stop"
$failures = New-Object System.Collections.Generic.List[string]
$warnings = New-Object System.Collections.Generic.List[string]

$skillDirs = Get-ChildItem -Path (Join-Path $Root "skills") -Directory -ErrorAction SilentlyContinue
foreach ($dir in $skillDirs) {
    $skill = Join-Path $dir.FullName "SKILL.md"
    if (-not (Test-Path $skill)) {
        $legacyJson = Join-Path $dir.FullName "skill.json"
        $legacyInstructions = Join-Path $dir.FullName "instructions.md"
        if ((Test-Path $legacyJson) -and (Test-Path $legacyInstructions)) {
            $warnings.Add("Legacy skill.json structure detected: $($dir.FullName)")
        }
        elseif ($dir.Name -notin @("openclaw")) {
            $failures.Add("Missing SKILL.md: $($dir.FullName)")
        }
        continue
    }

    $content = Get-Content -Raw -LiteralPath $skill
    if ($content -notmatch "(?s)^---\s.*?---") {
        $failures.Add("Missing YAML frontmatter: $skill")
        continue
    }
    if ($content -notmatch "(?m)^name:\s*") {
        $failures.Add("Missing name metadata: $skill")
    }
    if ($content -notmatch "(?m)^description:\s*") {
        $failures.Add("Missing description metadata: $skill")
    }
    if ($content -match "(?m)^allowed-tools:\s*.*Bash" -and $content -notmatch "失败|Failure|NOT_EXECUTED|降级") {
        $warnings.Add("Bash-capable legacy Skill should add explicit failure handling: $skill")
    }
}

foreach ($warning in $warnings) {
    Write-Warning $warning
}

if ($failures.Count -gt 0) {
    $failures | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Host "Skill validation passed."
