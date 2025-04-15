@echo off
echo -----------------------------------
echo  Step 1: Running Flake8 linter...
echo -----------------------------------
py -m flake8 . --format=html --htmldir=flake8-report
IF %ERRORLEVEL% NEQ 0 (
    echo  Flake8 found issues. Check flake8-report/index.html
    echo Proceeding with tests anyway...
) ELSE (
    echo  Code style passed!
)

echo -----------------------------------
echo  Step 2: Running Pytest tests (test_game.py only)...
echo -----------------------------------
py -m pytest test_game.py --tb=short
IF %ERRORLEVEL% NEQ 0 (
    echo  Some tests failed.
    exit /b %ERRORLEVEL%
)
echo  All tests passed!

echo -----------------------------------
echo  CI pipeline completed successfully!
pause
