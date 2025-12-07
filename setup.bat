@echo off
echo Setting up Health Monitoring System...

echo.
echo 1. Setting up Backend...
cd backend

echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate

echo Installing Python dependencies...
pip install -r requirements.txt

echo Setting up database...
python setup_db.py

echo Creating admin user...
python create_admin.py

echo.
echo 2. Setting up Frontend...
cd ..\frontend

echo Installing Node.js dependencies...
npm install

echo.
echo Setup complete!
echo.
echo To start the system:
echo 1. Backend: cd backend && venv\Scripts\activate && python main.py
echo 2. Frontend: cd frontend && npm start
echo 3. Admin login: username=admin, password=admin123
echo.
pause