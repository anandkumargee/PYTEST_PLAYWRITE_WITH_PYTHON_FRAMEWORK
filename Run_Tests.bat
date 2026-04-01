@echo off
SET ENV=%1
SET BROWSER=%2

if "%ENV%"=="" SET ENV=qa
if "%BROWSER%"=="" SET BROWSER=chromium

echo Running tests in %ENV% environment using %BROWSER% browser...

:: Activate virtual environment if it exists
if exist venv\Scripts\activate.bat (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
)

:: Clean up previous result artifacts and reports
echo Cleaning up previous reports...
if exist reports\playwright-artifacts rd /s /q reports\playwright-artifacts
if exist reports\pytest-reports rd /s /q reports\pytest-reports
if exist reports\allure-results rd /s /q reports\allure-results

:: Create new directories
mkdir reports\playwright-artifacts
mkdir reports\pytest-reports
mkdir reports\allure-results

:: Run tests
python -m pytest tests/ --env %ENV% --browser %BROWSER% --alluredir=reports/allure-results --html=reports/pytest-reports/report.html --self-contained-html

:: Handle Allure History and Generate Report
echo Generating Allure report with history...
if exist reports\allure-report\history (
    echo Copying history trends...
    xcopy /E /I /Y reports\allure-report\history reports\allure-results\history
)

call allure generate reports/allure-results --clean -o reports\allure-report

echo.
echo ======================================================
echo Test execution complete.
echo - HTML Report: reports/pytest-reports/report.html
echo - Allure Results: reports/allure-results
echo.
echo Opening Allure report with history...
start allure open reports\allure-report
echo ======================================================
