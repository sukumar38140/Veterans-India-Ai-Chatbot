"""
Veterans India AI Assistant - Quick Start Scripts
===============================================
Easy-to-use batch scripts for running the admin dashboard
and managing the system.

© 2025 Veterans India Team. All rights reserved.
"""

# run_admin_dashboard.bat
@echo off
echo Starting Veterans India Admin Dashboard...
echo.
echo Dashboard will be available at: http://localhost:8502
echo Default admin login: admin / admin123
echo.
streamlit run admin_dashboard.py --server.port 8502
pause
