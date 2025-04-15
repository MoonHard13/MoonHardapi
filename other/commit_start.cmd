@echo off
setlocal

REM === Set your project folder here ===
set PROJECT_PATH=C:\Users\skranis\Desktop\moonhard

cd /d "%PROJECT_PATH%"

IF NOT EXIST start.sh (
    echo ❌ start.sh not found in %PROJECT_PATH%
    pause
    exit /b
)

echo ✅ Adding start.sh to Git...
git add start.sh

echo ✅ Committing start.sh...
git commit -m "Add start.sh for Render"

echo 🚀 Pushing to GitHub...
git push

echo ✅ Done.
pause
