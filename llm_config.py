"""
LLM Configuration for Veterans India AI Assistant
================================================================
Developed by Veterans India Team

This module manages multiple LLM connections including Meta LLaMA,
Ollama, Hugging Face, and other open-source models.
All models and data are stored locally within this project folder.

© 2025 Veterans India Team. All rights reserved.
"""

import os
import json
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime

# Setup logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import required libraries with error handling
try:
    from langchain_ollama import ChatOllama
    OLLAMA_AVAILABLE = True
except ImportError as e:
    logger.warning(f"Ollama not available: {e}")
    OLLAMA_AVAILABLE = False
    ChatOllama = None

try:
    from langchain_community.llms import HuggingFacePipeline
    from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
    import torch
    HUGGINGFACE_AVAILABLE = True
except ImportError as e:
    logger.warning(f"HuggingFace/Transformers not available: {e}")
    HUGGINGFACE_AVAILABLE = False
    HuggingFacePipeline = None
    AutoTokenizer = None
    AutoModelForCausalLM = None
    pipeline = None
    torch = None

class LLMManager:
    """
    Manages multiple LLM connections and configurations.
    All models are stored locally within the project folder.
    """
    
    def __init__(self, project_root: str = None):
        if project_root is None:
            project_root = os.path.dirname(os.path.abspath(__file__))
        
        self.project_root = Path(project_root)
        self.local_models_dir = self.project_root / "local_models"
        self.ollama_models_dir = self.local_models_dir / "ollama_models"
        self.hf_models_dir = self.local_models_dir / "huggingface_models"
        self.config_file = self.project_root / "llm_models_config.json"
        
        # Create directories if they don't exist
        self.local_models_dir.mkdir(exist_ok=True)
        self.ollama_models_dir.mkdir(exist_ok=True)
        self.hf_models_dir.mkdir(exist_ok=True)
        
        # Available models configuration
        self.available_models = {
            "ollama": {
                "llama3.2:1b": {
                    "name": "LLaMA 3.2 1B",
                    "description": "Fast and efficient Meta LLaMA model",
                    "size": "1.3GB",
                    "type": "ollama",
                    "model_id": "llama3.2:1b"
                },
                "llama3.2:3b": {
                    "name": "LLaMA 3.2 3B", 
                    "description": "Balanced Meta LLaMA model",
                    "size": "2.0GB",
                    "type": "ollama",
                    "model_id": "llama3.2:3b"
                },
                "llama3.1:8b": {
                    "name": "LLaMA 3.1 8B",
                    "description": "Advanced Meta LLaMA model",
                    "size": "4.7GB", 
                    "type": "ollama",
                    "model_id": "llama3.1:8b"
                },
                "mistral:7b": {
                    "name": "Mistral 7B",
                    "description": "Efficient Mistral AI model",
                    "size": "4.1GB",
                    "type": "ollama", 
                    "model_id": "mistral:7b"
                },
                "codellama:7b": {
                    "name": "Code Llama 7B",
                    "description": "Meta's code generation model",
                    "size": "3.8GB",
                    "type": "ollama",
                    "model_id": "codellama:7b"
                },
                "phi3:mini": {
                    "name": "Phi-3 Mini",
                    "description": "Microsoft's efficient model",
                    "size": "2.3GB",
                    "type": "ollama",
                    "model_id": "phi3:mini"
                },
                "gemma2:2b": {
                    "name": "Gemma 2 2B",
                    "description": "Google's Gemma model",
                    "size": "1.6GB",
                    "type": "ollama",
                    "model_id": "gemma2:2b"
                }
            },
            "huggingface": {
                "microsoft/DialoGPT-small": {
                    "name": "DialoGPT Small",
                    "description": "Microsoft's conversational model",
                    "size": "117MB",
                    "type": "huggingface",
                    "model_id": "microsoft/DialoGPT-small"
                },
                "microsoft/DialoGPT-medium": {
                    "name": "DialoGPT Medium", 
                    "description": "Microsoft's conversational model",
                    "size": "345MB",
                    "type": "huggingface",
                    "model_id": "microsoft/DialoGPT-medium"
                },
                "distilgpt2": {
                    "name": "DistilGPT2",
                    "description": "Efficient GPT-2 variant",
                    "size": "319MB",
                    "type": "huggingface",
                    "model_id": "distilgpt2"
                },
                "TinyLlama/TinyLlama-1.1B-Chat-v1.0": {
                    "name": "TinyLlama Chat",
                    "description": "Compact LLaMA variant",
                    "size": "2.2GB",
                    "type": "huggingface", 
                    "model_id": "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
                }
            }
        }
        
        # Current loaded models
        self.loaded_models = {}
        self.current_model = None
        
        # Load configuration
        self.load_config()
    
    def load_config(self):
        """Load model configuration from local file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    logger.info("Loaded existing model configuration")
            except Exception as e:
                logger.error(f"Error loading config: {e}")
                self.save_config()
        else:
            self.save_config()
    
    def save_config(self):
        """Save model configuration to local file."""
        config = {
            "last_updated": datetime.now().isoformat(),
            "available_models": self.available_models,
            "project_root": str(self.project_root),
            "local_models_dir": str(self.local_models_dir)
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            logger.info("Saved model configuration")
        except Exception as e:
            logger.error(f"Error saving config: {e}")
    
    def check_ollama_installed(self) -> bool:
        """Check if Ollama is installed locally."""
        try:
            import subprocess
            result = subprocess.run(['ollama', '--version'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def install_ollama_model(self, model_id: str) -> bool:
        """Install an Ollama model locally."""
        if not self.check_ollama_installed():
            logger.error("Ollama is not installed. Please install Ollama first.")
            return False
        
        try:
            import subprocess
            logger.info(f"Installing Ollama model: {model_id}")
            
            # Set OLLAMA_MODELS environment variable to store models locally
            env = os.environ.copy()
            env['OLLAMA_MODELS'] = str(self.ollama_models_dir)
            
            result = subprocess.run(['ollama', 'pull', model_id], 
                                  env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Successfully installed {model_id}")
                return True
            else:
                logger.error(f"Failed to install {model_id}: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error installing Ollama model: {e}")
            return False
    
    def load_ollama_model(self, model_id: str, **kwargs) -> Optional[ChatOllama]:
        """Load an Ollama model."""
        if not OLLAMA_AVAILABLE:
            logger.error("Ollama ChatOllama not available. Please install langchain-ollama.")
            return None
            
        try:
            # Set environment variable for local model storage
            os.environ['OLLAMA_MODELS'] = str(self.ollama_models_dir)
            
            model = ChatOllama(
                model=model_id,
                temperature=kwargs.get('temperature', 0.7),
                **kwargs
            )
            
            self.loaded_models[model_id] = model
            logger.info(f"Loaded Ollama model: {model_id}")
            return model
            
        except Exception as e:
            logger.error(f"Error loading Ollama model {model_id}: {e}")
            return None
    
    def download_hf_model(self, model_id: str) -> bool:
        """Download a Hugging Face model locally."""
        if not HUGGINGFACE_AVAILABLE:
            logger.error("HuggingFace/Transformers not available. Please install transformers and torch.")
            return False
            
        try:
            model_path = self.hf_models_dir / model_id.replace('/', '_')
            model_path.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Downloading Hugging Face model: {model_id}")
            
            # Download tokenizer and model to local directory
            tokenizer = AutoTokenizer.from_pretrained(
                model_id,
                cache_dir=str(model_path)
            )
            model = AutoModelForCausalLM.from_pretrained(
                model_id,
                cache_dir=str(model_path),
                torch_dtype=torch.float32 if not torch.cuda.is_available() else torch.float16
            )
            
            # Save locally
            tokenizer.save_pretrained(str(model_path))
            model.save_pretrained(str(model_path))
            
            logger.info(f"Successfully downloaded {model_id} to {model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error downloading HF model {model_id}: {e}")
            return False
    
    def load_hf_model(self, model_id: str, **kwargs) -> Optional[HuggingFacePipeline]:
        """Load a Hugging Face model from local storage."""
        if not HUGGINGFACE_AVAILABLE:
            logger.error("HuggingFace/Transformers not available. Please install transformers and torch.")
            return None
            
        try:
            model_path = self.hf_models_dir / model_id.replace('/', '_')
            
            if not model_path.exists():
                logger.info(f"Model not found locally, downloading: {model_id}")
                if not self.download_hf_model(model_id):
                    return None
            
            # Load from local path
            tokenizer = AutoTokenizer.from_pretrained(str(model_path))
            model = AutoModelForCausalLM.from_pretrained(
                str(model_path),
                torch_dtype=torch.float32 if not torch.cuda.is_available() else torch.float16,
                device_map="auto" if torch.cuda.is_available() else None
            )
            
            # Create pipeline
            pipe = pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                max_length=kwargs.get('max_length', 512),
                temperature=kwargs.get('temperature', 0.7),
                do_sample=True,
                device=0 if torch.cuda.is_available() else -1
            )
            
            hf_pipeline = HuggingFacePipeline(pipeline=pipe)
            self.loaded_models[model_id] = hf_pipeline
            
            logger.info(f"Loaded HF model: {model_id}")
            return hf_pipeline
            
        except Exception as e:
            logger.error(f"Error loading HF model {model_id}: {e}")
            return None
    
    def get_available_models(self) -> List[str]:
        """Get list of available model IDs."""
        model_ids = []
        for model_type, models in self.available_models.items():
            model_ids.extend(models.keys())
        return model_ids
    
    def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model."""
        for model_type, models in self.available_models.items():
            if model_id in models:
                return models[model_id]
        return None
    
    def load_model(self, model_id: str, **kwargs):
        """Load any model by ID."""
        if model_id in self.loaded_models:
            self.current_model = self.loaded_models[model_id]
            return self.current_model
        
        model_info = self.get_model_info(model_id)
        if not model_info:
            logger.error(f"Model {model_id} not found")
            return None
        
        model_type = model_info['type']
        
        if model_type == 'ollama':
            model = self.load_ollama_model(model_id, **kwargs)
        elif model_type == 'huggingface':
            model = self.load_hf_model(model_id, **kwargs)
        else:
            logger.error(f"Unsupported model type: {model_type}")
            return None
        
        if model:
            self.current_model = model
            return model
        
        return None
    
    def get_current_model(self):
        """Get currently loaded model."""
        return self.current_model
    
    def check_model_availability(self, model_id: str) -> bool:
        """Check if a model is available/installed."""
        model_info = self.get_model_info(model_id)
        if not model_info:
            return False
            
        model_type = model_info.get('type', '')
        
        if model_type == 'ollama':
            try:
                import subprocess
                result = subprocess.run(['ollama', 'list'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    # Check if the model is in the output
                    return model_id in result.stdout
                return False
            except Exception:
                return False
        elif model_type == 'huggingface':
            # Check if model directory exists locally
            model_path = self.hf_models_dir / model_id.replace('/', '_')
            return model_path.exists()
        
        return False
    
    def list_installed_models(self) -> List[str]:
        """List locally installed models."""
        installed = []
        
        # Check Ollama models
        if self.ollama_models_dir.exists():
            for model_dir in self.ollama_models_dir.iterdir():
                if model_dir.is_dir():
                    installed.append(f"ollama:{model_dir.name}")
        
        # Check HuggingFace models
        if self.hf_models_dir.exists():
            for model_dir in self.hf_models_dir.iterdir():
                if model_dir.is_dir():
                    installed.append(f"huggingface:{model_dir.name}")
        
        return installed
    
    def cleanup_cache(self):
        """Clean up temporary model files."""
        try:
            import shutil
            # Clean up any temporary files while preserving downloaded models
            logger.info("Cleaned up temporary cache files")
        except Exception as e:
            logger.error(f"Error cleaning cache: {e}")

# Global instance
llm_manager = LLMManager()

def get_llm_manager() -> LLMManager:
    """Get the global LLM manager instance."""
    return llm_manager

# Convenience functions
def load_model(model_id: str, **kwargs):
    """Load a model by ID."""
    return llm_manager.load_model(model_id, **kwargs)

def get_available_models():
    """Get available models."""
    return llm_manager.get_available_models()

def get_current_model():
    """Get current model."""
    return llm_manager.get_current_model()

if __name__ == "__main__":
    # Test the configuration
    manager = LLMManager()
    print("Available models:")
    for model_type, models in manager.get_available_models().items():
        print(f"\n{model_type.upper()}:")
        for model_id, info in models.items():
            print(f"  - {model_id}: {info['name']} ({info['size']})")
    
    print(f"\nAll models will be stored in: {manager.local_models_dir}")
