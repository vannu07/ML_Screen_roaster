#!/usr/bin/env python3
"""
Data loading utilities for Screen Time Roast Analyzer.
"""

import pandas as pd
import os
from typing import Optional, Tuple
from utils.config import config
from utils.logger import analysis_logger
from utils.validators import validate_csv_structure


class DataLoader:
    """Handles loading and initial validation of data files."""
    
    def __init__(self, config_instance=None):
        """Initialize data loader with configuration."""
        self.config = config_instance or config
        self.df = None
    
    def load_csv(self, file_path: str, validate: bool = True) -> Optional[pd.DataFrame]:
        """
        Load CSV file with optional validation.
        
        Args:
            file_path: Path to CSV file
            validate: Whether to validate data structure
            
        Returns:
            DataFrame if successful, None otherwise
        """
        analysis_logger.progress(f"Loading data from: {file_path}")
        
        try:
            if validate:
                is_valid, df = validate_csv_structure(file_path)
                if not is_valid:
                    return None
                self.df = df
            else:
                self.df = pd.read_csv(file_path)
            
            analysis_logger.success(f"Loaded data with shape: {self.df.shape}")
            analysis_logger.info(f"Columns: {list(self.df.columns)}")
            
            return self.df
            
        except Exception as e:
            analysis_logger.error(f"Failed to load CSV file: {str(e)}")
            return None
    
    def load_sample_data(self) -> Optional[pd.DataFrame]:
        """
        Load the sample roast data from the data directory.
        
        Returns:
            DataFrame if successful, None otherwise
        """
        sample_file = os.path.join(self.config.data_dir, "sample_roast_data.csv")
        return self.load_csv(sample_file)
    
    def get_data_info(self) -> dict:
        """
        Get comprehensive information about loaded data.
        
        Returns:
            Dictionary with data information
        """
        if self.df is None:
            return {"error": "No data loaded"}
        
        info = {
            "shape": self.df.shape,
            "columns": list(self.df.columns),
            "dtypes": self.df.dtypes.to_dict(),
            "missing_values": self.df.isnull().sum().to_dict(),
            "memory_usage": f"{self.df.memory_usage(deep=True).sum() / 1024:.2f} KB",
            "unique_users": self.df['userId'].nunique() if 'userId' in self.df.columns else 0,
            "date_range": self._get_date_range(),
            "app_distribution": self._get_app_distribution(),
            "intensity_distribution": self._get_intensity_distribution()
        }
        
        return info
    
    def _get_date_range(self) -> dict:
        """Get date range information."""
        if 'date' not in self.df.columns:
            return {"error": "No date column found"}
        
        try:
            dates = pd.to_datetime(self.df['date'])
            return {
                "start_date": dates.min().strftime('%Y-%m-%d'),
                "end_date": dates.max().strftime('%Y-%m-%d'),
                "total_days": (dates.max() - dates.min()).days + 1
            }
        except:
            return {"error": "Invalid date format"}
    
    def _get_app_distribution(self) -> dict:
        """Get app usage distribution."""
        if 'app_name' not in self.df.columns:
            return {"error": "No app_name column found"}
        
        return self.df['app_name'].value_counts().to_dict()
    
    def _get_intensity_distribution(self) -> dict:
        """Get roast intensity distribution."""
        if 'roast_intensity' not in self.df.columns:
            return {"error": "No roast_intensity column found"}
        
        return self.df['roast_intensity'].value_counts().to_dict()
    
    def export_data(self, file_path: str, data: Optional[pd.DataFrame] = None) -> bool:
        """
        Export data to CSV file.
        
        Args:
            file_path: Output file path
            data: DataFrame to export (uses loaded data if None)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            df_to_export = data if data is not None else self.df
            
            if df_to_export is None:
                analysis_logger.error("No data to export")
                return False
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            df_to_export.to_csv(file_path, index=False)
            analysis_logger.success(f"Data exported to: {file_path}")
            return True
            
        except Exception as e:
            analysis_logger.error(f"Failed to export data: {str(e)}")
            return False
    
    def get_sample_users(self, n: int = 5) -> Optional[pd.DataFrame]:
        """
        Get sample users for demonstration.
        
        Args:
            n: Number of sample users to return
            
        Returns:
            DataFrame with sample users
        """
        if self.df is None:
            analysis_logger.error("No data loaded")
            return None
        
        return self.df.head(n)
    
    def filter_by_app(self, app_name: str) -> Optional[pd.DataFrame]:
        """
        Filter data by specific app.
        
        Args:
            app_name: Name of the app to filter by
            
        Returns:
            Filtered DataFrame
        """
        if self.df is None:
            analysis_logger.error("No data loaded")
            return None
        
        if 'app_name' not in self.df.columns:
            analysis_logger.error("No app_name column found")
            return None
        
        filtered_df = self.df[self.df['app_name'] == app_name]
        analysis_logger.info(f"Filtered data for {app_name}: {len(filtered_df)} records")
        
        return filtered_df
    
    def filter_by_intensity(self, intensity: str) -> Optional[pd.DataFrame]:
        """
        Filter data by roast intensity.
        
        Args:
            intensity: Roast intensity to filter by
            
        Returns:
            Filtered DataFrame
        """
        if self.df is None:
            analysis_logger.error("No data loaded")
            return None
        
        if 'roast_intensity' not in self.df.columns:
            analysis_logger.error("No roast_intensity column found")
            return None
        
        filtered_df = self.df[self.df['roast_intensity'] == intensity]
        analysis_logger.info(f"Filtered data for {intensity} intensity: {len(filtered_df)} records")
        
        return filtered_df