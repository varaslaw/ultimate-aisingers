. (Join-Path $PSScriptRoot "common.ps1")

Write-AISingersHeader "ДИАГНОСТИКА"

$reportPath = Join-Path $script:ProjectRoot "AISingers_диагностика.txt"
$lines = [System.Collections.Generic.List[string]]::new()

function Add-ReportLine {
    param([Parameter(Mandatory = $true)][string]$Text)
    $lines.Add($Text)
    Write-Host "  $Text"
}

Add-ReportLine "Дата: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
Add-ReportLine "Windows: $([Environment]::OSVersion.VersionString)"
Add-ReportLine "64-bit: $([Environment]::Is64BitOperatingSystem)"
Add-ReportLine "Папка: $script:ProjectRoot"
Add-ReportLine "Свободное место: $(Get-FreeSpaceGb) ГБ"

$videoCards = Get-NvidiaVideoCards
if ($videoCards.Count -gt 0) {
    Add-ReportLine "NVIDIA: $($videoCards -join ', ')"
}
else {
    Add-ReportLine "NVIDIA: не найдена"
}

$nvidiaSmi = Get-Command "nvidia-smi.exe" -ErrorAction SilentlyContinue
if ($null -ne $nvidiaSmi) {
    $driverReport = & $nvidiaSmi.Source --query-gpu=name,driver_version,memory.total --format=csv,noheader 2>&1 | Out-String
    Add-ReportLine "Драйвер NVIDIA: $($driverReport.Trim())"
}
else {
    Add-ReportLine "nvidia-smi: не найден (проверьте драйвер NVIDIA)"
}

Add-ReportLine "Visual C++ Runtime: $(Test-VCRuntimeInstalled)"
Add-ReportLine "uv.exe: $(Test-Path -LiteralPath $script:UvExe)"
Add-ReportLine "Python окружение: $(Test-Path -LiteralPath $script:VenvPython)"

if (Test-Path -LiteralPath $script:UvExe) {
    $uvVersion = & $script:UvExe --version 2>&1 | Out-String
    Add-ReportLine "uv: $($uvVersion.Trim())"
}

if (Test-AISingersInstalled) {
    $pythonReport = & $script:UvExe run --no-sync python -c "import gradio, torch; print('Python: OK'); print('Gradio:', gradio.__version__); print('PyTorch:', torch.__version__); print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'нет')" 2>&1 | Out-String
    foreach ($line in $pythonReport.Trim() -split "`r?`n") {
        Add-ReportLine $line
    }
}

$modelsPath = Join-Path $script:ProjectRoot "models"
$modelCount = 0
if (Test-Path -LiteralPath $modelsPath) {
    $modelCount = @(Get-ChildItem -LiteralPath $modelsPath -Recurse -Filter "*.pth" -ErrorAction SilentlyContinue).Count
}
Add-ReportLine "Найдено моделей .pth: $modelCount"

$lines | Set-Content -LiteralPath $reportPath -Encoding UTF8
Write-Host ""
Write-Host "  Отчёт сохранён: $reportPath" -ForegroundColor Green
Write-Host ""
