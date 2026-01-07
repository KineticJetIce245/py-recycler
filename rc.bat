@echo off
setlocal

@rem passing the script location, script directory, directory the script is run from, and any additional arguments to the Python script
set "PYTHONPATH=%~dp0/src"
set "SCRIPT_DIR=%~dp0"
set "CUR_DIR=%CD%"
set "ARGS="

:loopstart
if "%~1"=="" goto loopend

@rem fix the trailing backslash due to powershell autocomplete
set "ARG=%~1"
if "%ARG:~-1%"=="\" set "ARG=%ARG%."

@rem Add to ARGS with quotes
set "ARGS=%ARGS% "%ARG%""

shift
goto loopstart

:loopend
py "%SCRIPT_DIR%main.py" "%SCRIPT_DIR%." "%CUR_DIR%" %ARGS%
endlocal
