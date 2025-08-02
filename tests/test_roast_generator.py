#!/usr/bin/env python3
"""
Tests for roast generation functionality.
"""

import unittest
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from roast.generator import RoastGenerator
from utils.config import Config


class TestRoastGenerator(unittest.TestCase):
    """Test cases for RoastGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.generator = RoastGenerator()
    
    def test_generate_roast_prompt(self):
        """Test roast prompt generation."""
        prompt = self.generator.generate_roast_prompt(
            app_name='Instagram',
            predicted_usage=180,
            roast_category='health',
            roast_intensity='medium'
        )
        
        # Check that prompt is generated
        self.assertIsInstance(prompt, str)
        self.assertGreater(len(prompt), 100)
        
        # Check that key elements are included
        self.assertIn('Instagram', prompt)
        self.assertIn('medium', prompt)
        self.assertIn('health', prompt)
        self.assertIn('Hinglish', prompt)
    
    def test_format_usage_time(self):
        """Test usage time formatting."""
        # Test minutes only
        time_str = self.generator._format_usage_time(45)
        self.assertEqual(time_str, "45 minutes")
        
        # Test hours and minutes
        time_str = self.generator._format_usage_time(125)
        self.assertEqual(time_str, "2 hours and 5 minutes")
        
        # Test exact hours
        time_str = self.generator._format_usage_time(120)
        self.assertEqual(time_str, "2 hours")
        
        # Test singular forms
        time_str = self.generator._format_usage_time(61)
        self.assertEqual(time_str, "1 hour and 1 minute")
    
    def test_validate_roast_inputs(self):
        """Test input validation."""
        # Valid inputs
        is_valid, errors = self.generator.validate_roast_inputs(
            'Instagram', 120, 'health', 'medium'
        )
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        
        # Invalid app name
        is_valid, errors = self.generator.validate_roast_inputs(
            '', 120, 'health', 'medium'
        )
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        
        # Invalid usage
        is_valid, errors = self.generator.validate_roast_inputs(
            'Instagram', -10, 'health', 'medium'
        )
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
        
        # Invalid intensity
        is_valid, errors = self.generator.validate_roast_inputs(
            'Instagram', 120, 'health', 'extreme'
        )
        self.assertFalse(is_valid)
        self.assertGreater(len(errors), 0)
    
    def test_get_roast_preview(self):
        """Test roast preview generation."""
        preview = self.generator.get_roast_preview(
            'TikTok', 240, 'career', 'brutal'
        )
        
        # Check preview structure
        self.assertIn('app_name', preview)
        self.assertIn('usage_time', preview)
        self.assertIn('intensity', preview)
        self.assertIn('category', preview)
        
        # Check values
        self.assertEqual(preview['app_name'], 'TikTok')
        self.assertEqual(preview['usage_time'], '4 hours')
        self.assertEqual(preview['intensity'], 'brutal')
        self.assertEqual(preview['category'], 'career')
    
    def test_get_available_options(self):
        """Test getting available options."""
        options = self.generator.get_available_options()
        
        # Check structure
        self.assertIn('apps', options)
        self.assertIn('intensities', options)
        self.assertIn('categories', options)
        
        # Check that options are not empty
        self.assertGreater(len(options['apps']), 0)
        self.assertGreater(len(options['intensities']), 0)
        self.assertGreater(len(options['categories']), 0)


if __name__ == '__main__':
    unittest.main()