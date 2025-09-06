"""
Project Cleanup Script - Veterans India AI Assistant
====================================================
This script removes unnecessary files and keeps only essential ones for optimal performance.
"""

import os
import shutil
from pathlib import Path

class ProjectCleaner:
    def __init__(self, project_root="d:\\VeteransIndia AI Chatbot"):
        self.project_root = Path(project_root)
        
        # Essential files to KEEP
        self.essential_files = {
            'app.py',                          # Main application
            'llm_config.py',                   # LLM configuration
            'run_app.py',                      # Startup script
            'requirements.txt',                # Dependencies
            'README.md',                       # Documentation
            'setup_models.py',                 # Model setup
            'advanced_search_system.py',       # Web search
            'veterans_india_profile.py',       # Company profile
            'VETERANS_INDIA_COMPLETE_PROFILE.md',  # Company info
            'PROJECT_STATUS_COMPLETE.md',      # Status report
            'test_app_functionality.py'       # Core functionality test
        }
        
        # Essential directories to KEEP
        self.essential_dirs = {
            'local_models',     # Local AI models
            'training_data',    # Training data
            '__pycache__'       # Python cache (auto-regenerated)
        }
        
        # Files to REMOVE (test files, backups, duplicates)
        self.files_to_remove = {
            'app_simple.py',                   # Duplicate/simplified version
            'llm_config_backup.py',            # Backup file
            'llm_config_fresh.py',             # Duplicate config
            'llm_config_simple.py',            # Simplified version
            'llm_config_test.py',              # Test version
            'llm_config_working.py',           # Backup version
            'debug_model.py',                  # Debug script
            'fresh_llm_test.py',               # Test script
            'install_models.py',               # Duplicate of setup_models.py
            'test_direct_ollama.py',           # Individual test
            'test_end_to_end.py',              # Individual test
            'test_fresh_config.py',            # Individual test
            'test_import.py',                  # Individual test
            'test_models.py',                  # Individual test
            'test_new_llm_config.py',          # Individual test
            'test_prompt.py',                  # Individual test
            'test_reload_llm.py',              # Individual test
            'test_updated_llm.py',             # Individual test
            'test_web_search_integration.py',  # Individual test
            'auto_training_system.py',         # Not needed for basic operation
            'few_shot_training.py',            # Training script
            'final_validation.py',             # Validation script
            'training_data.py',                # Training utilities
            'integration_summary.py',          # Summary file
            'WEB_SEARCH_INTEGRATION_SUMMARY.py', # Summary file
            'company_profile.py',              # Duplicate of veterans_india_profile.py
            'venue_search_help.py',            # Specialized helper
            'scraper.py',                      # Web scraper utility
            'CLEANUP_PLAN.txt',                # Planning document
            'LLM_KNOWLEDGE_INTEGRATION_SUMMARY.md', # Summary document
            'PERFORMANCE_OPTIMIZATION_SUMMARY.md',  # Summary document
            'requirements_minimal.txt',        # Duplicate requirements
            'llm_models_config.json',          # Config file (data in llm_config.py)
            'analyze_persistence.py'           # Analysis script
        }
        
        # Directories to REMOVE
        self.dirs_to_remove = {
            'llms',          # Contains cache and temporary files
            'models'         # Duplicate of local_models
        }

    def analyze_file_sizes(self):
        """Analyze file sizes to identify large unnecessary files"""
        print("📊 Analyzing file sizes...")
        file_sizes = []
        
        for file_path in self.project_root.rglob('*'):
            if file_path.is_file():
                try:
                    size = file_path.stat().st_size
                    file_sizes.append((file_path, size))
                except:
                    continue
        
        # Sort by size descending
        file_sizes.sort(key=lambda x: x[1], reverse=True)
        
        print("\n🔍 Largest files:")
        for file_path, size in file_sizes[:10]:
            size_mb = size / (1024 * 1024)
            relative_path = file_path.relative_to(self.project_root)
            print(f"  {size_mb:.2f} MB - {relative_path}")
    
    def clean_unnecessary_files(self):
        """Remove unnecessary files"""
        print("\n🗑️ Removing unnecessary files...")
        removed_count = 0
        
        for filename in self.files_to_remove:
            file_path = self.project_root / filename
            if file_path.exists():
                try:
                    file_path.unlink()
                    print(f"  ✅ Removed: {filename}")
                    removed_count += 1
                except Exception as e:
                    print(f"  ❌ Failed to remove {filename}: {e}")
        
        print(f"\n📁 Removed {removed_count} unnecessary files")
    
    def clean_unnecessary_dirs(self):
        """Remove unnecessary directories"""
        print("\n🗂️ Removing unnecessary directories...")
        removed_count = 0
        
        for dirname in self.dirs_to_remove:
            dir_path = self.project_root / dirname
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                    print(f"  ✅ Removed directory: {dirname}")
                    removed_count += 1
                except Exception as e:
                    print(f"  ❌ Failed to remove {dirname}: {e}")
        
        print(f"\n📂 Removed {removed_count} unnecessary directories")
    
    def clean_cache_files(self):
        """Clean cache and temporary files"""
        print("\n🧹 Cleaning cache files...")
        cache_patterns = ['*.pyc', '*.pyo', '*.pyd', '__pycache__', '.pytest_cache', '.coverage']
        
        for pattern in cache_patterns:
            for file_path in self.project_root.rglob(pattern):
                if file_path.is_file():
                    try:
                        file_path.unlink()
                        print(f"  ✅ Removed cache: {file_path.name}")
                    except:
                        pass
                elif file_path.is_dir() and pattern == '__pycache__':
                    try:
                        shutil.rmtree(file_path)
                        print(f"  ✅ Removed cache dir: {file_path}")
                    except:
                        pass
    
    def optimize_training_data(self):
        """Keep only essential training data files"""
        print("\n📚 Optimizing training data...")
        training_dir = self.project_root / 'training_data'
        
        if training_dir.exists():
            # Remove backup directory
            backup_dir = training_dir / 'backup_20250826_163933'
            if backup_dir.exists():
                try:
                    shutil.rmtree(backup_dir)
                    print("  ✅ Removed training data backup")
                except Exception as e:
                    print(f"  ❌ Failed to remove backup: {e}")
    
    def create_essential_files_list(self):
        """Create a list of essential files for reference"""
        essential_structure = {
            'Core Application': [
                'app.py',
                'run_app.py',
                'llm_config.py'
            ],
            'Configuration': [
                'requirements.txt',
                'setup_models.py'
            ],
            'Business Logic': [
                'advanced_search_system.py',
                'veterans_india_profile.py'
            ],
            'Documentation': [
                'README.md',
                'VETERANS_INDIA_COMPLETE_PROFILE.md',
                'PROJECT_STATUS_COMPLETE.md'
            ],
            'Data Storage': [
                'local_models/',
                'training_data/'
            ],
            'Testing': [
                'test_app_functionality.py'
            ]
        }
        
        with open(self.project_root / 'ESSENTIAL_FILES_STRUCTURE.md', 'w') as f:
            f.write("# Veterans India AI Assistant - Essential Files Structure\n\n")
            f.write("This document lists all essential files kept after cleanup.\n\n")
            
            for category, files in essential_structure.items():
                f.write(f"## {category}\n")
                for file in files:
                    f.write(f"- `{file}`\n")
                f.write("\n")
        
        print("📝 Created essential files structure document")
    
    def run_cleanup(self):
        """Run complete cleanup process"""
        print("🇮🇳 Veterans India AI Assistant - Project Cleanup")
        print("=" * 60)
        
        # Analyze current state
        self.analyze_file_sizes()
        
        # Perform cleanup
        self.clean_unnecessary_files()
        self.clean_unnecessary_dirs()
        self.clean_cache_files()
        self.optimize_training_data()
        
        # Create documentation
        self.create_essential_files_list()
        
        print("\n" + "=" * 60)
        print("🎉 Project cleanup completed!")
        print("✨ Project is now optimized for performance and minimal size")
        
        # Show final structure
        self.show_final_structure()
    
    def show_final_structure(self):
        """Show the final clean project structure"""
        print("\n📁 Final Project Structure:")
        for item in sorted(self.project_root.iterdir()):
            if item.is_file():
                size = item.stat().st_size / 1024  # KB
                print(f"  📄 {item.name} ({size:.1f} KB)")
            elif item.is_dir():
                print(f"  📁 {item.name}/")

if __name__ == "__main__":
    cleaner = ProjectCleaner()
    cleaner.run_cleanup()
