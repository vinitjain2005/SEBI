@echo off
setlocal enableextensions enabledelayedexpansion
cd /d %~dp0

where py >nul 2>&1
if errorlevel 1 (
	where python >nul 2>&1 || (
		echo Python not found in PATH. Please install Python 3.10+ and try again.
		pause
		exit /b 1
	)
)

rem Install dependencies
py -3 -m pip install -r requirements.txt --disable-pip-version-check

rem Launch Streamlit app
py -3 -m streamlit run app.py --server.port 8501 --browser.gatherUsageStats false

endlocal
