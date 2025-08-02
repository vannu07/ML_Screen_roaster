#!/usr/bin/env python3
"""
Data validation utilities for Screen Time Roast Analyzer.
"""

import pandas as pd
from typing import List, Tuple, Optional
from datetime import datetime
from .config import config
from .logger import analysis_logger


class DataValidator:
    """Validates data quality and structure."""
    
    def __init__(self, config_instance=None):
        """Initialize validator with configuration."""
        self.config = config_instance or config
        self.errors = []
        self.warnings = []
    
    def validate_dataframe(self, df: pd.DataFrame) -> Tuple[bool, List[str], List[str]]:
        """
        Validate a pandas DataFrame for screen time analysis.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        # Check if DataFrame is empty
        if df.empty:
            self.errors.append("DataFrame is empty")
            return False, self.errors, self.warnings
        
        # Check required columns
        self._validate_columns(df)
        
        # Check data types and values
        self._validate_data_types(df)
        self._validate_data_values(df)
        
        # Check data quality
        self._validate_data_quality(df)
        
        is_valid = len(self.errors) == 0
        return is_valid, self.errors, self.warnings
    
    def _validate_columns(self, df: pd.DataFrame):
        """Validate required columns are present."""
        missing_columns = []
        for col in self.config.data.required_columns:
            if col not in df.columns:
                missing_columns.append(col)
        
        if missing_columns:
            self.errors.append(f"Missing required columns: {missing_columns}")
        
        # Check for unexpected columns
        expected_columns = self.config.data.required_columns + ['roast_category_2', 'fcmToken']
        unexpected_columns = [col for col in df.columns if col not in expected_columns]
        if unexpected_columns:
            self.warnings.append(f"Unexpected columns found: {unexpected_columns}")
    
    def _validate_data_types(self, df: pd.DataFrame):
        """Validate data types of columns."""
        try:
            # Check if userId is string-like
            if 'userId' in df.columns and not df['userId'].dtype == 'object':
                self.warnings.append("userId should be string type")
            
            # Check if usage_minutes is numeric
            if 'usage_minutes' in df.columns:
                if not pd.api.types.is_numeric_dtype(df['usage_minutes']):
                    self.errors.append("usage_minutes must be numeric")
            
            # Check if date can be converted to datetime
            if 'date' in df.columns:
                try:
                    pd.to_datetime(df['date'])
                except:
                    self.errors.append("date column cannot be converted to datetime")
        
        except Exception as e:
            self.errors.append(f"Error validating data types: {str(e)}")
    
    def _validate_data_values(self, df: pd.DataFrame):
        """Validate data values are within expected ranges."""
        
        # Validate roast_intensity values
        if 'roast_intensity' in df.columns:
            invalid_intensities = df[~df['roast_intensity'].isin(self.config.data.valid_intensities)]['roast_intensity'].unique()
            if len(invalid_intensities) > 0:
                self.errors.append(f"Invalid roast_intensity values: {invalid_intensities}")
        
        # Validate usage_minutes range
        if 'usage_minutes' in df.columns:
            min_usage, max_usage = self.config.data.usage_range
            out_of_range = df[(df['usage_minutes'] < min_usage) | (df['usage_minutes'] > max_usage)]
            if len(out_of_range) > 0:
                self.warnings.append(f"Found {len(out_of_range)} records with usage_minutes outside expected range ({min_usage}-{max_usage})")
        
        # Validate app_name values
        if 'app_name' in df.columns:
            unknown_apps = df[~df['app_name'].isin(self.config.data.valid_apps)]['app_name'].unique()
            if len(unknown_apps) > 0:
                self.warnings.append(f"Unknown app names found: {unknown_apps}")
    
    def _validate_data_quality(self, df: pd.DataFrame):
        """Validate overall data quality."""
        
        # Check for duplicate records
        if df.duplicated().sum() > 0:
            self.warnings.append(f"Found {df.duplicated().sum()} duplicate records")
        
        # Check for missing values
        missing_counts = df.isnull().sum()
        critical_missing = missing_counts[missing_counts > 0]
        if len(critical_missing) > 0:
            for col, count in critical_missing.items():
                if col in self.config.data.required_columns:
                    self.errors.append(f"Missing values in required column '{col}': {count}")
                else:
                    self.warnings.append(f"Missing values in column '{col}': {count}")
        
        # Check minimum sample size
        if len(df) < self.config.min_samples:
            self.warnings.append(f"Dataset has only {len(df)} samples, minimum recommended: {self.config.min_samples}")
        
        # Check date range
        if 'date' in df.columns:
            try:
                dates = pd.to_datetime(df['date'])
                date_range = dates.max() - dates.min()
                if date_range.days < 7:
                    self.warnings.append(f"Date range is only {date_range.days} days, consider longer period for better analysis")
            except:
                pass  # Date validation already handled in _validate_data_types
    
    def validate_user_data(self, user_data: pd.Series) -> Tuple[bool, List[str]]:
        """
        Validate a single user record for roast generation.
        
        Args:
            user_data: Series containing user data
            
        Returns:
            Tuple of (is_valid, errors)
        """
        errors = []
        
        required_fields = ['userId', 'app_name', 'roast_intensity', 'roast_category_1']
        for field in required_fields:
            if field not in user_data or pd.isna(user_data[field]):
                errors.append(f"Missing required field: {field}")
        
        # Validate specific values
        if 'roast_intensity' in user_data and user_data['roast_intensity'] not in self.config.data.valid_intensities:
            errors.append(f"Invalid roast_intensity: {user_data['roast_intensity']}")
        
        if 'app_name' in user_data and user_data['app_name'] not in self.config.data.valid_apps:
            errors.append(f"Unknown app_name: {user_data['app_name']}")
        
        return len(errors) == 0, errors
    
    def log_validation_results(self, is_valid: bool, errors: List[str], warnings: List[str]):
        """Log validation results using the analysis logger."""
        if is_valid:
            analysis_logger.success("Data validation passed")
        else:
            analysis_logger.error("Data validation failed")
        
        for error in errors:
            analysis_logger.error(f"Validation Error: {error}")
        
        for warning in warnings:
            analysis_logger.warning(f"Validation Warning: {warning}")


def validate_file_path(file_path: str) -> bool:
    """
    Validate if file path exists and is accessible.
    
    Args:
        file_path: Path to file
        
    Returns:
        True if file is valid, False otherwise
    """
    import os
    
    if not os.path.exists(file_path):
        analysis_logger.error(f"File not found: {file_path}")
        return False
    
    if not os.path.isfile(file_path):
        analysis_logger.error(f"Path is not a file: {file_path}")
        return False
    
    if not os.access(file_path, os.R_OK):
        analysis_logger.error(f"File is not readable: {file_path}")
        return False
    
    return True


def validate_csv_structure(file_path: str) -> Tuple[bool, Optional[pd.DataFrame]]:
    """
    Validate CSV file structure and load if valid.
    
    Args:
        file_path: Path to CSV file
        
    Returns:
        Tuple of (is_valid, dataframe or None)
    """
    if not validate_file_path(file_path):
        return False, None
    
    try:
        df = pd.read_csv(file_path)
        validator = DataValidator()
        is_valid, errors, warnings = validator.validate_dataframe(df)
        validator.log_validation_results(is_valid, errors, warnings)
        
        return is_valid, df if is_valid else None
    
    except Exception as e:
        analysis_logger.error(f"Error reading CSV file: {str(e)}")
        return False, None