#!/usr/bin/env python3
"""
Prompt Generator Module for Screen Time Roast Analyzer
Creates dynamic prompts for the Gemini API based on user context and predictions.
"""

import logging
from typing import Dict, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_roast_prompt(app_name: str, predicted_usage: float, roast_category: str, roast_intensity: str) -> str:
    """
    Generate a dynamic roast prompt for the Gemini API.
    
    Args:
        app_name: Name of the app (e.g., "Instagram", "TikTok")
        predicted_usage: Predicted usage time in minutes
        roast_category: Category of roast (e.g., "social_life", "career", "health")
        roast_intensity: Intensity level ("light", "medium", "brutal")
        
    Returns:
        Formatted prompt string ready for Gemini API
    """
    
    # Convert usage to hours and minutes for better readability
    hours = int(predicted_usage // 60)
    minutes = int(predicted_usage % 60)
    
    if hours > 0:
        usage_text = f"{hours} hours and {minutes} minutes" if minutes > 0 else f"{hours} hours"
    else:
        usage_text = f"{minutes} minutes"
    
    # App-specific context
    app_contexts = {
        "Instagram": {
            "addiction_type": "social comparison and endless scrolling",
            "typical_behavior": "double-tapping photos and watching stories",
            "time_waste": "comparing your life to others' highlight reels"
        },
        "TikTok": {
            "addiction_type": "short-form video binge-watching",
            "typical_behavior": "swiping up for 'just one more video'",
            "time_waste": "watching dance videos and random content"
        },
        "YouTube": {
            "addiction_type": "video binge-watching and rabbit holes",
            "typical_behavior": "falling into recommendation loops",
            "time_waste": "watching 'educational' videos that aren't really educational"
        },
        "Twitter": {
            "addiction_type": "news and social media drama consumption",
            "typical_behavior": "doom-scrolling and engaging in arguments",
            "time_waste": "reading hot takes and getting angry at strangers"
        },
        "Reddit": {
            "addiction_type": "endless thread reading and discussion",
            "typical_behavior": "going down comment rabbit holes",
            "time_waste": "reading debates about topics you don't care about"
        },
        "Facebook": {
            "addiction_type": "social networking and news feed scrolling",
            "typical_behavior": "checking what everyone is up to",
            "time_waste": "reading posts from people you barely know"
        },
        "WhatsApp": {
            "addiction_type": "constant messaging and group chat monitoring",
            "typical_behavior": "checking messages every few minutes",
            "time_waste": "reading forwarded messages and group drama"
        },
        "Netflix": {
            "addiction_type": "binge-watching shows and movies",
            "typical_behavior": "saying 'just one more episode'",
            "time_waste": "watching shows you don't even enjoy"
        },
        "Snapchat": {
            "addiction_type": "story viewing and snap streaks",
            "typical_behavior": "maintaining streaks and checking stories",
            "time_waste": "sending meaningless snaps to keep streaks alive"
        },
        "Spotify": {
            "addiction_type": "music streaming and playlist creation",
            "typical_behavior": "constantly switching songs and creating playlists",
            "time_waste": "spending more time choosing music than listening"
        }
    }
    
    # Get app-specific context or use generic
    app_context = app_contexts.get(app_name, {
        "addiction_type": "digital content consumption",
        "typical_behavior": "mindless scrolling and tapping",
        "time_waste": "consuming content that adds no value to your life"
    })
    
    # Intensity-based tone
    intensity_tones = {
        "light": {
            "opening": "Hey there, digital explorer! 😊",
            "tone": "friendly and encouraging",
            "closing": "Maybe it's time for a little digital detox? 🌱"
        },
        "medium": {
            "opening": "Alright, let's talk about your screen time habits! 📱",
            "tone": "direct but supportive",
            "closing": "Time to take control of your digital life! 💪"
        },
        "brutal": {
            "opening": "Bro, we need to have a serious conversation! 🔥",
            "tone": "brutally honest and savage",
            "closing": "Wake up and smell the reality! ⏰"
        }
    }
    
    tone_config = intensity_tones.get(roast_intensity, intensity_tones["medium"])
    
    # Category-specific focus areas
    category_focuses = {
        "social_life": "how this app usage is affecting your real-world relationships and social interactions",
        "career": "how this excessive screen time is impacting your professional growth and productivity",
        "health": "how this digital addiction is affecting your physical and mental well-being",
        "finance": "how this time could be better spent on improving your financial situation",
        "laziness": "how this app is enabling your procrastination and lazy habits",
        "productivity": "how this usage is destroying your focus and ability to get things done"
    }
    
    category_focus = category_focuses.get(roast_category, "how this excessive usage is impacting your overall life balance")
    
    # Build the comprehensive prompt
    prompt = f"""
You are a witty, culturally aware AI roast generator that creates personalized, humorous critiques of people's screen time habits. Your job is to create a roast that's {tone_config['tone']} while being entertaining and thought-provoking.

USER CONTEXT:
- App: {app_name}
- Predicted Usage Time: {usage_text}
- Primary Concern: {roast_category}
- Roast Intensity: {roast_intensity}

APP-SPECIFIC CONTEXT:
- Addiction Type: {app_context['addiction_type']}
- Typical Behavior: {app_context['typical_behavior']}
- Time Waste Pattern: {app_context['time_waste']}

ROAST REQUIREMENTS:
1. **Tone**: {tone_config['tone']}
2. **Opening**: Start with something like "{tone_config['opening']}"
3. **Focus Area**: Emphasize {category_focus}
4. **Cultural Elements**: Include Hinglish phrases and Indian cultural references where appropriate
5. **Length**: 3-4 sentences maximum
6. **Style**: Mix of humor, reality check, and motivation

SPECIFIC FOCUS:
The user is predicted to spend {usage_text} on {app_name}, which involves {app_context['addiction_type']}. Focus on {category_focus} and make it relatable to someone who spends this much time {app_context['typical_behavior']}.

INTENSITY GUIDELINES:
- Light: Gentle nudging with humor, encouraging tone
- Medium: Direct reality check with balanced humor and concern
- Brutal: Savage, no-holds-barred roasting with harsh truths

Generate a roast that will make the user laugh, think, and maybe feel a little called out. End with something motivational like "{tone_config['closing']}"

Remember: Be witty, be real, but don't be mean-spirited. The goal is to create awareness through humor, not to hurt feelings.
"""
    
    logger.info(f"✅ Generated roast prompt for {app_name} ({usage_text}, {roast_intensity} intensity)")
    return prompt.strip()


def generate_simple_roast_prompt(app_name: str, predicted_usage: float) -> str:
    """
    Generate a simple roast prompt with default settings.
    
    Args:
        app_name: Name of the app
        predicted_usage: Predicted usage time in minutes
        
    Returns:
        Simple formatted prompt string
    """
    return generate_roast_prompt(app_name, predicted_usage, "productivity", "medium")


def get_app_specific_insights(app_name: str) -> Dict:
    """
    Get app-specific insights for roast generation.
    
    Args:
        app_name: Name of the app
        
    Returns:
        Dictionary with app insights
    """
    insights = {
        "Instagram": {
            "primary_addiction": "Visual social comparison",
            "common_excuses": ["Just checking stories", "Looking for inspiration"],
            "reality_check": "You're comparing your behind-the-scenes to others' highlight reels",
            "alternative_activity": "Go create real memories instead of consuming others'"
        },
        "TikTok": {
            "primary_addiction": "Dopamine-driven short content",
            "common_excuses": ["It's educational", "Just for a few minutes"],
            "reality_check": "Your attention span is getting shorter with each swipe",
            "alternative_activity": "Learn a real skill that takes more than 60 seconds"
        },
        "YouTube": {
            "primary_addiction": "Information overload and entertainment",
            "common_excuses": ["I'm learning something", "It's research"],
            "reality_check": "Watching productivity videos doesn't make you productive",
            "alternative_activity": "Actually practice what you've been watching tutorials about"
        },
        "Twitter": {
            "primary_addiction": "News and opinion consumption",
            "common_excuses": ["Staying informed", "Networking"],
            "reality_check": "You're getting angry at strangers' opinions all day",
            "alternative_activity": "Have real conversations with people you actually know"
        },
        "Reddit": {
            "primary_addiction": "Discussion and community browsing",
            "common_excuses": ["Learning from discussions", "Community engagement"],
            "reality_check": "You're reading debates about topics you'll forget tomorrow",
            "alternative_activity": "Join a real community or hobby group offline"
        }
    }
    
    return insights.get(app_name, {
        "primary_addiction": "Digital content consumption",
        "common_excuses": ["Just checking quickly", "It's important"],
        "reality_check": "You're spending precious time on things that don't matter",
        "alternative_activity": "Do something that actually improves your life"
    })


def main():
    """Demo function to test prompt generation."""
    print("🎭 PROMPT GENERATOR DEMO")
    print("=" * 50)
    
    # Test different scenarios
    test_cases = [
        ("Instagram", 180, "social_life", "brutal"),
        ("TikTok", 240, "productivity", "medium"),
        ("YouTube", 120, "career", "light"),
        ("Twitter", 90, "health", "medium")
    ]
    
    for app, usage, category, intensity in test_cases:
        print(f"\n📱 {app.upper()} - {usage} minutes ({intensity} intensity)")
        print("-" * 40)
        prompt = generate_roast_prompt(app, usage, category, intensity)
        print(prompt[:200] + "..." if len(prompt) > 200 else prompt)
        print()


if __name__ == "__main__":
    main()