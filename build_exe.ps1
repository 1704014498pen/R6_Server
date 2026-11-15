# Build a single-file Windows exe into dist\R6_Server.exe
# (PyInstaller logs to stderr, so check the exit code instead of ErrorActionPreference=Stop)
Set-Location $PSScriptRoot
python -m PyInstaller --noconfirm --clean --onefile --windowed `
    --name R6_Server --paths src src\r6_server\__main__.py
if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed ($LASTEXITCODE)" }
Write-Host "Built: $PSScriptRoot\dist\R6_Server.exe"
