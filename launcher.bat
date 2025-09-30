@echo off
REM MNIST Digit Predictor Launcher Script for Windows

echo 🧠 MNIST Digit Predictor - Project Launcher
echo ==========================================
echo.
echo Please choose an option:
echo 1. 🌐 Start Web App (Frontend + Backend)
echo 2. 📊 Start Streamlit App
echo 3. 📚 Open Jupyter Notebooks
echo 4. 🔧 Install All Dependencies
echo 5. ❌ Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo Starting Web Application...
    echo Backend will start on http://localhost:8000
    echo Frontend will start on http://localhost:3000
    echo.
    REM Start backend in new window
    start "API Backend" cmd /k "cd api-backend && python -m uvicorn model:app --reload --port 8000"
    REM Start frontend server
    cd web-app && python -m http.server 3000
) else if "%choice%"=="2" (
    echo Starting Streamlit App...
    cd streamlit-app && streamlit run streamlit_app.py
) else if "%choice%"=="3" (
    echo Opening Jupyter Notebooks...
    cd notebooks && jupyter notebook
) else if "%choice%"=="4" (
    echo Installing all dependencies...
    pip install -r requirements.txt
    echo ✅ All dependencies installed!
    pause
) else if "%choice%"=="5" (
    echo Goodbye! 👋
    exit /b 0
) else (
    echo Invalid choice. Please run the script again.
    pause
    exit /b 1
)
