@echo off
set /p commitMessage= "Commit messaje: "
ECHO.
ECHO Pushing...
ECHO.
git add -A
git commit -m "%commitMessage%"
git push origin master
ECHO.
pause