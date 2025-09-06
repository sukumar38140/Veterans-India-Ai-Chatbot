"""
Test script to verify Veterans India AI Assistant functionality
"""

import sys
import os

def test_imports():
    """Test all critical imports"""
    print("🧪 Testing imports...")
    try:
        import streamlit
        print("✅ Streamlit imported")
        
        from llm_config import get_llm_manager, get_available_models
        print("✅ LLM config imported")
        
        from langchain_ollama import ChatOllama
        print("✅ LangChain Ollama imported")
        
        import PyPDF2
        print("✅ PyPDF2 imported")
        
        import docx
        print("✅ python-docx imported")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_llm_manager():
    """Test LLM manager functionality"""
    print("\n🤖 Testing LLM Manager...")
    try:
        from llm_config import get_llm_manager
        llm_manager = get_llm_manager()
        
        # Test available models
        models = llm_manager.get_available_models()
        print(f"✅ Found {len(models)} available models: {models[:3]}...")
        
        # Test model info
        if models:
            model_info = llm_manager.get_model_info(models[0])
            print(f"✅ Model info retrieved for {models[0]}")
            
            # Test model availability
            available = llm_manager.check_model_availability(models[0])
            print(f"✅ Model availability check: {available}")
            
            # Test model loading
            if available:
                model = llm_manager.load_model(models[0])
                if model:
                    print(f"✅ Model loaded successfully")
                    return True
                else:
                    print(f"❌ Failed to load model")
                    return False
        
        return True
    except Exception as e:
        print(f"❌ LLM Manager error: {e}")
        return False

def test_ollama_connection():
    """Test direct Ollama connection"""
    print("\n🦙 Testing Ollama connection...")
    try:
        import subprocess
        result = subprocess.run(['ollama', 'list'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Ollama is running")
            print(f"Available models:\n{result.stdout}")
            return True
        else:
            print("❌ Ollama not responding")
            return False
    except Exception as e:
        print(f"❌ Ollama test error: {e}")
        return False

def main():
    print("🇮🇳 Veterans India AI Assistant - Functionality Test")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Run tests
    all_tests_passed &= test_imports()
    all_tests_passed &= test_ollama_connection()
    all_tests_passed &= test_llm_manager()
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 All tests PASSED! Application is ready to run.")
        print("▶️  Run: python -m streamlit run app.py")
    else:
        print("❌ Some tests FAILED. Please check the errors above.")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
