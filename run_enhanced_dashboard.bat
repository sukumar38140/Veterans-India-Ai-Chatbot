@echo off
echo Starting Enhanced Veterans India Admin Dashboard...
echo.
echo Enhanced Dashboard will be available at: http://localhost:8503
echo Features: Advanced Analytics, Charts, Enhanced UI
echo Default admin login: admin / admin123
echo.
streamlit run admin_dashboard_enhanced.py --server.port 8503
pause
