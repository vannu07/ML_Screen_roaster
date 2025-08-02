#!/usr/bin/env python3
"""
Configuration file for Screen Time Roast Analyzer
Customize settings, prompts, and behavior here.
"""

# Model Configuration
MODEL_CONFIG = {
    'test_size': 0.2,
    'random_state': 42,
    'max_depth': 10,
    'features': ['roast_intensity', 'app_name', 'day_of_week'],
    'target': 'usage_minutes'
}

# Visualization Configuration
VIZ_CONFIG = {
    'figure_size': (12, 8),
    'style': 'seaborn-v0_8',
    'color_palette': ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'],
    'show_plots': True
}

# Roast Intensity Instructions
INTENSITY_INSTRUCTIONS = {
    'light': "Keep it playful and gentle, like a friendly tease between friends. Use humor that makes them smile rather than cringe.",
    'medium': "Make it witty and clever with a good balance of humor and reality check. Include some sass but keep it entertaining.",
    'brutal': "Go all out with savage humor! Be ruthlessly funny and don't hold back. Make it hilariously harsh but still entertaining."
}

# App-Specific Contexts for Roasting
APP_CONTEXTS = {
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

# Category-Specific Focus Areas
CATEGORY_FOCUS = {
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

# Hinglish Phrases and Expressions
HINGLISH_PHRASES = [
    "Yaar", "Bhai", "Arre", "Kya baat hai", "Sach mein", "Bilkul", 
    "Bas kar", "Chill maar", "Tension mat le", "Paisa vasool",
    "Time pass", "Bindaas", "Jugaad", "Funda", "Scene", "Vibe"
]

# Cultural References
CULTURAL_REFERENCES = [
    "Sharma ji ka beta", "Ghar wale", "Padosi", "Relatives", 
    "College friends", "Office colleagues", "Gym jaana", 
    "Cooking skills", "Traffic", "Metro", "Rickshaw"
]

# Gemini API Configuration
GEMINI_CONFIG = {
    'model_name': 'gemini-pro',
    'temperature': 0.7,
    'max_tokens': 150,
    'timeout': 30
}

# Prompt Template
ROAST_PROMPT_TEMPLATE = """Generate a {intensity} intensity, witty, and funny roast in Hinglish (Hindi-English mix) for a user who is predicted to spend {time_str} on {app_name}.

ROAST REQUIREMENTS:
- Intensity Level: {intensity_upper} - {intensity_instruction}
- Primary Focus: {focus_area}
- App Context: Target {app_context}
- Language Style: Hinglish (mix Hindi and English naturally, like how young Indians speak)
- Tone: Humorous, relatable, and entertaining
- Length: 2-3 sentences maximum

CONTEXT DETAILS:
- Predicted Usage Time: {predicted_usage:.0f} minutes ({time_str})
- App: {app_name}
- Roast Category: {roast_category}
- Focus on the irony and humor of spending this much time on {app_name}

STYLE GUIDELINES:
- Use popular Hinglish phrases and expressions
- Include relatable references to Indian culture/lifestyle
- Make it sound like a friend roasting another friend
- Avoid offensive content, keep it fun and entertaining
- Use emojis sparingly but effectively

Generate a roast that will make the user laugh while also making them think about their {app_name} usage habits!"""

# Data Validation Rules
DATA_VALIDATION = {
    'required_columns': [
        'userId', 'roast_category_1', 'roast_intensity', 
        'date', 'app_name', 'usage_minutes'
    ],
    'valid_intensities': ['light', 'medium', 'brutal'],
    'valid_apps': [
        'Instagram', 'TikTok', 'YouTube', 'Twitter', 'Reddit',
        'Facebook', 'Snapchat', 'WhatsApp', 'LinkedIn'
    ],
    'usage_range': (1, 1440),  # 1 minute to 24 hours
    'date_format': '%Y-%m-%d'
}

# Output Configuration
OUTPUT_CONFIG = {
    'show_progress': True,
    'verbose_logging': True,
    'save_results': False,
    'results_file': 'roast_results.json',
    'demo_users': 5
}

# Performance Thresholds
PERFORMANCE_THRESHOLDS = {
    'min_r2_score': 0.5,
    'max_mae_minutes': 60,
    'min_samples': 100
}

# Custom Roast Templates by App and Intensity
CUSTOM_ROAST_TEMPLATES = {
    'Instagram': {
        'brutal': "Bhai {predicted_usage:.0f} minutes Instagram pe? Itna time mein toh khud ka photoshoot kar lete! But nahi, tumhe toh bas dusron ki fake life dekhni hai! 📸",
        'medium': "Instagram pe {time_str}? Yaar, real life mein bhi kuch interesting karo, stories mein daalne ke liye! 📱",
        'light': "Instagram scrolling champion! {time_str} mein kitne reels dekhe? Just remember, real life bhi equally entertaining hai! 😄"
    },
    'TikTok': {
        'brutal': "{predicted_usage:.0f} minutes TikTok pe? Bhai, itna time mein actual dance class join kar lete! But nahi, tumhe toh bas 15-second videos dekhne hain! 🕺",
        'medium': "TikTok pe {time_str}? Koi naya dance seekha ya bas time waste kiya? Real skills develop karo yaar! 💃",
        'light': "TikTok expert spotted! {time_str} of entertainment, hope you learned some cool moves! 🎵"
    }
}

# Error Messages
ERROR_MESSAGES = {
    'file_not_found': "❌ CSV file not found! Please check the file path.",
    'invalid_data': "❌ Invalid data format! Please check your CSV structure.",
    'model_error': "❌ Model training failed! Check your data quality.",
    'api_error': "❌ API call failed! Check your internet connection and API key.",
    'insufficient_data': "❌ Not enough data for training! Need at least {min_samples} samples."
}

# Success Messages
SUCCESS_MESSAGES = {
    'data_loaded': "✅ Data loaded successfully!",
    'model_trained': "✅ Model trained successfully!",
    'roast_generated': "✅ Roast generated successfully!",
    'analysis_complete': "✅ Analysis completed successfully!"
}