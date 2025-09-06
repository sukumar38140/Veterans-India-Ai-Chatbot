"""
Setup Script for Veterans India AI Assistant
============================================
This script helps install and configure multiple LLM models
"""

import subprocess
import sys
import os
from typing import List

class ModelSetup:
    def __init__(self):
        self.ollama_models = [
            "llama3.2:1b",
            "llama3.2:3b", 
            "llama3.1:8b",
            "llama2:7b",
            "codellama:7b",
            "mistral:7b",
            "phi3:3.8b",
            "qwen2:7b",
            "gemma:7b"
        ]
    
    def check_ollama_installed(self) -> bool:
        """Check if Ollama is installed"""
        try:
            result = subprocess.run(["ollama", "--version"], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def install_python_dependencies(self):
        """Install Python dependencies"""
        print("📦 Installing Python dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python dependencies installed!")
    
    def pull_ollama_model(self, model_name: str) -> bool:
        """Pull a specific Ollama model"""
        try:
            print(f"🔄 Pulling model: {model_name}")
            result = subprocess.run(["ollama", "pull", model_name], 
                                  capture_output=True, text=True, timeout=1800)  # 30 min timeout
            if result.returncode == 0:
                print(f"✅ Successfully pulled: {model_name}")
                return True
            else:
                print(f"❌ Failed to pull: {model_name}")
                print(f"Error: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print(f"⏰ Timeout pulling: {model_name}")
            return False
        except Exception as e:
            print(f"❌ Error pulling {model_name}: {str(e)}")
            return False
    
    def list_installed_models(self) -> List[str]:
        """List currently installed Ollama models"""
        try:
            result = subprocess.run(["ollama", "list"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')[1:]  # Skip header
                models = []
                for line in lines:
                    if line.strip():
                        model_name = line.split()[0]
                        models.append(model_name)
                return models
            return []
        except:
            return []
    
    def setup_recommended_models(self):
        """Setup recommended models for the AI assistant"""
        if not self.check_ollama_installed():
            print("❌ Ollama is not installed!")
            print("Please install Ollama from: https://ollama.com/download")
            return
        
        print("🤖 Setting up recommended LLM models...")
        
        # Check already installed models
        installed = self.list_installed_models()
        print(f"📋 Currently installed models: {installed}")
        
        # Recommended models in order of priority
        recommended = [
            "llama3.2:1b",    # Fast, small model
            "llama3.2:3b",    # Balanced model
            "mistral:7b",     # Good alternative
            "codellama:7b"    # For coding tasks
        ]
        
        for model in recommended:
            if model not in installed:
                success = self.pull_ollama_model(model)
                if not success:
                    print(f"⚠️  Failed to install {model}, continuing with next...")
            else:
                print(f"✅ {model} already installed")
    
    def setup_all_models(self):
        """Setup all available models (may take very long!)"""
        if not self.check_ollama_installed():
            print("❌ Ollama is not installed!")
            return
        
        print("🤖 Setting up ALL LLM models (this will take a while)...")
        installed = self.list_installed_models()
        
        for model in self.ollama_models:
            if model not in installed:
                self.pull_ollama_model(model)
            else:
                print(f"✅ {model} already installed")
    
    def create_models_directory(self):
        """Create directory for local model files"""
        models_dir = "./models"
        if not os.path.exists(models_dir):
            os.makedirs(models_dir)
            print(f"📁 Created models directory: {models_dir}")
        
        # Create a README for GGUF models
        readme_path = os.path.join(models_dir, "README.md")
        if not os.path.exists(readme_path):
            with open(readme_path, 'w') as f:
                f.write("""# Local Models Directory

This directory is for storing local model files (GGUF format).

## How to add GGUF models:

1. Download GGUF models from HuggingFace
2. Place them in this directory
3. Update the `local_path` in `llm_config.py`

## Popular GGUF models:
- LLaMA 2 7B Chat: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF
- Code Llama 7B: https://huggingface.co/TheBloke/CodeLlama-7B-Instruct-GGUF
- Mistral 7B: https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF

## Usage:
The models will be automatically loaded by the LLM configuration system.
""")
            print("📄 Created models README.md")

def main():
    setup = ModelSetup()
    
    print("🇮🇳 Veterans India AI Assistant - Model Setup")
    print("=" * 50)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Install Python dependencies")
        print("2. Setup recommended models (Fast)")
        print("3. Setup all models (Very slow, requires lots of storage)")
        print("4. List installed models")
        print("5. Create models directory")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            setup.install_python_dependencies()
        elif choice == "2":
            setup.setup_recommended_models()
        elif choice == "3":
            confirm = input("This will download many large models. Continue? (y/N): ")
            if confirm.lower() == 'y':
                setup.setup_all_models()
        elif choice == "4":
            models = setup.list_installed_models()
            print(f"📋 Installed models: {models}")
        elif choice == "5":
            setup.create_models_directory()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
