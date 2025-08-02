# 🔥 Screen Time Roast Analyzer

A machine learning-powered system that analyzes screen time patterns and generates personalized, witty roasts to help users become more aware of their digital habits.

## 🎯 Project Overview

This project combines data science, machine learning, and AI-powered content generation to create a unique digital wellness tool. It predicts user screen time based on behavioral patterns and generates culturally relevant, humorous roasts using the Gemini API.

## 📁 Project Structure

```
├── data/
│   └── sample_roast_data.csv          # Sample dataset for training and testing
│
├── src/
│   ├── __init__.py                    # Package initialization
│   ├── data_processor.py              # Data loading and preprocessing
│   ├── model_trainer.py               # ML model training and evaluation
│   ├── prompt_generator.py            # Dynamic prompt generation for Gemini API
│   └── simulation.py                  # Main pipeline and user experience simulation
│
├── .gitignore                         # Git ignore rules
├── README.md                          # Project documentation
└── requirements.txt                   # Python dependencies
```

## 🚀 Features

- **📊 Data Processing**: Comprehensive data cleaning and feature engineering
- **🤖 ML Prediction**: Random Forest model for usage time prediction
- **🎭 Dynamic Roasting**: Context-aware prompt generation with multiple intensity levels
- **🌍 Cultural Adaptation**: Hinglish phrases and Indian cultural references
- **📱 App-Specific Context**: Tailored roasts for different social media platforms
- **📈 Performance Metrics**: Model evaluation and accuracy tracking

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/vannu07/ML_Screen_roaster.git
   cd ML_Screen_roaster
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gemini API** (optional for full functionality):
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

## 🎮 Usage

### Quick Start - Run Complete Simulation

```bash
python src/simulation.py
```

This will:
1. Load and process the sample data
2. Train the ML model
3. Simulate user experiences with sample users
4. Generate roast prompts for each user
5. Display comprehensive results

### Individual Module Usage

#### 1. Data Processing
```python
from src.data_processor import DataProcessor

processor = DataProcessor()
processed_data, insights = processor.process_complete("data/sample_roast_data.csv")
print(f"Processed {insights['user_stats']['total_users']} users")
```

#### 2. Model Training
```python
from src.model_trainer import ModelTrainer

trainer = ModelTrainer()
results = trainer.train_model(processed_data)
print(f"Model R² Score: {results['test_r2']:.3f}")
```

#### 3. Prompt Generation
```python
from src.prompt_generator import generate_roast_prompt

prompt = generate_roast_prompt(
    app_name="Instagram",
    predicted_usage=180,  # 3 hours
    roast_category="social_life",
    roast_intensity="brutal"
)
print(prompt)
```

## 📊 Sample Output

```
👤 USER 1 SIMULATION RESULTS
====================================
📱 App: Instagram
🆔 User ID: user_087
📅 Day: Sunday
🎯 Roast Category: social_life
🔥 Roast Intensity: brutal

📊 USAGE PREDICTION:
   Actual Usage: 210 minutes (3.5 hours)
   Predicted Usage: 195 minutes (3.2 hours)
   Prediction Error: 15 minutes
   Accuracy: 92.3%

🎭 GENERATED ROAST PROMPT:
────────────────────────────────────
Bro, we need to have a serious conversation! 🔥

You're predicted to spend 3 hours and 15 minutes on Instagram, 
which involves social comparison and endless scrolling. Focus on 
how this app usage is affecting your real-world relationships 
and social interactions...

Wake up and smell the reality! ⏰
────────────────────────────────────
```

## 🎭 Roast Intensity Levels

- **Light** 🟢: Gentle, encouraging tone with friendly humor
- **Medium** 🟡: Direct reality check with balanced humor and concern  
- **Brutal** 🔴: Savage, no-holds-barred roasting with harsh truths

## 📱 Supported Apps

- Instagram (Social Media)
- TikTok (Short Video)
- YouTube (Video Streaming)
- Twitter (Social Media)
- Reddit (Social Forum)
- Facebook (Social Media)
- WhatsApp (Messaging)
- Netflix (Entertainment)
- Snapchat (Social Media)
- Spotify (Music Streaming)

## 🧠 How It Works

1. **Data Processing**: Cleans data, engineers features (day_of_week, usage_category, app_category)
2. **Model Training**: Uses Random Forest Regressor to predict usage_minutes based on user patterns
3. **Prediction**: Takes user context and predicts their likely screen time
4. **Roast Generation**: Creates personalized prompts based on app, usage, category, and intensity
5. **API Integration**: Sends prompts to Gemini API for final roast generation (when API key provided)

## 📈 Model Performance

- **R² Score**: ~0.85+ (explains 85%+ of usage variance)
- **Mean Absolute Error**: ~15-25 minutes
- **Accuracy within 30 minutes**: ~80-90%
- **Cross-validation**: Consistent performance across different data splits

## 🔧 Configuration

The system supports various configuration options:

- **Model Type**: Random Forest (default) or Linear Regression
- **Roast Categories**: social_life, career, health, finance, laziness, productivity
- **Intensity Levels**: light, medium, brutal
- **Cultural Context**: Hinglish integration, Indian cultural references

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 Future Enhancements

- [ ] Real-time data collection from actual devices
- [ ] Web dashboard for user analytics
- [ ] Mobile app integration
- [ ] Advanced ML models (Neural Networks, XGBoost)
- [ ] Multi-language support
- [ ] User feedback and improvement system
- [ ] Social features and challenges
- [ ] Integration with digital wellness platforms

## 🙏 Acknowledgments

- **Gemini API** for AI-powered content generation
- **scikit-learn** for machine learning capabilities
- **pandas** for data processing
- The open-source community for inspiration and tools

## 📞 Contact

- **GitHub**: [@vannu07](https://github.com/vannu07)
- **Project Link**: [https://github.com/vannu07/ML_Screen_roaster](https://github.com/vannu07/ML_Screen_roaster)

---

**Made with ❤️ and a lot of ☕ for digital wellness awareness**