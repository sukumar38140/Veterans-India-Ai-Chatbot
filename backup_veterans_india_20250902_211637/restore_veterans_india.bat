@echo off
echo Restoring Veterans India AI Assistant...
echo =======================================

cd /d "D:\VeteransIndia AI Chatbot"

echo Copying Veterans India files back...
copy "backup_veterans_india_20250902_211637\app_veterans_india.py" "app.py"
copy "backup_veterans_india_20250902_211637\llm_config_veterans_india.py" "llm_config.py"
copy "backup_veterans_india_20250902_211637\README_veterans_india.md" "README.md"

echo Veterans India AI Assistant restored successfully!
echo You can now run: streamlit run app.py
pause
