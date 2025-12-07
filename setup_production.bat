@echo off
echo ========================================
echo Health Monitoring System
echo Production Setup Script
echo ========================================
echo.

echo Step 1: Checking Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Git not found. Install from: https://git-scm.com
    pause
    exit /b 1
)
echo [OK] Git installed

echo.
echo Step 2: Initialize Git Repository...
if not exist .git (
    git init
    echo [OK] Git repository initialized
) else (
    echo [OK] Git repository already exists
)

echo.
echo Step 3: Create .gitignore...
if not exist .gitignore (
    echo [OK] .gitignore created
) else (
    echo [OK] .gitignore already exists
)

echo.
echo Step 4: Commit files...
git add .
git commit -m "Production deployment setup" >nul 2>&1
echo [OK] Files committed

echo.
echo ========================================
echo NEXT STEPS:
echo ========================================
echo.
echo 1. Create GitHub repository
echo    https://github.com/new
echo.
echo 2. Push code:
echo    git remote add origin https://github.com/YOUR_USERNAME/health-monitoring.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Deploy Database (Neon):
echo    https://console.neon.tech
echo.
echo 4. Deploy Backend (Render):
echo    https://dashboard.render.com
echo.
echo 5. Deploy Frontend (Vercel):
echo    https://vercel.com/dashboard
echo.
echo 6. Follow DEPLOYMENT_GUIDE.md for detailed steps
echo.
echo ========================================
pause
