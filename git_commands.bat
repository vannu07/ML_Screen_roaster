@echo off
echo 🚀 Screen Time Roast Analyzer - Git Setup
echo ==========================================

echo.
echo 📁 Navigating to project directory...
cd /d "d:\PROJECTS\ML_Screen_roaster"

echo.
echo 🔧 Initializing Git repository...
git init

echo.
echo 📋 Checking Git status...
git status

echo.
echo 📦 Adding files to Git...
git add src/
git add tests/
git add scripts/
git add data/sample_roast_data.csv
git add docs/
git add requirements.txt
git add setup.py
git add README.md
git add run.py
git add analyze_top_apps.py
git add PROJECT_STRUCTURE.md
git add TOP_10_APPS_ANALYSIS_REPORT.md
git add GIT_SETUP_GUIDE.md
git add .gitignore

echo.
echo 📊 Checking what's staged...
git status

echo.
echo 💾 Creating initial commit...
git commit -m "🎉 Initial commit: Screen Time Roast Analyzer

✅ Complete ML pipeline for screen time analysis
✅ Intelligent roast generation system  
✅ Top 10 apps focused analysis
✅ Professional modular architecture
✅ Comprehensive testing framework
✅ Production-ready configuration

🚀 Ready for deployment and collaboration"

echo.
echo ✅ Git setup completed!
echo.
echo 🔗 Next steps:
echo 1. Create repository on GitHub: https://github.com/new
echo 2. Repository name: screen-time-roast-analyzer
echo 3. Run these commands (replace YOUR_USERNAME):
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/screen-time-roast-analyzer.git
echo    git branch -M main
echo    git push -u origin main
echo.
pause