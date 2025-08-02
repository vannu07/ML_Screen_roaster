#!/usr/bin/env python3
"""
Gemini API client for Screen Time Roast Analyzer.
"""

import os
import time
from typing import Optional, Dict, Any, List
from utils.config import config
from utils.logger import analysis_logger

# Uncomment when google-generativeai is installed
# import google.generativeai as genai


class GeminiClient:
    """Client for interacting with Google's Gemini API."""
    
    def __init__(self, api_key: Optional[str] = None, config_instance=None):
        """
        Initialize Gemini API client.
        
        Args:
            api_key: Gemini API key (optional, will use environment variable if not provided)
            config_instance: Configuration instance (optional)
        """
        self.config = config_instance or config
        self.api_key = api_key or self.config.gemini.api_key
        self.client = None
        self.is_configured = False
        
        if self.api_key:
            self._setup_client()
        else:
            analysis_logger.warning("No Gemini API key provided")
            analysis_logger.info("Set GEMINI_API_KEY environment variable or pass api_key parameter")
            analysis_logger.info("Get your API key from: https://makersuite.google.com/app/apikey")
    
    def _setup_client(self) -> None:
        """Set up the Gemini API client."""
        try:
            # Uncomment when google-generativeai is installed
            # genai.configure(api_key=self.api_key)
            # self.client = genai.GenerativeModel(self.config.gemini.model_name)
            # self.is_configured = True
            # analysis_logger.success("Gemini API client configured successfully")
            
            # For now, just log that we would configure it
            analysis_logger.info("Gemini API client would be configured here")
            analysis_logger.info("Install google-generativeai package to enable real API calls")
            
        except Exception as e:
            analysis_logger.error(f"Failed to setup Gemini API client: {str(e)}")
            self.client = None
            self.is_configured = False
    
    def generate_roast(self, prompt: str) -> str:
        """
        Generate a roast using the Gemini API.
        
        Args:
            prompt: The roast prompt
            
        Returns:
            Generated roast response
        """
        if not self.is_configured:
            return self._simulate_roast_response(prompt)
        
        try:
            # Uncomment when API is set up
            # response = self.client.generate_content(
            #     prompt,
            #     generation_config={
            #         'temperature': self.config.gemini.temperature,
            #         'max_output_tokens': self.config.gemini.max_tokens,
            #     }
            # )
            # return response.text
            
            # For now, return simulated response
            return self._simulate_roast_response(prompt)
            
        except Exception as e:
            analysis_logger.error(f"Error generating roast: {str(e)}")
            return "Sorry yaar, roast machine thoda busy hai! Try again later! 😅"
    
    def _simulate_roast_response(self, prompt: str) -> str:
        """
        Simulate a roast response for demonstration purposes.
        
        Args:
            prompt: The roast prompt
            
        Returns:
            Simulated roast response
        """
        # Extract key information from prompt for better simulation
        prompt_lower = prompt.lower()
        
        # App-specific responses
        if "instagram" in prompt_lower:
            if "brutal" in prompt_lower:
                return "Bhai, itna time Instagram pe? 📱 Dusron ki perfect life dekhte dekhte apni life hi bhool gaye! Paisa kamane ke bajaye paisa waste karne mein expert ho gaye ho! 💸 Ab toh Sharma ji ka beta bhi tumse aage nikal gaya hoga! 😂"
            elif "medium" in prompt_lower:
                return "Instagram pe itna time? 📸 Yaar, real life mein bhi kuch interesting karo, stories mein daalne ke liye! Warna bas dusron ke reels dekhte dekhte apna time reel ho jayega! 😄"
            else:
                return "Instagram scrolling champion! 🏆 Bas thoda sa real world mein bhi time spend karo, wahan bhi equally entertaining cheezein hoti hain! 😊"
        
        elif "tiktok" in prompt_lower:
            if "brutal" in prompt_lower:
                return "TikTok pe itna time? 🕺 Bhai, actual dance class join kar lete! But nahi, tumhe toh bas 15-second videos dekhne hain! Productivity ka toh funeral ho gaya tumhara! ⚰️ Ab toh TikTok tumhara full-time job ban gaya hai! 😅"
            elif "medium" in prompt_lower:
                return "TikTok pe itna time? 💃 Koi naya dance seekha ya bas time waste kiya? Real skills develop karo yaar, warna resume mein 'TikTok Expert' likhna padega! 😂"
            else:
                return "TikTok expert spotted! 🎵 Hope you learned some cool moves! Just remember, real life mein bhi kuch productive karna padega! 😄"
        
        elif "youtube" in prompt_lower:
            if "brutal" in prompt_lower:
                return "YouTube pe itna time? 📺 'How to be productive' videos dekhte dekhte hi unproductive ho gaye! Career goals YouTube shorts mein kho gaye kya? Time to close the app and actually DO something! 💪"
            elif "medium" in prompt_lower:
                return "YouTube university se PhD kar rahe ho kya? 🎓 Itne videos dekhe hain, ab toh expert ban jana chahiye tha! But practical mein kya kiya? 🤔"
            else:
                return "YouTube pe research kar rahe the ya entertainment? 📚 Thoda balance maintain karo, knowledge gain karo but time bhi manage karo! 😊"
        
        elif "reddit" in prompt_lower:
            if "brutal" in prompt_lower:
                return "Reddit pe itna time? 🤯 Random strangers ke comments padhte padhte apni life ka comment section hi bhool gaye! Health ke liye Google kar rahe ho ya memes dekh rahe ho? Touch some grass, literally! 🌱"
            elif "medium" in prompt_lower:
                return "Reddit rabbit hole mein gir gaye? 🐰 Interesting discussions hote hain, but real world mein bhi kuch discuss karo! Friends ke saath bhi time spend karo! 😄"
            else:
                return "Reddit explorer! 🗺️ Interesting communities explore kar rahe ho, bas real life mein bhi explore karna mat bhoolna! 😊"
        
        elif "twitter" in prompt_lower:
            if "brutal" in prompt_lower:
                return "Twitter pe itna time? 🐦 Hot takes padhte padhte apna social life cold ho gaya! Real friends se baat karne ka time hai ya bas online drama dekhna hai? Get a life beyond the timeline! 📱➡️🌍"
            elif "medium" in prompt_lower:
                return "Twitter pe news updates ya drama updates dekh rahe the? 📰 Thoda filter karo content, mental peace bhi important hai! Real conversations bhi try karo! 😊"
            else:
                return "Twitter pe kya trending dekh rahe the? 📈 Hope it was something useful! Social media se thoda break leke social life mein bhi invest karo! 😄"
        
        else:
            # Generic response
            return "Yaar, screen time dekh ke lagta hai phone tumhara best friend ban gaya hai! 📱 Real world mein bhi kuch time spend karo, wahan bhi interesting cheezein hoti hain! Balance is key! 😉"
    
    def generate_batch_roasts(self, prompts: List[str]) -> List[str]:
        """
        Generate roasts for multiple prompts.
        
        Args:
            prompts: List of roast prompts
            
        Returns:
            List of generated roasts
        """
        roasts = []
        
        for i, prompt in enumerate(prompts):
            analysis_logger.progress(f"Generating roast {i+1}/{len(prompts)}")
            
            try:
                roast = self.generate_roast(prompt)
                roasts.append(roast)
                
                # Add small delay to avoid rate limiting
                if self.is_configured:
                    time.sleep(0.5)
                    
            except Exception as e:
                analysis_logger.error(f"Error generating roast {i+1}: {str(e)}")
                roasts.append("Sorry, couldn't generate roast for this one! 😅")
        
        return roasts
    
    def test_connection(self) -> bool:
        """
        Test the connection to Gemini API.
        
        Returns:
            True if connection is successful, False otherwise
        """
        if not self.is_configured:
            analysis_logger.warning("Gemini API not configured")
            return False
        
        try:
            # Test with a simple prompt
            test_prompt = "Say 'Hello' in Hinglish"
            response = self.generate_roast(test_prompt)
            
            if response and len(response) > 0:
                analysis_logger.success("Gemini API connection test successful")
                return True
            else:
                analysis_logger.error("Gemini API returned empty response")
                return False
                
        except Exception as e:
            analysis_logger.error(f"Gemini API connection test failed: {str(e)}")
            return False
    
    def get_api_status(self) -> Dict[str, Any]:
        """
        Get the status of the Gemini API client.
        
        Returns:
            Dictionary with API status information
        """
        return {
            'is_configured': self.is_configured,
            'has_api_key': bool(self.api_key),
            'model_name': self.config.gemini.model_name,
            'temperature': self.config.gemini.temperature,
            'max_tokens': self.config.gemini.max_tokens,
            'timeout': self.config.gemini.timeout
        }
    
    def update_config(self, **kwargs) -> None:
        """
        Update Gemini API configuration.
        
        Args:
            **kwargs: Configuration parameters to update
        """
        for key, value in kwargs.items():
            if hasattr(self.config.gemini, key):
                setattr(self.config.gemini, key, value)
                analysis_logger.info(f"Updated Gemini config: {key} = {value}")
            else:
                analysis_logger.warning(f"Unknown Gemini config parameter: {key}")
        
        # Reconfigure client if API key was updated
        if 'api_key' in kwargs:
            self.api_key = kwargs['api_key']
            self._setup_client()