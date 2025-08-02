"""
Screen Time Roast Analyzer - Source Package
A machine learning-powered system for analyzing screen time and generating personalized roasts.
"""

__version__ = "1.0.0"
__author__ = "Screen Time Roast Analyzer Team"

from .data_processor import DataProcessor
from .model_trainer import ModelTrainer
from .prompt_generator import generate_roast_prompt
from .simulation import ScreenTimeSimulator

__all__ = [
    'DataProcessor',
    'ModelTrainer', 
    'generate_roast_prompt',
    'ScreenTimeSimulator'
]