@echo off
echo 🤖 MetaMind OS - Fast Start
echo =============================

echo 📦 Installing dependencies...
cd backend
pip install fastapi uvicorn[standard] pandas numpy scikit-learn python-multipart python-dotenv

echo 🚀 Starting MetaMind backend...
start "MetaMind Backend" uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

cd ..

echo ✅ MetaMind OS is starting!
echo ================================
echo 🔧 Backend API: http://localhost:8000
echo 📚 API Docs: http://localhost:8000/docs
echo ================================
echo.
echo 📝 Quick Test:
echo 1. Go to http://localhost:8000/docs
echo 2. Upload a CSV file via /upload endpoint
echo 3. Use /generate-complete-project endpoint
echo.
echo ⚡ The system will generate a complete ML application fast!
echo.
pause