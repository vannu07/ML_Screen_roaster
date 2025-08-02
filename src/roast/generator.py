#!/usr/bin/env python3
"""
Roast generation system for Screen Time Roast Analyzer.
"""

import pandas as pd
from typing import Dict, Any, Optional
from utils.config import config
from utils.logger import analysis_logger


class RoastGenerator:
    """Generates context-aware roast prompts for the Gemini API."""
    
    def __init__(self, config_instance=None):
        """Initialize roast generator with configuration."""
        self.config = config_instance or config
        self.roast_config = self.config.roast
    
    def generate_roast_prompt(
        self, 
        app_name: str, 
        predicted_usage: float, 
        roast_category: str, 
        roast_intensity: str,
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate a detailed, context-aware prompt for the Gemini API.
        
        Args:
            app_name: Name of the app
            predicted_usage: Predicted usage minutes
            roast_category: Category for roasting (e.g., 'health', 'career')
            roast_intensity: Intensity level ('light', 'medium', 'brutal')
            user_context: Additional user context (optional)
            
        Returns:
            Formatted prompt for Gemini API
        """
        # Convert predicted usage to readable format
        time_str = self._format_usage_time(predicted_usage)
        
        # Get configuration elements
        intensity_instruction = self.roast_config.intensity_instructions.get(
            roast_intensity, 
            "Generate a humorous roast"
        )
        
        app_context = self.roast_config.app_contexts.get(
            app_name, 
            f"their {app_name} usage habits"
        )
        
        focus_area = self.roast_config.category_focus.get(
            roast_category, 
            "their screen time habits"
        )
        
        # Build the comprehensive prompt
        prompt = self._build_prompt_template(
            app_name=app_name,
            predicted_usage=predicted_usage,
            time_str=time_str,
            roast_category=roast_category,
            roast_intensity=roast_intensity,
            intensity_instruction=intensity_instruction,
            app_context=app_context,
            focus_area=focus_area,
            user_context=user_context
        )
        
        return prompt
    
    def _format_usage_time(self, minutes: float) -> str:
        """
        Format usage time into readable string.
        
        Args:
            minutes: Usage time in minutes
            
        Returns:
            Formatted time string
        """
        hours = int(minutes // 60)
        remaining_minutes = int(minutes % 60)
        
        if hours > 0:
            if remaining_minutes > 0:
                return f"{hours} hour{'s' if hours != 1 else ''} and {remaining_minutes} minute{'s' if remaining_minutes != 1 else ''}"
            else:
                return f"{hours} hour{'s' if hours != 1 else ''}"
        else:
            return f"{remaining_minutes} minute{'s' if remaining_minutes != 1 else ''}"
    
    def _build_prompt_template(
        self,
        app_name: str,
        predicted_usage: float,
        time_str: str,
        roast_category: str,
        roast_intensity: str,
        intensity_instruction: str,
        app_context: str,
        focus_area: str,
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Build the complete prompt template."""
        
        # Base prompt template
        prompt = f"""Generate a {roast_intensity} intensity, witty, and funny roast in Hinglish (Hindi-English mix) for a user who is predicted to spend {time_str} on {app_name}.

ROAST REQUIREMENTS:
- Intensity Level: {roast_intensity.upper()} - {intensity_instruction}
- Primary Focus: {focus_area}
- App Context: Target {app_context}
- Language Style: Hinglish (mix Hindi and English naturally, like how young Indians speak)
- Tone: Humorous, relatable, and entertaining
- Length: 2-3 sentences maximum

CONTEXT DETAILS:
- Predicted Usage Time: {predicted_usage:.0f} minutes ({time_str})
- App: {app_name}
- Roast Category: {roast_category}
- Focus on the irony and humor of spending this much time on {app_name}"""
        
        # Add user context if provided
        if user_context:
            prompt += f"\n- Additional Context: {self._format_user_context(user_context)}"
        
        # Add style guidelines
        prompt += f"""

STYLE GUIDELINES:
- Use popular Hinglish phrases and expressions
- Include relatable references to Indian culture/lifestyle
- Make it sound like a friend roasting another friend
- Avoid offensive content, keep it fun and entertaining
- Use emojis sparingly but effectively

HINGLISH PHRASES TO CONSIDER:
{', '.join(self.roast_config.hinglish_phrases[:10])}

CULTURAL REFERENCES TO USE:
{', '.join(self.roast_config.cultural_references[:8])}

Generate a roast that will make the user laugh while also making them think about their {app_name} usage habits!"""
        
        return prompt
    
    def _format_user_context(self, user_context: Dict[str, Any]) -> str:
        """Format additional user context for the prompt."""
        context_parts = []
        
        if 'day_of_week' in user_context:
            context_parts.append(f"Day: {user_context['day_of_week']}")
        
        if 'usage_category' in user_context:
            context_parts.append(f"Usage Pattern: {user_context['usage_category']}")
        
        if 'is_weekend' in user_context:
            day_type = "weekend" if user_context['is_weekend'] else "weekday"
            context_parts.append(f"Day Type: {day_type}")
        
        return ", ".join(context_parts)
    
    def generate_custom_roast_prompt(
        self,
        template: str,
        **kwargs
    ) -> str:
        """
        Generate roast prompt using a custom template.
        
        Args:
            template: Custom prompt template with placeholders
            **kwargs: Values to fill in the template
            
        Returns:
            Formatted prompt
        """
        try:
            return template.format(**kwargs)
        except KeyError as e:
            analysis_logger.error(f"Missing template variable: {e}")
            return self.generate_roast_prompt(
                kwargs.get('app_name', 'Unknown'),
                kwargs.get('predicted_usage', 0),
                kwargs.get('roast_category', 'general'),
                kwargs.get('roast_intensity', 'medium')
            )
    
    def get_roast_preview(
        self,
        app_name: str,
        predicted_usage: float,
        roast_category: str,
        roast_intensity: str
    ) -> Dict[str, Any]:
        """
        Get a preview of roast elements without generating full prompt.
        
        Args:
            app_name: Name of the app
            predicted_usage: Predicted usage minutes
            roast_category: Category for roasting
            roast_intensity: Intensity level
            
        Returns:
            Dictionary with roast preview elements
        """
        return {
            'app_name': app_name,
            'usage_time': self._format_usage_time(predicted_usage),
            'usage_minutes': predicted_usage,
            'intensity': roast_intensity,
            'category': roast_category,
            'intensity_description': self.roast_config.intensity_instructions.get(roast_intensity, ''),
            'app_context': self.roast_config.app_contexts.get(app_name, f'{app_name} usage'),
            'focus_area': self.roast_config.category_focus.get(roast_category, 'screen time habits'),
            'suggested_phrases': self.roast_config.hinglish_phrases[:5],
            'cultural_refs': self.roast_config.cultural_references[:3]
        }
    
    def validate_roast_inputs(
        self,
        app_name: str,
        predicted_usage: float,
        roast_category: str,
        roast_intensity: str
    ) -> tuple[bool, list[str]]:
        """
        Validate inputs for roast generation.
        
        Args:
            app_name: Name of the app
            predicted_usage: Predicted usage minutes
            roast_category: Category for roasting
            roast_intensity: Intensity level
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Validate app name
        if not app_name or not isinstance(app_name, str):
            errors.append("App name must be a non-empty string")
        
        # Validate predicted usage
        if not isinstance(predicted_usage, (int, float)) or predicted_usage < 0:
            errors.append("Predicted usage must be a non-negative number")
        elif predicted_usage > 1440:  # More than 24 hours
            errors.append("Predicted usage cannot exceed 1440 minutes (24 hours)")
        
        # Validate roast intensity
        if roast_intensity not in self.roast_config.intensity_instructions:
            valid_intensities = list(self.roast_config.intensity_instructions.keys())
            errors.append(f"Roast intensity must be one of: {valid_intensities}")
        
        # Validate roast category
        if roast_category not in self.roast_config.category_focus:
            valid_categories = list(self.roast_config.category_focus.keys())
            errors.append(f"Roast category must be one of: {valid_categories}")
        
        return len(errors) == 0, errors
    
    def get_available_options(self) -> Dict[str, list]:
        """
        Get all available options for roast generation.
        
        Returns:
            Dictionary with available options
        """
        return {
            'apps': list(self.roast_config.app_contexts.keys()),
            'intensities': list(self.roast_config.intensity_instructions.keys()),
            'categories': list(self.roast_config.category_focus.keys()),
            'hinglish_phrases': self.roast_config.hinglish_phrases,
            'cultural_references': self.roast_config.cultural_references
        }
    
    def generate_batch_prompts(
        self,
        user_data: pd.DataFrame,
        predictions: list
    ) -> list[Dict[str, Any]]:
        """
        Generate roast prompts for multiple users.
        
        Args:
            user_data: DataFrame with user information
            predictions: List of usage predictions
            
        Returns:
            List of dictionaries with user info and prompts
        """
        if len(user_data) != len(predictions):
            raise ValueError("User data and predictions must have the same length")
        
        batch_results = []
        
        for i, (_, user_row) in enumerate(user_data.iterrows()):
            try:
                # Validate inputs
                is_valid, errors = self.validate_roast_inputs(
                    user_row['app_name'],
                    predictions[i],
                    user_row['roast_category_1'],
                    user_row['roast_intensity']
                )
                
                if not is_valid:
                    analysis_logger.warning(f"Invalid inputs for user {user_row['userId']}: {errors}")
                    continue
                
                # Generate prompt
                prompt = self.generate_roast_prompt(
                    app_name=user_row['app_name'],
                    predicted_usage=predictions[i],
                    roast_category=user_row['roast_category_1'],
                    roast_intensity=user_row['roast_intensity'],
                    user_context={
                        'day_of_week': user_row.get('day_of_week'),
                        'is_weekend': user_row.get('is_weekend')
                    }
                )
                
                batch_results.append({
                    'user_id': user_row['userId'],
                    'app_name': user_row['app_name'],
                    'predicted_usage': predictions[i],
                    'actual_usage': user_row.get('usage_minutes', 0),
                    'roast_intensity': user_row['roast_intensity'],
                    'roast_category': user_row['roast_category_1'],
                    'day_of_week': user_row.get('day_of_week'),
                    'roast_prompt': prompt
                })
                
            except Exception as e:
                analysis_logger.error(f"Error generating prompt for user {user_row['userId']}: {str(e)}")
                continue
        
        analysis_logger.success(f"Generated {len(batch_results)} roast prompts")
        return batch_results