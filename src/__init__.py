"""
Screen Time Roast Analyzer Package
A comprehensive ML-powered system for analyzing screen time and generating personalized roasts.
"""

__version__ = "1.0.0"
__author__ = "AI/ML Engineer"
__email__ = "contact@screenroaster.com"

from .data.data_processor import DataProcessor
from .models.predictor import UsagePredictor
from .roast.generator import RoastGenerator
from .utils.config import Config

__all__ = [
    'DataProcessor',
    'UsagePredictor', 
    'RoastGenerator',
    'Config'
]