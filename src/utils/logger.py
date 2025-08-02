#!/usr/bin/env python3
"""
Logging utilities for Screen Time Roast Analyzer.
"""

import logging
import os
from datetime import datetime
from typing import Optional


def setup_logger(
    name: str = "screen_roast_analyzer",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    console_output: bool = True
) -> logging.Logger:
    """
    Set up a logger with both file and console handlers.
    
    Args:
        name: Logger name
        level: Logging level
        log_file: Path to log file (optional)
        console_output: Whether to output to console
        
    Returns:
        Configured logger instance
    """
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        # Create logs directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_default_log_file() -> str:
    """Get default log file path with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"logs/screen_roast_analyzer_{timestamp}.log"


class AnalysisLogger:
    """Custom logger for analysis steps."""
    
    def __init__(self, name: str = "analysis"):
        self.logger = setup_logger(name)
    
    def step(self, step_number: int, title: str, width: int = 60):
        """Log a major analysis step."""
        separator = "=" * width
        self.logger.info(f"\n{separator}")
        self.logger.info(f"STEP {step_number}: {title}")
        self.logger.info(f"{separator}")
    
    def section(self, title: str, width: int = 50):
        """Log a section within a step."""
        separator = "-" * width
        self.logger.info(f"\n{separator}")
        self.logger.info(f"{title}")
        self.logger.info(f"{separator}")
    
    def success(self, message: str):
        """Log a success message."""
        self.logger.info(f"✅ {message}")
    
    def warning(self, message: str):
        """Log a warning message."""
        self.logger.warning(f"⚠️ {message}")
    
    def error(self, message: str):
        """Log an error message."""
        self.logger.error(f"❌ {message}")
    
    def info(self, message: str):
        """Log an info message."""
        self.logger.info(f"ℹ️ {message}")
    
    def metric(self, name: str, value: any):
        """Log a metric."""
        self.logger.info(f"📊 {name}: {value}")
    
    def progress(self, message: str):
        """Log a progress message."""
        self.logger.info(f"🔄 {message}")


# Global logger instance
analysis_logger = AnalysisLogger()