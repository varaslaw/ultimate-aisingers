. (Join-Path $PSScriptRoot "common.ps1")

Write-AISingersHeader "ЗАПУСК"

try {
    if (-not (Test-AISingersInstalled)) {
        Write-Host "  AISingers ещё не установлен. Сейчас автоматически откроется установка." -ForegroundColor Yellow
        & powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot "install.ps1")
        if ($LASTEXITCODE -ne 0 -or -not (Test-AISingersInstalled)) {
            throw "Автоматическая установка не завершена."
        }
        Write-AISingersHeader "ЗАПУСК"
    }

    $port = 7860
    $activePorts = @(
        [System.Net.NetworkInformation.IPGlobalProperties]::GetIPGlobalProperties().GetActiveTcpListeners() |
            Select-Object -ExpandProperty Port
    )
    while ($activePorts -contains $port -and $port -lt 7870) {
        $port++
    }
    if ($activePorts -contains $port) {
        throw "Не найден свободный порт от 7860 до 7870. Закройте другие веб-приложения и повторите запуск."
    }

    $url = "http://127.0.0.1:$port"
    Write-Host "  Интерфейс: $url" -ForegroundColor Cyan
    Write-Host "  Браузер откроется автоматически после загрузки." -ForegroundColor Gray
    Write-Host "  Для остановки AISingers закройте это окно или нажмите Ctrl+C." -ForegroundColor Yellow
    Write-Host ""

    $browserCommand = "Start-Sleep -Seconds 8; Start-Process '$url'"
    Start-Process -FilePath "powershell.exe" -ArgumentList "-NoLogo", "-NoProfile", "-Command", $browserCommand -WindowStyle Hidden | Out-Null

    Invoke-CheckedCommand $script:UvExe "run" "--no-sync" "python" "./src/ultimate_rvc/web/main.py" "--listen-port" "$port"
}
catch {
    Write-Host ""
    Write-Host "  ОШИБКА ЗАПУСКА" -ForegroundColor Red
    Write-Host "  $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "  Запустите 4_ДИАГНОСТИКА_AISingers.bat." -ForegroundColor Yellow
    exit 1
}
