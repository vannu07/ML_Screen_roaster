#!/usr/bin/env python3
"""
Tests for data processing functionality.
"""

import unittest
import pandas as pd
import numpy as np
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data.data_processor import DataProcessor
from utils.config import Config


class TestDataProcessor(unittest.TestCase):
    """Test cases for DataProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.processor = DataProcessor()
        
        # Create sample data
        self.sample_data = pd.DataFrame({
            'userId': ['user_001', 'user_002', 'user_003'],
            'app_name': ['Instagram', 'TikTok', 'YouTube'],
            'usage_minutes': [120, 180, 90],
            'roast_intensity': ['medium', 'brutal', 'light'],
            'roast_category_1': ['health', 'career', 'social_life'],
            'roast_category_2': [None, 'health', None],
            'date': ['2025-07-15', '2025-07-16', '2025-07-17']
        })
    
    def test_process_data(self):
        """Test complete data processing pipeline."""
        processed_data = self.processor.process_data(self.sample_data)
        
        # Check that data is processed
        self.assertIsNotNone(processed_data)
        self.assertEqual(len(processed_data), 3)
        
        # Check that missing values are handled
        self.assertFalse(processed_data['roast_category_2'].isnull().any())
        
        # Check that date is converted to datetime
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(processed_data['date']))
        
        # Check that day_of_week is created
        self.assertIn('day_of_week', processed_data.columns)
    
    def test_feature_engineering(self):
        """Test feature engineering functionality."""
        processed_data = self.processor.process_data(self.sample_data)
        
        # Check new features are created
        expected_features = ['day_of_week', 'usage_category', 'month', 'day_of_month', 'is_weekend']
        for feature in expected_features:
            self.assertIn(feature, processed_data.columns)
    
    def test_prepare_modeling_features(self):
        """Test preparation of modeling features."""
        processed_data = self.processor.process_data(self.sample_data)
        X, y = self.processor.prepare_modeling_features()
        
        # Check shapes
        self.assertEqual(len(X), len(processed_data))
        self.assertEqual(len(y), len(processed_data))
        
        # Check feature columns
        expected_features = ['roast_intensity', 'app_name', 'day_of_week']
        self.assertListEqual(list(X.columns), expected_features)
    
    def test_data_insights(self):
        """Test data insights generation."""
        processed_data = self.processor.process_data(self.sample_data)
        insights = self.processor.get_data_insights()
        
        # Check insights structure
        self.assertIn('total_records', insights)
        self.assertIn('unique_users', insights)
        self.assertIn('intensity_distribution', insights)
        
        # Check values
        self.assertEqual(insights['total_records'], 3)
        self.assertEqual(insights['unique_users'], 3)


if __name__ == '__main__':
    unittest.main()