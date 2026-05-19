@echo off
title Parquet Reader Standalone Installer
echo ==============================================================
echo  ⚡ Antigravity Parquet View Studio - Standalone Installer ⚡
echo ==============================================================
echo.
echo Registering custom "Parquet Reader" association for current user...
echo.

:: Ensure ParquetReader.exe exists in the dist/ParquetReader folder
if not exist "%~dp0dist\ParquetReader\ParquetReader.exe" (
    echo [ERROR] Compiled ParquetReader.exe was not found in the dist\ParquetReader folder.
    pause
    exit /b
)

:: Register the application under Applications with a friendly name in Windows Registry
reg add "HKCU\Software\Classes\Applications\ParquetReader.exe" /v "FriendlyAppName" /t REG_SZ /d "Parquet Reader" /f >nul
reg add "HKCU\Software\Classes\Applications\ParquetReader.exe\shell\open\command" /ve /t REG_SZ /d "\"%~dp0dist\ParquetReader\ParquetReader.exe\" \"%%1\"" /f >nul
reg add "HKCU\Software\Classes\Applications\ParquetReader.exe\DefaultIcon" /ve /t REG_SZ /d "%~dp0dist\ParquetReader\ParquetReader.exe,0" /f >nul

:: Register .parquet and .pq file extensions to use ParquetReader.exe
reg add "HKCU\Software\Classes\.parquet" /ve /t REG_SZ /d "Antigravity.ParquetViewer" /f >nul
reg add "HKCU\Software\Classes\.pq" /ve /t REG_SZ /d "Antigravity.ParquetViewer" /f >nul

:: Register the Antigravity application launcher mapped to ParquetReader.exe in the dist folder
reg add "HKCU\Software\Classes\Antigravity.ParquetViewer" /ve /t REG_SZ /d "Parquet Document File" /f >nul
reg add "HKCU\Software\Classes\Antigravity.ParquetViewer\shell\open\command" /ve /t REG_SZ /d "\"%~dp0dist\ParquetReader\ParquetReader.exe\" \"%%1\"" /f >nul
reg add "HKCU\Software\Classes\Antigravity.ParquetViewer\DefaultIcon" /ve /t REG_SZ /d "%~dp0dist\ParquetReader\ParquetReader.exe,0" /f >nul

echo.
echo ==============================================================
echo [SUCCESS] Custom "Parquet Reader" has been registered!
echo All .parquet / .pq files will now open with the standalone
echo ParquetReader.exe with absolutely zero terminal flashes.
echo ==============================================================
echo.
pause
