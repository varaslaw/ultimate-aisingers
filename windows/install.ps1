. (Join-Path $PSScriptRoot "common.ps1")

Write-AISingersHeader "УСТАНОВКА"

try {
    if (-not [Environment]::Is64BitOperatingSystem) {
        throw "AISingers поддерживает только 64-битную Windows."
    }

    Write-Host "  Установка выполняется в папку проекта и не требует системного Python." -ForegroundColor Gray
    Write-Host "  Папка: $script:ProjectRoot" -ForegroundColor DarkGray

    $freeSpace = Get-FreeSpaceGb
    if ($freeSpace -ge 0) {
        Write-Host "  Свободно на диске: $freeSpace ГБ" -ForegroundColor Gray
        if ($freeSpace -lt 15) {
            Write-Host "  ВНИМАНИЕ: рекомендуется не менее 15 ГБ свободного места." -ForegroundColor Yellow
        }
    }

    $videoCards = @(Get-NvidiaVideoCards)
    if ($videoCards.Count -gt 0) {
        Write-Host "  NVIDIA: $($videoCards -join ', ')" -ForegroundColor Green
    }
    else {
        Write-Host "  NVIDIA-видеокарта не обнаружена. Работа на CPU будет очень медленной." -ForegroundColor Yellow
    }

    foreach ($directory in @(
        $script:RuntimeRoot,
        $script:RuntimeBin,
        $script:PythonRoot,
        $script:UvRoot,
        $script:UvCache,
        (Join-Path $script:ProjectRoot "models"),
        (Join-Path $script:ProjectRoot "audio"),
        (Join-Path $script:ProjectRoot "temp"),
        (Join-Path $script:ProjectRoot "config"),
        (Join-Path $script:ProjectRoot "logs")
    )) {
        New-Item -ItemType Directory -Path $directory -Force | Out-Null
    }

    Write-Step 1 "Проверка Microsoft Visual C++ Runtime"
    if (Test-VCRuntimeInstalled) {
        Write-Host "  Уже установлен." -ForegroundColor Green
    }
    else {
        Write-Host "  Компонент не найден. Будет открыт стандартный установщик Microsoft." -ForegroundColor Yellow
        $vcInstaller = Join-Path $script:RuntimeRoot "vc_redist.x64.exe"
        Invoke-WebRequest -UseBasicParsing -Uri "https://aka.ms/vc14/vc_redist.x64.exe" -OutFile $vcInstaller
        $process = Start-Process -FilePath $vcInstaller -ArgumentList "/install", "/quiet", "/norestart" -Verb RunAs -Wait -PassThru
        if ($process.ExitCode -notin @(0, 1638, 3010)) {
            Write-Host "  Visual C++ Runtime вернул код $($process.ExitCode). Установка AISingers продолжится." -ForegroundColor Yellow
        }
    }

    Write-Step 2 "Установка локального менеджера Python"
    if (-not (Test-Path -LiteralPath $script:UvExe)) {
        $installScript = Invoke-RestMethod -UseBasicParsing -Uri "https://astral.sh/uv/0.9.11/install.ps1"
        Invoke-Expression $installScript
    }
    if (-not (Test-Path -LiteralPath $script:UvExe)) {
        throw "Не удалось установить uv.exe. Проверьте интернет и антивирус."
    }
    Invoke-CheckedCommand $script:UvExe "--version"

    Write-Step 3 "Загрузка локального Python 3.12"
    Invoke-CheckedCommand $script:UvExe "python" "install" "3.12" "--managed-python"

    Write-Step 4 "Установка AISingers, RVC, PyTorch и CUDA-библиотек"
    Write-Host "  Это самый долгий этап. Окно не зависло — дождитесь завершения загрузки." -ForegroundColor Yellow
    Invoke-CheckedCommand $script:UvExe "sync" "--python" "3.12" "--extra" "cuda" "--prerelease" "if-necessary-or-explicit" "--no-dev"

    Write-Step 5 "Загрузка служебных моделей RVC"
    Invoke-CheckedCommand $script:UvExe "run" "--no-sync" "python" "./src/ultimate_rvc/core/main.py"

    Write-Step 6 "Проверка готовности"
    Invoke-CheckedCommand $script:UvExe "run" "--no-sync" "python" "-c" "import gradio, torch; print('  Gradio:', gradio.__version__); print('  PyTorch:', torch.__version__); print('  CUDA доступна:', torch.cuda.is_available()); print('  Видеокарта:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'не найдена')"

    $installationInfo = [ordered]@{
        installed_at = (Get-Date).ToString("o")
        python = "3.12"
        accelerator = "cuda"
        project = "AISingers Studio"
    }
    $installationInfo | ConvertTo-Json | Set-Content -LiteralPath $script:InstalledMarker -Encoding UTF8

    Write-Host ""
    Write-Host "  ============================================================" -ForegroundColor Green
    Write-Host "     ГОТОВО! Теперь запустите: 2_ЗАПУСТИТЬ_AISingers.bat" -ForegroundColor Green
    Write-Host "  ============================================================" -ForegroundColor Green
    Write-Host ""
}
catch {
    Write-Host ""
    Write-Host "  ОШИБКА УСТАНОВКИ" -ForegroundColor Red
    Write-Host "  $($_.Exception.Message)" -ForegroundColor Red
    Write-Host ""
    Write-Host "  Запустите 4_ДИАГНОСТИКА_AISingers.bat и сохраните показанный отчёт." -ForegroundColor Yellow
    exit 1
}
