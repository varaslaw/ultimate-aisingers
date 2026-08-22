. (Join-Path $PSScriptRoot "common.ps1")

Write-AISingersHeader "ОБНОВЛЕНИЕ"

try {
    $updateRoot = Join-Path $script:RuntimeRoot "update"
    $archivePath = Join-Path $updateRoot "main.zip"
    $extractPath = Join-Path $updateRoot "extracted"

    if (Test-Path -LiteralPath $updateRoot) {
        Remove-Item -LiteralPath $updateRoot -Recurse -Force
    }
    New-Item -ItemType Directory -Path $extractPath -Force | Out-Null

    Write-Step 1 "Загрузка последней версии с GitHub"
    Invoke-WebRequest -UseBasicParsing -Uri "https://github.com/varaslaw/ultimate-aisingers/archive/refs/heads/main.zip" -OutFile $archivePath

    Write-Step 2 "Проверка и распаковка обновления"
    Expand-Archive -LiteralPath $archivePath -DestinationPath $extractPath -Force
    $sourceRoot = Get-ChildItem -LiteralPath $extractPath -Directory | Select-Object -First 1
    if ($null -eq $sourceRoot -or -not (Test-Path -LiteralPath (Join-Path $sourceRoot.FullName "pyproject.toml"))) {
        throw "Полученный архив не похож на AISingers. Обновление остановлено."
    }

    Write-Step 3 "Обновление программы без удаления моделей и результатов"
    $excluded = @(
        ".git",
        ".runtime",
        "uv",
        ".venv",
        "models",
        "audio",
        "temp",
        "config",
        "logs"
    )
    $robocopyArguments = @(
        $sourceRoot.FullName,
        $script:ProjectRoot,
        "/E",
        "/R:2",
        "/W:1",
        "/NFL",
        "/NDL",
        "/NJH",
        "/NJS",
        "/NP",
        "/XD"
    ) + $excluded
    & robocopy.exe @robocopyArguments
    if ($LASTEXITCODE -gt 7) {
        throw "Не удалось скопировать обновление. Код robocopy: $LASTEXITCODE"
    }

    Write-Step 4 "Обновление Python-библиотек"
    & powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "install.ps1")
    if ($LASTEXITCODE -ne 0) {
        throw "Программа обновлена, но зависимости установить не удалось."
    }

    Write-Host ""
    Write-Host "  Обновление завершено. Ваши модели, аудио и настройки сохранены." -ForegroundColor Green
    Write-Host ""
}
catch {
    Write-Host ""
    Write-Host "  ОШИБКА ОБНОВЛЕНИЯ" -ForegroundColor Red
    Write-Host "  $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  Текущая установленная версия не удалена." -ForegroundColor Yellow
    exit 1
}
