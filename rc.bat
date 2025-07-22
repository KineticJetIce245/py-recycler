@echo off
@rem passing the script location, script directory, directory the script is run from, and any additional arguments to the Python script
python %~dp0main.py %~dp0 %CD% %*
