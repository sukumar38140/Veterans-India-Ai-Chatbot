@echo off
echo Generating Demo Data for Veterans India Admin Dashboard...
echo.
echo This will create realistic test data including:
echo - 50 sample users with Indian names
echo - Various subscription plans and statuses
echo - Device registrations
echo - Subscription history
echo - Admin activity logs
echo.
pause
echo.
echo Generating data...
python generate_demo_data.py
echo.
echo Demo data generation complete!
echo You can now run the admin dashboard to see the test data.
echo.
pause
