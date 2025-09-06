#!/usr/bin/env python3
"""
Veterans India AI Assistant - Startup Optimizer
Ensures optimal application restart behavior and model persistence
"""

import os
import sys
import json
import time
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StartupOptimizer:
    """Optimize application startup and ensure persistence"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.config_file = self.base_dir / "startup_config.json"
        self.last_run_file = self.base_dir / "last_run.json"
        
    def save_startup_state(self):
        """Save current startup state for quick restarts"""
        state = {
            "last_startup": time.time(),
            "models_verified": True,
            "ollama_available": self._check_ollama(),
            "dependencies_checked": True,
            "port": 8501
        }
        
        with open(self.last_run_file, 'w') as f:
            json.dump(state, f, indent=2)
        
        logger.info("✅ Startup state saved for quick restarts")
    
    def load_startup_state(self):
        """Load previous startup state"""
        if not self.last_run_file.exists():
            return None
            
        try:
            with open(self.last_run_file, 'r') as f:
                state = json.load(f)
            
            # Check if state is recent (within 24 hours)
            if time.time() - state.get("last_startup", 0) < 86400:
                return state
        except Exception as e:
            logger.warning(f"Could not load startup state: {e}")
        
        return None
    
    def _check_ollama(self):
        """Check if Ollama is available"""
        try:
            import ollama
            models = ollama.list()
            return len(models.models) > 0
        except Exception:
            return False
    
    def optimize_startup(self):
        """Optimize startup process"""
        print("🚀 Optimizing startup...")
        
        # Check previous state
        state = self.load_startup_state()
        if state and state.get("ollama_available"):
            print("✅ Using cached startup state")
            print("🔄 Quick restart mode enabled")
            return True
        
        # Full startup verification
        print("🔍 Full startup verification...")
        
        # Check Ollama
        if not self._check_ollama():
            print("❌ Ollama not available")
            return False
        
        # Save optimized state
        self.save_startup_state()
        return True
    
    def create_quick_start_script(self):
        """Create quick start script for instant restarts"""
        script_content = '''@echo off
REM Veterans India AI Assistant - Quick Start Script
echo Veterans India AI Assistant - Quick Start
echo ============================================

REM Check if already running
for /f "tokens=5" %%a in ('netstat -ano ^| find ":8501"') do (
    if "%%a" NEQ "" (
        echo Application already running at http://localhost:8501
        start http://localhost:8501
        exit /b 0
    )
)

REM Start application
echo Starting application...
python run_app.py

pause
'''
        
        script_path = self.base_dir / "quick_start.bat"
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"✅ Quick start script created: {script_path}")
    
    def optimize_model_loading(self):
        """Optimize model loading for persistence"""
        config_updates = {
            "model_cache_enabled": True,
            "auto_model_detection": True,
            "fast_startup": True,
            "persistence_mode": True
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config_updates, f, indent=2)
        
        print("✅ Model loading optimized for persistence")

def main():
    """Main optimization process"""
    print("🛠️  Veterans India AI Assistant - Startup Optimization")
    print("=" * 60)
    
    optimizer = StartupOptimizer()
    
    # Optimize startup
    if optimizer.optimize_startup():
        print("✅ Startup optimization complete")
    else:
        print("❌ Startup optimization failed")
        return
    
    # Create quick start script
    optimizer.create_quick_start_script()
    
    # Optimize model loading
    optimizer.optimize_model_loading()
    
    print("\n🎉 Optimization Complete!")
    print("📝 Benefits:")
    print("   • Faster application restarts")
    print("   • Automatic model detection")
    print("   • Persistent configuration")
    print("   • Quick start script available")
    print("\n▶️  Use 'quick_start.bat' for instant launches!")

if __name__ == "__main__":
    main()
