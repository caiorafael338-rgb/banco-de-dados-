@echo off
cd /d "%~dp0"
where py >nul 2>nul && (set PY=py) || (set PY=python)
echo Usando: %PY%
%PY% -m pip install flask
start "" cmd /c "timeout /t 4 >nul & start http://127.0.0.1:5000"
%PY% app.py
echo.
echo O servidor parou. Leia a mensagem acima.
pause
