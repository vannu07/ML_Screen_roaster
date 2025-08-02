#!/usr/bin/env python3
"""
Environment setup script for Screen Time Roast Analyzer.
This script helps set up the development environment and dependencies.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def print_header(title: str):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"{title.center(60)}")
    print(f"{'='*60}")


def print_section(title: str):
    """Print a formatted section."""
    print(f"\n{'-'*50}")
    print(f"{title}")
    print(f"{'-'*50}")


def check_python_version():
    """Check if Python version is compatible."""
    print_section("Checking Python Version")
    
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        return False
    else:
        print("✅ Python version is compatible")
        return True


def check_pip():
    """Check if pip is available."""
    print_section("Checking pip")
    
    try:
        import pip
        print(f"✅ pip is available (version: {pip.__version__})")
        return True
    except ImportError:
        print("❌ pip is not available")
        return False


def install_requirements():
    """Install required packages."""
    print_section("Installing Requirements")
    
    requirements_file = Path(__file__).parent.parent / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    try:
        print("📦 Installing packages from requirements.txt...")
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All packages installed successfully")
            return True
        else:
            print(f"❌ Installation failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing packages: {str(e)}")
        return False


def create_directories():
    """Create necessary directories."""
    print_section("Creating Directories")
    
    base_dir = Path(__file__).parent.parent
    directories = [
        "data",
        "output",
        "logs",
        "models"
    ]
    
    for directory in directories:
        dir_path = base_dir / directory
        try:
            dir_path.mkdir(exist_ok=True)
            print(f"✅ Created/verified directory: {directory}")
        except Exception as e:
            print(f"❌ Failed to create directory {directory}: {str(e)}")
            return False
    
    return True


def check_data_file():
    """Check if sample data file exists."""
    print_section("Checking Data Files")
    
    data_file = Path(__file__).parent.parent / "data" / "sample_roast_data.csv"
    
    if data_file.exists():
        print(f"✅ Sample data file found: {data_file}")
        
        # Check file size
        size_mb = data_file.stat().st_size / (1024 * 1024)
        print(f"   File size: {size_mb:.2f} MB")
        
        return True
    else:
        print(f"❌ Sample data file not found: {data_file}")
        print("   Please ensure the data file is in the correct location")
        return False


def setup_environment_variables():
    """Guide user through environment variable setup."""
    print_section("Environment Variables Setup")
    
    print("🔑 Optional: Set up Gemini API key")
    print("   1. Get API key from: https://makersuite.google.com/app/apikey")
    print("   2. Set environment variable:")
    
    if platform.system() == "Windows":
        print("      Windows: set GEMINI_API_KEY=your_api_key_here")
        print("      PowerShell: $env:GEMINI_API_KEY='your_api_key_here'")
    else:
        print("      Linux/Mac: export GEMINI_API_KEY=your_api_key_here")
    
    print("   3. Or pass it as parameter when running the script")
    print("✅ Environment variables guide provided")


def test_installation():
    """Test if the installation works."""
    print_section("Testing Installation")
    
    try:
        # Test imports
        print("🧪 Testing imports...")
        
        import pandas as pd
        print("✅ pandas imported successfully")
        
        import numpy as np
        print("✅ numpy imported successfully")
        
        import sklearn
        print("✅ scikit-learn imported successfully")
        
        import matplotlib.pyplot as plt
        print("✅ matplotlib imported successfully")
        
        import seaborn as sns
        print("✅ seaborn imported successfully")
        
        # Test project imports
        sys.path.append(str(Path(__file__).parent.parent / "src"))
        
        from utils.config import config
        print("✅ Project configuration imported successfully")
        
        from data.data_loader import DataLoader
        print("✅ Data loader imported successfully")
        
        from models.predictor import UsagePredictor
        print("✅ ML predictor imported successfully")
        
        from roast.generator import RoastGenerator
        print("✅ Roast generator imported successfully")
        
        print("🎉 All imports successful!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False


def display_usage_instructions():
    """Display usage instructions."""
    print_section("Usage Instructions")
    
    print("🚀 How to run the Screen Time Roast Analyzer:")
    print()
    print("1. Basic usage (with sample data):")
    print("   python scripts/run_analysis.py")
    print()
    print("2. With custom data file:")
    print("   python scripts/run_analysis.py --data-file path/to/your/data.csv")
    print()
    print("3. With Gemini API key:")
    print("   python scripts/run_analysis.py --api-key your_api_key")
    print()
    print("4. Save results to file:")
    print("   python scripts/run_analysis.py --save-results")
    print()
    print("5. Full options:")
    print("   python scripts/run_analysis.py --help")
    print()
    print("📚 Alternative: Run the main module directly:")
    print("   python src/main.py")


def main():
    """Main setup function."""
    print_header("SCREEN TIME ROAST ANALYZER - ENVIRONMENT SETUP")
    
    print("🔧 Setting up your development environment...")
    
    success_count = 0
    total_checks = 6
    
    # Run all checks
    if check_python_version():
        success_count += 1
    
    if check_pip():
        success_count += 1
    
    if install_requirements():
        success_count += 1
    
    if create_directories():
        success_count += 1
    
    if check_data_file():
        success_count += 1
    
    if test_installation():
        success_count += 1
    
    # Setup environment variables (always succeeds)
    setup_environment_variables()
    
    # Display results
    print_header("SETUP RESULTS")
    
    print(f"✅ Completed: {success_count}/{total_checks} checks passed")
    
    if success_count == total_checks:
        print("🎉 Environment setup completed successfully!")
        print("🚀 You're ready to run the Screen Time Roast Analyzer!")
        
        display_usage_instructions()
        
        return 0
    else:
        print("⚠️  Some setup steps failed. Please review the errors above.")
        print("💡 You may still be able to run the analyzer with limited functionality.")
        
        return 1


if __name__ == "__main__":
    exit(main())