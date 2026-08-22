Set-StrictMode -Version 2.0
$ErrorActionPreference = "Stop"

$script:ProjectRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$script:RuntimeRoot = Join-Path $script:ProjectRoot ".runtime"
$script:RuntimeBin = Join-Path $script:RuntimeRoot "bin"
$script:UvExe = Join-Path $script:RuntimeBin "uv.exe"
$script:PythonRoot = Join-Path $script:RuntimeRoot "python"
$script:PythonBin = Join-Path $script:PythonRoot "bin"
$script:UvRoot = Join-Path $script:ProjectRoot "uv"
$script:VenvRoot = Join-Path $script:UvRoot ".venv"
$script:VenvPython = Join-Path $script:VenvRoot "Scripts\python.exe"
$script:UvCache = Join-Path $script:UvRoot "cache"
$script:InstalledMarker = Join-Path $script:RuntimeRoot "installed.json"

function Initialize-AISingersEnvironment {
    [Console]::InputEncoding = [System.Text.Encoding]::UTF8
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding = [System.Text.Encoding]::UTF8

    $env:UV_UNMANAGED_INSTALL = $script:RuntimeBin
    $env:UV_PYTHON_INSTALL_DIR = $script:PythonRoot
    $env:UV_PYTHON_BIN_DIR = $script:PythonBin
    $env:UV_PYTHON_INSTALL_REGISTRY = "0"
    $env:UV_PYTHON_PREFERENCE = "only-managed"
    $env:UV_CACHE_DIR = $script:UvCache
    $env:UV_PROJECT_ENVIRONMENT = $script:VenvRoot
    $env:VIRTUAL_ENV = $script:VenvRoot
    $env:UV_TOOL_DIR = Join-Path $script:UvRoot "tools"
    $env:UV_TOOL_BIN_DIR = Join-Path $script:UvRoot "tools\bin"
    $env:GRADIO_NODE_PATH = Join-Path $script:VenvRoot "Lib\site-packages\nodejs_wheel\node.exe"
    $env:GRADIO_ANALYTICS_ENABLED = "False"
    $env:URVC_ACCELERATOR = "cuda"
    $env:URVC_CONSOLE_LOG_LEVEL = "WARNING"
    $env:PATH = "$script:RuntimeBin;$script:PythonBin;$env:PATH"
    Set-Location -LiteralPath $script:ProjectRoot
}

function Write-AISingersHeader {
    param([Parameter(Mandatory = $true)][string]$Title)

    Clear-Host
    Write-Host ""
    Write-Host "  ============================================================" -ForegroundColor DarkMagenta
    Write-Host "     AISingers Studio  |  $Title" -ForegroundColor Magenta
    Write-Host "  ============================================================" -ForegroundColor DarkMagenta
    Write-Host ""
}

function Write-Step {
    param(
        [Parameter(Mandatory = $true)][int]$Number,
        [Parameter(Mandatory = $true)][string]$Text
    )

    Write-Host ""
    Write-Host "  [$Number] $Text" -ForegroundColor Cyan
}

function Assert-ProjectRoot {
    $marker = Join-Path $script:ProjectRoot ".aisingers-root"
    $projectFile = Join-Path $script:ProjectRoot "pyproject.toml"
    if (-not (Test-Path -LiteralPath $marker) -or -not (Test-Path -LiteralPath $projectFile)) {
        throw "Не найдена корневая папка AISingers. Не переносите файлы запуска отдельно от проекта."
    }
}

function Test-AISingersInstalled {
    return (
        (Test-Path -LiteralPath $script:UvExe) -and
        (Test-Path -LiteralPath $script:VenvPython)
    )
}

function Get-NvidiaVideoCards {
    try {
        return @(
            Get-CimInstance -ClassName Win32_VideoController |
                Where-Object { $_.Name -match "NVIDIA" } |
                Select-Object -ExpandProperty Name
        )
    }
    catch {
        return @()
    }
}

function Get-FreeSpaceGb {
    $root = [System.IO.Path]::GetPathRoot($script:ProjectRoot).TrimEnd("\")
    try {
        $drive = Get-CimInstance -ClassName Win32_LogicalDisk -Filter "DeviceID='$root'"
        if ($null -ne $drive) {
            return [math]::Round($drive.FreeSpace / 1GB, 1)
        }
    }
    catch {
        return -1
    }
    return -1
}

function Test-VCRuntimeInstalled {
    $paths = @(
        "HKLM:\SOFTWARE\Microsoft\VisualStudio\14.0\VC\Runtimes\x64",
        "HKLM:\SOFTWARE\WOW6432Node\Microsoft\VisualStudio\14.0\VC\Runtimes\x64"
    )
    foreach ($path in $paths) {
        try {
            $runtime = Get-ItemProperty -LiteralPath $path -ErrorAction Stop
            if ($runtime.Installed -eq 1) {
                return $true
            }
        }
        catch {
            continue
        }
    }
    return $false
}

function Invoke-CheckedCommand {
    param(
        [Parameter(Mandatory = $true)][string]$FilePath,
        [Parameter(ValueFromRemainingArguments = $true)][string[]]$Arguments
    )

    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Команда завершилась с ошибкой $LASTEXITCODE`: $FilePath"
    }
}

Initialize-AISingersEnvironment
Assert-ProjectRoot
