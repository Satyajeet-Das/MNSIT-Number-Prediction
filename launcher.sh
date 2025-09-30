#!/bin/bash
# MNIST Digit Predictor Launcher Script

echo "🧠 MNIST Digit Predictor - Project Launcher"
echo "=========================================="
echo ""
echo "Please choose an option:"
echo "1. 🌐 Start Web App (Frontend + Backend)"
echo "2. 📊 Start Streamlit App"
echo "3. 📚 Open Jupyter Notebooks"
echo "4. 🔧 Install All Dependencies"
echo "5. ❌ Exit"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo "Starting Web Application..."
        echo "Backend will start on http://localhost:8000"
        echo "Frontend will start on http://localhost:3000"
        echo ""
        # Start backend in background
        cd api-backend && python -m uvicorn model:app --reload --port 8000 &
        # Start frontend server
        cd ../web-app && python -m http.server 3000
        ;;
    2)
        echo "Starting Streamlit App..."
        cd streamlit-app && streamlit run streamlit_app.py
        ;;
    3)
        echo "Opening Jupyter Notebooks..."
        cd notebooks && jupyter notebook
        ;;
    4)
        echo "Installing all dependencies..."
        pip install -r requirements.txt
        echo "✅ All dependencies installed!"
        ;;
    5)
        echo "Goodbye! 👋"
        exit 0
        ;;
    *)
        echo "Invalid choice. Please run the script again."
        exit 1
        ;;
esac
