#!/usr/bin/env python3
"""
Configuration management for Screen Time Roast Analyzer.
"""

import os
from typing import Dict, List, Any
from dataclasses import dataclass


@dataclass
class ModelConfig:
    """Configuration for machine learning model."""
    test_size: float = 0.2
    random_state: int = 42
    max_depth: int = 10
    features: List[str] = None
    target: str = 'usage_minutes'
    
    def __post_init__(self):
        if self.features is None:
            self.features = ['roast_intensity', 'app_name', 'day_of_week']


@dataclass
class VisualizationConfig:
    """Configuration for data visualizations."""
    figure_size: tuple = (12, 8)
    style: str = 'seaborn-v0_8'
    color_palette: List[str] = None
    show_plots: bool = True
    
    def __post_init__(self):
        if self.color_palette is None:
            self.color_palette = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']


@dataclass
class RoastConfig:
    """Configuration for roast generation."""
    intensity_instructions: Dict[str, str] = None
    app_contexts: Dict[str, str] = None
    category_focus: Dict[str, str] = None
    hinglish_phrases: List[str] = None
    cultural_references: List[str] = None
    
    def __post_init__(self):
        if self.intensity_instructions is None:
            self.intensity_instructions = {
                'light': "Keep it playful and gentle, like a friendly tease between friends. Use humor that makes them smile rather than cringe.",
                'medium': "Make it witty and clever with a good balance of humor and reality check. Include some sass but keep it entertaining.",
                'brutal': "Go all out with savage humor! Be ruthlessly funny and don't hold back. Make it hilariously harsh but still entertaining."
            }
        
        if self.app_contexts is None:
            self.app_contexts = {
                'Instagram': "their endless scrolling through perfectly curated lives and food photos",
                'TikTok': "their addiction to short-form videos and dance trends",
                'YouTube': "their rabbit hole of random videos and procrastination",
                'Twitter': "their obsession with hot takes and social media drama",
                'Reddit': "their deep dives into random communities and endless comment threads",
                'Facebook': "their endless scrolling through family drama and old friends' updates",
                'Snapchat': "their obsession with streaks and disappearing messages",
                'WhatsApp': "their endless group chat notifications and forwarded messages",
                'LinkedIn': "their professional networking that turned into mindless scrolling"
            }
        
        if self.category_focus is None:
            self.category_focus = {
                'health': "how this screen time is affecting their physical and mental well-being",
                'career': "how this is impacting their productivity and professional goals",
                'social_life': "how this is affecting their real-world relationships and social skills",
                'finance': "the opportunity cost and how they could be making money instead",
                'laziness': "their procrastination habits and avoidance of responsibilities",
                'productivity': "how this is killing their focus and getting things done",
                'relationships': "how this is affecting their personal relationships",
                'fitness': "how this sedentary behavior is impacting their physical fitness",
                'sleep': "how late-night scrolling is ruining their sleep schedule",
                'None': "their general screen time habits and digital lifestyle"
            }
        
        if self.hinglish_phrases is None:
            self.hinglish_phrases = [
                "Yaar", "Bhai", "Arre", "Kya baat hai", "Sach mein", "Bilkul", 
                "Bas kar", "Chill maar", "Tension mat le", "Paisa vasool",
                "Time pass", "Bindaas", "Jugaad", "Funda", "Scene", "Vibe"
            ]
        
        if self.cultural_references is None:
            self.cultural_references = [
                "Sharma ji ka beta", "Ghar wale", "Padosi", "Relatives", 
                "College friends", "Office colleagues", "Gym jaana", 
                "Cooking skills", "Traffic", "Metro", "Rickshaw"
            ]


@dataclass
class GeminiConfig:
    """Configuration for Gemini API."""
    model_name: str = 'gemini-pro'
    temperature: float = 0.7
    max_tokens: int = 150
    timeout: int = 30
    api_key: str = None
    
    def __post_init__(self):
        if self.api_key is None:
            self.api_key = os.getenv('GEMINI_API_KEY')


@dataclass
class DataConfig:
    """Configuration for data processing."""
    required_columns: List[str] = None
    valid_intensities: List[str] = None
    valid_apps: List[str] = None
    usage_range: tuple = (1, 1440)  # 1 minute to 24 hours
    date_format: str = '%Y-%m-%d'
    
    def __post_init__(self):
        if self.required_columns is None:
            self.required_columns = [
                'userId', 'roast_category_1', 'roast_intensity', 
                'date', 'app_name', 'usage_minutes'
            ]
        
        if self.valid_intensities is None:
            self.valid_intensities = ['light', 'medium', 'brutal']
        
        if self.valid_apps is None:
            self.valid_apps = [
                'Instagram', 'TikTok', 'YouTube', 'Twitter', 'Reddit',
                'Facebook', 'Snapchat', 'WhatsApp', 'LinkedIn'
            ]


class Config:
    """Main configuration class that combines all configurations."""
    
    def __init__(self):
        self.model = ModelConfig()
        self.visualization = VisualizationConfig()
        self.roast = RoastConfig()
        self.gemini = GeminiConfig()
        self.data = DataConfig()
        
        # File paths
        self.data_dir = "data"
        self.models_dir = "models"
        self.logs_dir = "logs"
        self.output_dir = "output"
        
        # Performance thresholds
        self.min_r2_score = 0.5
        self.max_mae_minutes = 60
        self.min_samples = 100
        
        # Output settings
        self.show_progress = True
        self.verbose_logging = True
        self.save_results = False
        self.demo_users = 5
    
    def get_data_path(self, filename: str) -> str:
        """Get full path for data file."""
        return os.path.join(self.data_dir, filename)
    
    def get_model_path(self, filename: str) -> str:
        """Get full path for model file."""
        return os.path.join(self.models_dir, filename)
    
    def validate(self) -> bool:
        """Validate configuration settings."""
        try:
            # Validate model config
            assert 0 < self.model.test_size < 1, "test_size must be between 0 and 1"
            assert self.model.max_depth > 0, "max_depth must be positive"
            assert len(self.model.features) > 0, "features list cannot be empty"
            
            # Validate data config
            assert len(self.data.required_columns) > 0, "required_columns cannot be empty"
            assert len(self.data.valid_intensities) > 0, "valid_intensities cannot be empty"
            
            # Validate roast config
            assert len(self.roast.intensity_instructions) > 0, "intensity_instructions cannot be empty"
            assert len(self.roast.app_contexts) > 0, "app_contexts cannot be empty"
            
            return True
            
        except AssertionError as e:
            print(f"Configuration validation failed: {e}")
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'model': self.model.__dict__,
            'visualization': self.visualization.__dict__,
            'roast': self.roast.__dict__,
            'gemini': self.gemini.__dict__,
            'data': self.data.__dict__
        }
    
    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'Config':
        """Create configuration from dictionary."""
        config = cls()
        
        if 'model' in config_dict:
            for key, value in config_dict['model'].items():
                setattr(config.model, key, value)
        
        if 'visualization' in config_dict:
            for key, value in config_dict['visualization'].items():
                setattr(config.visualization, key, value)
        
        if 'roast' in config_dict:
            for key, value in config_dict['roast'].items():
                setattr(config.roast, key, value)
        
        if 'gemini' in config_dict:
            for key, value in config_dict['gemini'].items():
                setattr(config.gemini, key, value)
        
        if 'data' in config_dict:
            for key, value in config_dict['data'].items():
                setattr(config.data, key, value)
        
        return config


# Global configuration instance
config = Config()