set-location $PSScriptRoot
. ".\Venv\scripts\activate.ps1"
python .\mill_log_reports.py
start-sleep -seconds 3