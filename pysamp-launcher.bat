@echo off
@setlocal

SETLOCAL ENABLEDELAYEDEXPANSION
(set \n=^
%=DONT REMOVE THIS=%
)

SET PYSAMP_VERSION=1.2.0
SET PYSAMP_EMPTY_GAMEMODE_URL=https://github.com/habecker/PySAMP/releases/download/1.2.0/empty-gamemode.zip
SET PYSAMP_DLL_URL=https://github.com/habecker/PySAMP/releases/download/1.2.0/PySAMP.dll


Rem http://github.com/habecker/PySAMP/releases/latest/download/pySAMP.dll

SET PYTHON_VERSION=3.8.6
SET PYTHON_NAME=Python %PYTHON_VERSION% 32bit
SET PYTHON_DOWNLOAD_URL=https://www.python.org/ftp/python/%PYTHON_VERSION%/python-%PYTHON_VERSION%-embed-win32.zip
SET PYTHON_CHECK="from sys import exit;import platform; print('Found Python %%s (%%s)' %% (platform.python_version(), platform.architecture()[0])); _v = 0 if platform.architecture()[0] == '32bit' and platform.python_version() == '%PYTHON_VERSION%' else 1; exit(_v)"

SET INTERPRETER_PATH=%~dp0interpreter\
SET ARGUMENT=%1

SET CLEAN_INSTALL="false"
SET UPDATE_INSTALL="false"

if "%ARGUMENT%"=="--clean" (
    set CLEAN_INSTALL="true"
    set UPDATE_INSTALL="true"
)


if "%ARGUMENT%"=="--update" (
    set UPDATE_INSTALL="true"
)

echo PySAMP-Launcher %PYSAMP_VERSION% for Python %PYTHON_NAME%

@REM echo Checking for %PYTHON_NAME%

@REM WHERE python.exe >nul 2>&1

@REM if errorlevel 1 (
@REM     goto install-embedded-python
@REM )

@REM python.exe -c %PYTHON_CHECK%


@REM if errorlevel 1 (
@REM     goto install-embedded-python
@REM )

@REM echo %PYTHON_NAME% was found, it should work as expected
@REM goto check-server

@REM :install-embedded-python

@REM if exist ".\interpreter\" (
@REM     echo %PYTHON_NAME% was not found globally, checking embedded python
@REM     SET "PATH=%INTERPRETER_PATH%;%PATH%"
@REM     python.exe -c %PYTHON_CHECK%
@REM     if errorlevel 1 (
@REM         echo current embedded python is not compatible, reinstalling ...
@REM         del /f /s /q interpreter 1>nul
@REM         rmdir /s /q interpreter
@REM         goto download-embedded-python
@REM     )

@REM     if %CLEAN_INSTALL% == "true" (
@REM         echo removing current embedded interpreter
@REM         del /f /s /q interpreter 1>nul
@REM         rmdir /s /q interpreter
@REM     ) else (
@REM         echo compatible interpreter exists and should work as expected. Use setup.bat --clean for a reinstall
@REM         goto check-server
@REM     )
@REM ) else (
@REM     echo %PYTHON_NAME% was not found, installing embedded python
@REM )

@REM :download-embedded-python
@REM mkdir ".\interpreter\"
@REM cmd "(New-Object System.Net.WebClient).DownloadFile('%PYTHON_DOWNLOAD_URL%', '%~dp0\interpreter\embedded.zip')"

@REM cd ".\interpreter\"
@REM cmd Expand-Archive embedded.zip -DestinationPath .\
@REM cd "..\"

:check-server
SET "PATH=%INTERPRETER_PATH%;%PATH%"   

if not exist ".\python\" (
    echo Initializing empty python gamemode
    mkdir ".\python\"
    cd ".\python\"
    cmd "(New-Object System.Net.WebClient).DownloadFile('%PYSAMP_EMPTY_GAMEMODE_URL%', '%~dp0\python\empty-gamemode.zip')"
    cmd Expand-Archive empty-gamemode.zip -DestinationPath .\
    move empty\gamemode.py .\gamemode.py
    move empty\samp.py .\samp.py
    move empty\const.py .\const.py
    del /f /s /q empty-gamemode.zip 1>nul
    del /f /s /q empty 1>nul
    rmdir /s /q empty
    cd "..\"
)

if %UPDATE_INSTALL%=="true" (
    echo Updating samp.py-API
    cd ".\python\"
    cmd "(New-Object System.Net.WebClient).DownloadFile('%PYSAMP_EMPTY_GAMEMODE_URL%', '%~dp0\python\empty-gamemode.zip')"
    cmd Expand-Archive empty-gamemode.zip -DestinationPath .\
    move /Y empty\samp.py .\samp.py
    del /f /s /q empty-gamemode.zip 1>nul
    del /f /s /q empty 1>nul
    rmdir /s /q empty
    cd "..\"
)

if not exist ".\plugins\" (
    mkdir ".\plugins\"
)

set result="false"
if not exist ".\plugins\PySAMP.dll" set result="true"
if %UPDATE_INSTALL%=="true" set result="true"
if %result% == "true" (
    echo Installing PySAMP.dll
    cmd "(New-Object System.Net.WebClient).DownloadFile('%PYSAMP_DLL_URL%', '%~dp0\plugins\PySAMP.dll')"
)
echo Updating server.cfg
python.exe -c "exec('import random, string; cfg_path=\'server.cfg\'; updated_config = \'\'; added_plugin = False;\nf = open(cfg_path)\nchanged = False\n\nfor line in f:\n    if line.lstrip()[0] == \'#\':\n        continue\n    line = line.rstrip(\' \\r\\n\'); k,v = line.split(\' \', 1)\n    if k == \'plugins\' and \'PySAMP.dll\' not in v:\n        added_plugin = True\n        v += \' PySAMP.dll\'\n        changed = True\n    elif k == \'plugins\' and \'PySAMP.dll\' in v:\n        added_plugin = True\n    if k == \'rcon_password\' and v == \'changeme\':\n        print(\'Changed default password\')\n        changed = True\n        v = \'\'.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))\n    updated_config += \'%%s %%s\\n\' %% (k, v)\nif not added_plugin:\n    updated_config += \'plugins PySAMP.dll\\n\'\n    changed = True\nf.close()\n\nif changed:\n    f = open(cfg_path, \'w\')\n    f.write(updated_config)\n    f.close()\n')"
:start-server
samp-server.exe
@endlocal
