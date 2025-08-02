#!/usr/bin/env python3
"""
Simple runner script for Screen Time Roast Analyzer.
This is the easiest way to run the complete analysis.
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import main

if __name__ == "__main__":
    exit(main())