"""
Veterans India AI Assistant - Startup Script
============================================
Quick startup script to run the application with model checking
"""

import subprocess
import sys
import os
from llm_config import llm_manager

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import streamlit
        import langchain_ollama
        import PyPDF2
        import docx
        print("✅ All Python dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Run: python setup_models.py and choose option 1 to install dependencies")
        return False

def check_ollama():
    """Check if Ollama is running"""
    try:
        result = subprocess.run(["ollama", "list"], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except:
        return False

def check_models():
    """Check available models"""
    print("🤖 Checking available models...")
    
    available_count = 0
    for model_id in llm_manager.get_available_models():
        config = llm_manager.get_model_info(model_id)
        if config:
            # Handle both dict and object access patterns
            model_type = getattr(config, 'model_type', None) or config.get('model_type')
            name = getattr(config, 'name', None) or config.get('name', model_id)
            
            if model_type == "ollama":
                if llm_manager.check_model_availability(model_id):
                    print(f"✅ {name}")
                    available_count += 1
                else:
                    print(f"❌ {name} - Not installed")
    
    if available_count == 0:
        print("⚠️  No models are available!")
        print("Run: python setup_models.py to install models")
        return False
    
    print(f"📊 {available_count} models are ready to use")
    return True

def main():
    print("🇮🇳 Veterans India AI Assistant - Starting Up...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check if Ollama is available
    if not check_ollama():
        print("⚠️  Ollama is not running or not installed")
        print("Please install Ollama from: https://ollama.com/download")
        print("Or start Ollama service if already installed")
    
    # Check models
    check_models()
    
    print("\n🚀 Starting Veterans India AI Assistant...")
    print("Opening in your default web browser...")
    
    try:
        # Run Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    main()
