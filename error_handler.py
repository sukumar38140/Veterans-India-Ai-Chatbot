"""
Error Handling System for Veterans India AI Assistant
====================================================
Provides comprehensive error handling and user-friendly error messages
for common issues that may occur in the application.

© 2025 Veterans India Team. All rights reserved.
"""

import logging
import traceback
from typing import Dict, Any, Optional
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorCodes:
    """Standard error codes for the Veterans India AI Assistant"""
    
    # Dependencies and Installation Errors
    MISSING_DEPENDENCY = "VET_DEP_001"
    OLLAMA_NOT_INSTALLED = "VET_OLL_001" 
    MODEL_NOT_FOUND = "VET_MOD_001"
    CONFIGURATION_ERROR = "VET_CFG_001"
    
    # Runtime Errors
    FUNCTION_INVOCATION_FAILED = "VET_FUN_001"
    WEB_SEARCH_FAILED = "VET_WEB_001"
    FILE_PROCESSING_ERROR = "VET_FILE_001"
    
    # Network and External Service Errors
    NETWORK_CONNECTION_ERROR = "VET_NET_001"
    EXTERNAL_API_ERROR = "VET_API_001"
    
    # User Input Errors
    INVALID_INPUT = "VET_INP_001"
    FILE_TOO_LARGE = "VET_INP_002"
    UNSUPPORTED_FILE_TYPE = "VET_INP_003"

