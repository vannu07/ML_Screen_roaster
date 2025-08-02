#!/usr/bin/env python3
"""
Data processing and feature engineering for Screen Time Roast Analyzer.
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple, List
from utils.config import config
from utils.logger import analysis_logger


class DataProcessor:
    """Handles data cleaning, preprocessing, and feature engineering."""
    
    def __init__(self, config_instance=None):
        """Initialize data processor with configuration."""
        self.config = config_instance or config
        self.df = None
        self.processed_df = None
    
    def process_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Complete data processing pipeline.
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Processed DataFrame
        """
        analysis_logger.step(1, "DATA PROCESSING AND CLEANING")
        
        self.df = df.copy()
        
        # Data cleaning
        self._clean_data()
        
        # Feature engineering
        self._engineer_features()
        
        # Data validation
        self._validate_processed_data()
        
        self.processed_df = self.df
        analysis_logger.success("Data processing completed successfully")
        
        return self.processed_df
    
    def _clean_data(self) -> None:
        """Clean the data by handling missing values and data types."""
        analysis_logger.section("Data Cleaning")
        
        # Log initial missing values
        missing_before = self.df.isnull().sum()
        analysis_logger.info(f"Missing values before cleaning:\n{missing_before}")
        
        # Handle missing values in roast_category_2
        if 'roast_category_2' in self.df.columns:
            missing_count = self.df['roast_category_2'].isnull().sum()
            self.df['roast_category_2'] = self.df['roast_category_2'].fillna('None')
            analysis_logger.success(f"Filled {missing_count} missing values in 'roast_category_2' with 'None'")
        
        # Convert date column to datetime
        if 'date' in self.df.columns:
            try:
                self.df['date'] = pd.to_datetime(self.df['date'])
                analysis_logger.success("Converted 'date' column to datetime format")
            except Exception as e:
                analysis_logger.error(f"Failed to convert date column: {str(e)}")
        
        # Clean string columns
        string_columns = ['userId', 'app_name', 'roast_category_1', 'roast_category_2', 'roast_intensity']
        for col in string_columns:
            if col in self.df.columns:
                self.df[col] = self.df[col].astype(str).str.strip()
        
        # Handle outliers in usage_minutes
        if 'usage_minutes' in self.df.columns:
            self._handle_usage_outliers()
        
        # Log final missing values
        missing_after = self.df.isnull().sum()
        analysis_logger.info(f"Missing values after cleaning:\n{missing_after}")
    
    def _handle_usage_outliers(self) -> None:
        """Handle outliers in usage_minutes column."""
        usage_col = self.df['usage_minutes']
        
        # Calculate quartiles and IQR
        Q1 = usage_col.quantile(0.25)
        Q3 = usage_col.quantile(0.75)
        IQR = Q3 - Q1
        
        # Define outlier bounds
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # Count outliers
        outliers = self.df[(usage_col < lower_bound) | (usage_col > upper_bound)]
        
        if len(outliers) > 0:
            analysis_logger.warning(f"Found {len(outliers)} outliers in usage_minutes")
            
            # Cap outliers instead of removing them
            self.df.loc[usage_col < lower_bound, 'usage_minutes'] = lower_bound
            self.df.loc[usage_col > upper_bound, 'usage_minutes'] = upper_bound
            
            analysis_logger.info(f"Capped outliers to range [{lower_bound:.1f}, {upper_bound:.1f}]")
    
    def _engineer_features(self) -> None:
        """Create new features from existing data."""
        analysis_logger.section("Feature Engineering")
        
        # Create day_of_week from date
        if 'date' in self.df.columns:
            self.df['day_of_week'] = self.df['date'].dt.day_name()
            analysis_logger.success("Created 'day_of_week' column from date")
        
        # Create usage categories
        if 'usage_minutes' in self.df.columns:
            self.df['usage_category'] = pd.cut(
                self.df['usage_minutes'],
                bins=[0, 30, 120, 300, float('inf')],
                labels=['Light', 'Moderate', 'Heavy', 'Extreme'],
                include_lowest=True
            )
            analysis_logger.success("Created 'usage_category' column")
        
        # Create time-based features
        if 'date' in self.df.columns:
            self.df['month'] = self.df['date'].dt.month
            self.df['day_of_month'] = self.df['date'].dt.day
            self.df['is_weekend'] = self.df['date'].dt.dayofweek.isin([5, 6])
            analysis_logger.success("Created time-based features")
        
        # Create user engagement score
        if 'usage_minutes' in self.df.columns and 'roast_intensity' in self.df.columns:
            intensity_weights = {'light': 1, 'medium': 2, 'brutal': 3}
            self.df['engagement_score'] = (
                self.df['usage_minutes'] * 
                self.df['roast_intensity'].map(intensity_weights).fillna(1)
            )
            analysis_logger.success("Created 'engagement_score' feature")
    
    def _validate_processed_data(self) -> None:
        """Validate the processed data."""
        analysis_logger.section("Data Validation")
        
        # Check for any remaining critical missing values
        critical_columns = ['userId', 'app_name', 'usage_minutes', 'roast_intensity']
        for col in critical_columns:
            if col in self.df.columns:
                missing_count = self.df[col].isnull().sum()
                if missing_count > 0:
                    analysis_logger.error(f"Critical column '{col}' has {missing_count} missing values")
                else:
                    analysis_logger.success(f"Column '{col}' has no missing values")
        
        # Validate data ranges
        if 'usage_minutes' in self.df.columns:
            min_usage = self.df['usage_minutes'].min()
            max_usage = self.df['usage_minutes'].max()
            analysis_logger.info(f"Usage minutes range: {min_usage:.1f} - {max_usage:.1f}")
        
        # Final data shape
        analysis_logger.success(f"Final processed data shape: {self.df.shape}")
    
    def get_feature_summary(self) -> dict:
        """
        Get summary of all features in the processed data.
        
        Returns:
            Dictionary with feature summaries
        """
        if self.processed_df is None:
            return {"error": "No processed data available"}
        
        summary = {}
        
        for col in self.processed_df.columns:
            if self.processed_df[col].dtype in ['object', 'category']:
                # Categorical features
                summary[col] = {
                    'type': 'categorical',
                    'unique_values': self.processed_df[col].nunique(),
                    'top_values': self.processed_df[col].value_counts().head().to_dict(),
                    'missing_count': self.processed_df[col].isnull().sum()
                }
            elif pd.api.types.is_numeric_dtype(self.processed_df[col]):
                # Numerical features
                summary[col] = {
                    'type': 'numerical',
                    'mean': self.processed_df[col].mean(),
                    'std': self.processed_df[col].std(),
                    'min': self.processed_df[col].min(),
                    'max': self.processed_df[col].max(),
                    'missing_count': self.processed_df[col].isnull().sum()
                }
            else:
                # Other types (datetime, etc.)
                summary[col] = {
                    'type': str(self.processed_df[col].dtype),
                    'unique_values': self.processed_df[col].nunique(),
                    'missing_count': self.processed_df[col].isnull().sum()
                }
        
        return summary
    
    def get_data_insights(self) -> dict:
        """
        Generate insights from the processed data.
        
        Returns:
            Dictionary with data insights
        """
        if self.processed_df is None:
            return {"error": "No processed data available"}
        
        insights = {}
        
        # Basic statistics
        insights['total_records'] = len(self.processed_df)
        insights['unique_users'] = self.processed_df['userId'].nunique() if 'userId' in self.processed_df.columns else 0
        
        # App usage insights
        if 'app_name' in self.processed_df.columns and 'usage_minutes' in self.processed_df.columns:
            app_stats = self.processed_df.groupby('app_name')['usage_minutes'].agg(['count', 'mean', 'sum']).round(2)
            insights['top_apps_by_usage'] = app_stats.sort_values('sum', ascending=False).to_dict('index')
            insights['top_apps_by_sessions'] = app_stats.sort_values('count', ascending=False).to_dict('index')
        
        # Intensity distribution
        if 'roast_intensity' in self.processed_df.columns:
            intensity_dist = self.processed_df['roast_intensity'].value_counts()
            insights['intensity_distribution'] = intensity_dist.to_dict()
            insights['intensity_percentages'] = (intensity_dist / len(self.processed_df) * 100).round(2).to_dict()
        
        # Time-based insights
        if 'day_of_week' in self.processed_df.columns:
            day_usage = self.processed_df.groupby('day_of_week')['usage_minutes'].mean().round(2)
            insights['average_usage_by_day'] = day_usage.to_dict()
            insights['most_active_day'] = day_usage.idxmax()
        
        # Usage patterns
        if 'usage_category' in self.processed_df.columns:
            usage_dist = self.processed_df['usage_category'].value_counts()
            insights['usage_patterns'] = usage_dist.to_dict()
        
        return insights
    
    def prepare_modeling_features(self) -> Tuple[pd.DataFrame, pd.Series]:
        """
        Prepare features for machine learning modeling.
        
        Returns:
            Tuple of (features DataFrame, target Series)
        """
        if self.processed_df is None:
            raise ValueError("No processed data available. Run process_data() first.")
        
        # Select features for modeling
        feature_columns = self.config.model.features
        target_column = self.config.model.target
        
        # Check if all required columns exist
        missing_features = [col for col in feature_columns if col not in self.processed_df.columns]
        if missing_features:
            raise ValueError(f"Missing feature columns: {missing_features}")
        
        if target_column not in self.processed_df.columns:
            raise ValueError(f"Missing target column: {target_column}")
        
        X = self.processed_df[feature_columns].copy()
        y = self.processed_df[target_column].copy()
        
        analysis_logger.success(f"Prepared features: {feature_columns}")
        analysis_logger.success(f"Target variable: {target_column}")
        analysis_logger.info(f"Feature matrix shape: {X.shape}")
        analysis_logger.info(f"Target vector shape: {y.shape}")
        
        return X, y