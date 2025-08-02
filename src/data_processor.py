#!/usr/bin/env python3
"""
Data Processor Module for Screen Time Roast Analyzer
Handles all data loading and preprocessing operations.
"""

import pandas as pd
import numpy as np
import logging
from typing import Tuple, Dict, Any
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Handles data loading, cleaning, and preprocessing."""
    
    def __init__(self):
        """Initialize the DataProcessor."""
        self.processed_data = None
        
    def load_and_prepare_data(self, file_path: str) -> pd.DataFrame:
        """
        Load and prepare data from CSV file.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Clean, prepared DataFrame
        """
        logger.info(f"📊 Loading data from: {file_path}")
        
        try:
            # Load the CSV file
            df = pd.read_csv(file_path)
            logger.info(f"✅ Loaded {len(df)} rows and {len(df.columns)} columns")
            
            # Perform data cleaning
            df_clean = self._clean_data(df)
            
            # Perform feature engineering
            df_processed = self._engineer_features(df_clean)
            
            logger.info(f"✅ Data processing completed. Final shape: {df_processed.shape}")
            self.processed_data = df_processed
            
            return df_processed
            
        except FileNotFoundError:
            logger.error(f"❌ File not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"❌ Error processing data: {str(e)}")
            raise
    
    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the data by handling missing values and data types.
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        logger.info("🧹 Cleaning data...")
        
        df_clean = df.copy()
        
        # Fill missing values
        if 'usage_minutes' in df_clean.columns:
            df_clean.loc[:, 'usage_minutes'] = df_clean['usage_minutes'].fillna(df_clean['usage_minutes'].median())
        
        if 'app_name' in df_clean.columns:
            df_clean.loc[:, 'app_name'] = df_clean['app_name'].fillna('Unknown')
        
        if 'roast_category_1' in df_clean.columns:
            df_clean.loc[:, 'roast_category_1'] = df_clean['roast_category_1'].fillna('productivity')
        
        if 'roast_intensity' in df_clean.columns:
            df_clean.loc[:, 'roast_intensity'] = df_clean['roast_intensity'].fillna('medium')
        
        # Handle any other missing values
        for col in df_clean.columns:
            if df_clean[col].dtype == 'object':
                df_clean.loc[:, col] = df_clean[col].fillna('Unknown')
            else:
                df_clean.loc[:, col] = df_clean[col].fillna(df_clean[col].median())
        
        # Remove duplicates
        initial_rows = len(df_clean)
        df_clean.drop_duplicates(inplace=True)
        removed_duplicates = initial_rows - len(df_clean)
        
        if removed_duplicates > 0:
            logger.info(f"🗑️ Removed {removed_duplicates} duplicate rows")
        
        logger.info(f"✅ Data cleaning completed. Shape: {df_clean.shape}")
        return df_clean
    
    def _engineer_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Engineer new features from existing data.
        
        Args:
            df: Cleaned DataFrame
            
        Returns:
            DataFrame with engineered features
        """
        logger.info("⚙️ Engineering features...")
        
        df_features = df.copy()
        
        # Create day_of_week feature if date information exists
        if 'date' in df_features.columns:
            df_features['date'] = pd.to_datetime(df_features['date'])
            df_features['day_of_week'] = df_features['date'].dt.day_name()
        elif 'day_of_week' not in df_features.columns:
            # If no date column, create random day_of_week for simulation
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            df_features['day_of_week'] = np.random.choice(days, size=len(df_features))
        
        # Create usage categories
        if 'usage_minutes' in df_features.columns:
            df_features['usage_category'] = pd.cut(
                df_features['usage_minutes'],
                bins=[0, 30, 120, 300, float('inf')],
                labels=['Light', 'Moderate', 'Heavy', 'Extreme']
            ).astype(str)
        
        # Create app categories
        if 'app_name' in df_features.columns:
            social_media_apps = ['Instagram', 'Facebook', 'Twitter', 'Snapchat', 'TikTok']
            entertainment_apps = ['YouTube', 'Netflix', 'Spotify']
            communication_apps = ['WhatsApp', 'Telegram', 'Discord']
            
            def categorize_app(app_name):
                if app_name in social_media_apps:
                    return 'Social Media'
                elif app_name in entertainment_apps:
                    return 'Entertainment'
                elif app_name in communication_apps:
                    return 'Communication'
                else:
                    return 'Other'
            
            df_features['app_category'] = df_features['app_name'].apply(categorize_app)
        
        # Create time-based features
        if 'usage_minutes' in df_features.columns:
            df_features['usage_hours'] = df_features['usage_minutes'] / 60
            df_features['is_heavy_user'] = (df_features['usage_minutes'] > 180).astype(int)
        
        logger.info(f"✅ Feature engineering completed. New shape: {df_features.shape}")
        return df_features
    
    def process_complete(self, file_path: str) -> Tuple[pd.DataFrame, Dict[str, Any]]:
        """
        Complete data processing pipeline with insights generation.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Tuple of (processed_dataframe, insights_dictionary)
        """
        # Process the data
        processed_df = self.load_and_prepare_data(file_path)
        
        # Generate insights
        insights = self._generate_insights(processed_df)
        
        return processed_df, insights
    
    def _generate_insights(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate insights from the processed data.
        
        Args:
            df: Processed DataFrame
            
        Returns:
            Dictionary containing data insights
        """
        logger.info("📈 Generating data insights...")
        
        insights = {}
        
        # Basic statistics
        insights['user_stats'] = {
            'total_users': len(df),
            'total_sessions': len(df),
            'unique_apps': df['app_name'].nunique() if 'app_name' in df.columns else 0,
            'avg_usage_minutes': df['usage_minutes'].mean() if 'usage_minutes' in df.columns else 0,
            'total_usage_hours': df['usage_minutes'].sum() / 60 if 'usage_minutes' in df.columns else 0
        }
        
        # App-specific insights
        if 'app_name' in df.columns and 'usage_minutes' in df.columns:
            app_stats = df.groupby('app_name')['usage_minutes'].agg(['mean', 'count', 'sum']).round(2)
            insights['app_insights'] = {
                app: {
                    'avg_usage': stats['mean'],
                    'sessions': stats['count'],
                    'total_usage': stats['sum']
                }
                for app, stats in app_stats.iterrows()
            }
        
        # Usage category distribution
        if 'usage_category' in df.columns:
            category_dist = df['usage_category'].value_counts()
            insights['usage_distribution'] = category_dist.to_dict()
        
        # Day of week patterns
        if 'day_of_week' in df.columns and 'usage_minutes' in df.columns:
            day_stats = df.groupby('day_of_week')['usage_minutes'].mean().round(2)
            insights['day_patterns'] = day_stats.to_dict()
        
        logger.info("✅ Insights generation completed")
        return insights
    
    def get_sample_users(self, n: int = 5) -> pd.DataFrame:
        """
        Get sample users for simulation.
        
        Args:
            n: Number of sample users to return
            
        Returns:
            DataFrame with sample users
        """
        if self.processed_data is None:
            raise ValueError("No processed data available. Run load_and_prepare_data() first.")
        
        return self.processed_data.sample(n=min(n, len(self.processed_data)))


def main():
    """Demo function to test data processing."""
    print("📊 DATA PROCESSOR DEMO")
    print("=" * 40)
    
    # Create sample data for testing
    sample_data = {
        'userId': [f'user_{i:03d}' for i in range(1, 101)],
        'app_name': np.random.choice(['Instagram', 'TikTok', 'YouTube', 'Twitter', 'WhatsApp'], 100),
        'usage_minutes': np.random.normal(150, 60, 100).clip(10, 500),
        'roast_category_1': np.random.choice(['social_life', 'productivity', 'health', 'career'], 100),
        'roast_intensity': np.random.choice(['light', 'medium', 'brutal'], 100)
    }
    
    # Create temporary CSV
    temp_df = pd.DataFrame(sample_data)
    temp_path = "temp_sample_data.csv"
    temp_df.to_csv(temp_path, index=False)
    
    try:
        # Test the processor
        processor = DataProcessor()
        processed_data, insights = processor.process_complete(temp_path)
        
        print(f"✅ Processed {len(processed_data)} records")
        print(f"📊 Columns: {list(processed_data.columns)}")
        print(f"📈 Average usage: {insights['user_stats']['avg_usage_minutes']:.1f} minutes")
        print(f"📱 Unique apps: {insights['user_stats']['unique_apps']}")
        
        # Show sample
        print("\n📋 Sample processed data:")
        print(processed_data.head())
        
    finally:
        # Clean up
        if os.path.exists(temp_path):
            os.remove(temp_path)


if __name__ == "__main__":
    main()