class VeteransErrorHandler:
    """Centralized error handling for the Veterans India AI Assistant"""
    
    def __init__(self):
        self.error_log = []
    
    def handle_error(self, error: Exception, context: str = "Unknown", 
                    error_code: str = None) -> Dict[str, Any]:
        """
        Handle an error and return a user-friendly response
        
        Args:
            error: The exception that occurred
            context: Where the error occurred
            error_code: Optional error code
            
        Returns:
            Dict with error details and user message
        """
        
        error_info = {
            'timestamp': datetime.now().isoformat(),
            'error_type': type(error).__name__,
            'error_message': str(error),
            'context': context,
            'error_code': error_code or self._classify_error(error),
            'user_message': self._get_user_friendly_message(error, context),
            'suggested_actions': self._get_suggested_actions(error, context),
            'technical_details': traceback.format_exc() if logger.level <= logging.DEBUG else None
        }
        
        # Log the error
        logger.error(f"Error in {context}: {error_info['error_code']} - {str(error)}")
        self.error_log.append(error_info)
        
        return error_info
    
    def _classify_error(self, error: Exception) -> str:
        """Classify error and assign appropriate error code"""
        error_type = type(error).__name__
        error_message = str(error).lower()
        
        if "no module named" in error_message:
            return ErrorCodes.MISSING_DEPENDENCY
        elif "ollama" in error_message and "no such file" in error_message:
            return ErrorCodes.OLLAMA_NOT_INSTALLED
        elif "model" in error_message and ("not found" in error_message or "not available" in error_message):
            return ErrorCodes.MODEL_NOT_FOUND
        elif "connection" in error_message or "network" in error_message:
            return ErrorCodes.NETWORK_CONNECTION_ERROR
        elif "timeout" in error_message:
            return ErrorCodes.NETWORK_CONNECTION_ERROR
        elif "file" in error_message and "too large" in error_message:
            return ErrorCodes.FILE_TOO_LARGE
        else:
            return ErrorCodes.FUNCTION_INVOCATION_FAILED
    
    def _get_user_friendly_message(self, error: Exception, context: str) -> str:
        """Get user-friendly error message"""
        error_type = type(error).__name__
        error_message = str(error).lower()
        
        if "no module named" in error_message:
            module_name = str(error).split("'")[1] if "'" in str(error) else "a required module"
            return f"🔧 Missing dependency: {module_name}. Some features may not be available until this is installed."
        
        elif "ollama" in error_message:
            return "🤖 Ollama AI models are not currently available. You can still use other features of the assistant."
        
        elif "model" in error_message and "not found" in error_message:
            return "🔍 The requested AI model is not available. Please try selecting a different model from the sidebar."
        
        elif "connection" in error_message or "network" in error_message:
            return "🌐 Network connection issue. Please check your internet connection and try again."
        
        elif "timeout" in error_message:
            return "⏱️ The operation timed out. Please try again or use a different approach."
        
        elif "file" in error_message and "too large" in error_message:
            return "📁 The file is too large. Please try with a smaller file (maximum 10MB recommended)."
        
        elif context == "web_search":
            return "🔍 Web search is currently unavailable. I can still help with general veteran-related questions using my knowledge base."
        
        elif context == "file_processing":
            return "📄 There was an issue processing your file. Please ensure it's a valid PDF, Word document, or text file."
        
        else:
            return f"❌ An unexpected error occurred in {context}. Please try again or contact support if the issue persists."
    
    def _get_suggested_actions(self, error: Exception, context: str) -> list:
        """Get suggested actions to resolve the error"""
        error_message = str(error).lower()
        
        if "no module named" in error_message:
            module_name = str(error).split("'")[1] if "'" in str(error) else "the missing module"
            return [
                f"Install the missing dependency: pip install {module_name}",
                "Check the requirements.txt file for all dependencies",
                "Contact support if installation issues persist"
            ]
        
        elif "ollama" in error_message:
            return [
                "Install Ollama from https://ollama.com/download",
                "Pull a model: ollama pull llama3.2:1b",
                "Use the setup_models.py script for automatic installation",
                "Try using other AI features that don't require Ollama"
            ]
        
        elif "model" in error_message:
            return [
                "Select a different model from the sidebar",
                "Install the model using: ollama pull <model-name>",
                "Check available models in the configuration"
            ]
        
        elif "connection" in error_message or "timeout" in error_message:
            return [
                "Check your internet connection",
                "Try again in a few moments",
                "Use offline features if available"
            ]
        
        elif context == "file_processing":
            return [
                "Ensure the file is not corrupted",
                "Try with a different file format (PDF, DOCX, TXT)",
                "Reduce file size if it's too large",
                "Check file permissions"
            ]
        
        else:
            return [
                "Try refreshing the page",
                "Check the application logs for more details",
                "Contact support if the issue persists"
            ]
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get statistics about errors that have occurred"""
        if not self.error_log:
            return {"total_errors": 0, "error_types": {}, "most_common": None}
        
        error_types = {}
        for error in self.error_log:
            error_code = error['error_code']
            error_types[error_code] = error_types.get(error_code, 0) + 1
        
        most_common = max(error_types.items(), key=lambda x: x[1]) if error_types else None
        
        return {
            "total_errors": len(self.error_log),
            "error_types": error_types,
            "most_common": most_common,
            "recent_errors": self.error_log[-5:] if len(self.error_log) > 5 else self.error_log
        }

# Global error handler instance
global_error_handler = VeteransErrorHandler()

def handle_app_error(error: Exception, context: str = "Application") -> Dict[str, Any]:
    """Convenience function for handling application errors"""
    return global_error_handler.handle_error(error, context)

def safe_execute(func, *args, context: str = "Function", default_return=None, **kwargs):
    """
    Safely execute a function with error handling
    
    Args:
        func: Function to execute
        *args: Function arguments
        context: Context description for error reporting
        default_return: Value to return if function fails
        **kwargs: Function keyword arguments
        
    Returns:
        Function result or default_return if error occurs
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        error_info = handle_app_error(e, context)
        logger.warning(f"Safe execution failed: {error_info['user_message']}")
        return default_return

def display_error_info(error_info: Dict[str, Any]) -> str:
    """Format error information for display to users"""
    return f"""
**{error_info['user_message']}**

**Error Code:** {error_info['error_code']}  
**Time:** {error_info['timestamp']}

**Suggested Actions:**
{chr(10).join(f"• {action}" for action in error_info['suggested_actions'])}

---
*If you continue to experience issues, please contact the Veterans India support team.*
"""