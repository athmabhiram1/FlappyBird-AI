@echo off
echo Starting Flappy Bird AI Auto-Training...
echo ======================================
echo This will start automatic training with default parameters.
echo Press Ctrl+C to stop training at any time.
echo Models will be saved in the 'models' directory.
echo ======================================
echo.
timeout /t 3 /nobreak >nul
python auto_train.py train 200
pause