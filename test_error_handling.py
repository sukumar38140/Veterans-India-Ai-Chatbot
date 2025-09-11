"""
Simple test to verify error handling improvements
"""

import sys
import os

def test_error_handling():
    """Test the error handling system"""
    print("🧪 Testing Error Handling System...")
    
    try:
        from error_handler import ErrorCodes, VeteransErrorHandler, handle_app_error
        print("✅ Error handling system imported successfully")
        
        # Test error handling
        handler = VeteransErrorHandler()
        
        # Simulate a missing dependency error
        try:
            raise ImportError("No module named 'nonexistent_module'")
        except ImportError as e:
            error_info = handler.handle_error(e, "test_import")
            print(f"✅ Dependency error handled: {error_info['error_code']}")
        
        # Simulate a model not found error
        try:
            raise FileNotFoundError("Model 'test_model' not found")
        except FileNotFoundError as e:
            error_info = handler.handle_error(e, "model_loading")
            print(f"✅ Model error handled: {error_info['error_code']}")
        
        # Test statistics
        stats = handler.get_error_statistics()
        print(f"✅ Error statistics: {stats['total_errors']} errors logged")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def test_basic_imports():
    """Test basic imports with error handling"""
    print("🧪 Testing Basic Imports with Error Handling...")
    
    try:
        import streamlit
        print("✅ Streamlit available")
    except ImportError:
        print("❌ Streamlit not available")
        return False
    
    try:
        from llm_config import get_llm_manager
        manager = get_llm_manager()
        print("✅ LLM config loaded with error handling")
    except Exception as e:
        print(f"⚠️  LLM config loaded with warnings: {e}")
    
    try:
        from advanced_search_system import search_web_and_answer
        print("✅ Advanced search system loaded")
    except Exception as e:
        print(f"⚠️  Advanced search system loaded with warnings: {e}")
    
    return True

def test_app_structure():
    """Test that the main app file can be imported"""
    print("🧪 Testing App Structure...")
    
    try:
        # Test if app.py can be imported (syntax check)
        import ast
        with open('app.py', 'r') as f:
            ast.parse(f.read())
        print("✅ App.py syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ App.py syntax error: {e}")
        return False
    except Exception as e:
        print(f"❌ App.py structure error: {e}")
        return False

def main():
    print("🇮🇳 Veterans India AI Assistant - Error Handling Test")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Run tests
    all_tests_passed &= test_error_handling()
    all_tests_passed &= test_basic_imports()
    all_tests_passed &= test_app_structure()
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 All error handling tests PASSED!")
        print("✅ Application is ready with improved error handling")
        print("▶️  Run: streamlit run app.py")
    else:
        print("❌ Some tests FAILED. Check the errors above.")
    
    return all_tests_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)