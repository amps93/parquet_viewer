@echo off
title Parquet Reader Uninstaller
echo ==============================================================
echo  ⚡ Antigravity Parquet View Studio - Uninstaller ⚡
echo ==============================================================
echo.
echo Removing custom "Parquet Reader" association from Windows Registry...
echo.

:: Remove Registry keys created by register_association.bat
reg delete "HKCU\Software\Classes\Applications\ParquetReader.exe" /f >nul 2>&1
reg delete "HKCU\Software\Classes\Antigravity.ParquetViewer" /f >nul 2>&1
reg delete "HKCU\Software\Classes\.parquet" /f >nul 2>&1
reg delete "HKCU\Software\Classes\.pq" /f >nul 2>&1

echo.
echo ==============================================================
echo [SUCCESS] Parquet Reader file associations have been removed.
echo You can now safely delete the program folder.
echo ==============================================================
echo.
pause
