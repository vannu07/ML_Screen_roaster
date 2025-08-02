# 🔥 Screen Time Roast Analyzer

A comprehensive Python system that analyzes user screen time data and generates dynamic, personalized roasts using machine learning and the Gemini API.

## 🎯 Project Overview

This project creates an intelligent system that:
- Analyzes user screen time patterns across different apps
- Predicts future usage behavior using machine learning
- Generates personalized, humorous roasts in Hinglish (Hindi-English mix)
- Provides detailed insights into digital consumption habits

## 📊 Features

### 1. Data Analysis & Cleaning
- ✅ Loads and processes CSV data with user screen time information
- ✅ Handles missing values intelligently
- ✅ Performs feature engineering (day of week extraction)
- ✅ Comprehensive data validation

### 2. Exploratory Data Analysis (EDA)
- ✅ Top app usage statistics
- ✅ Average usage patterns by app
- ✅ Roast intensity preference distribution
- ✅ Interactive visualizations with matplotlib/seaborn
- ✅ Detailed insights and trends

### 3. Machine Learning Model
- ✅ Decision Tree Regressor for usage prediction
- ✅ One-hot encoding for categorical features
- ✅ Train/test split with proper validation
- ✅ Model performance metrics (MAE, R², RMSE)
- ✅ Feature importance analysis

### 4. Intelligent Roast Generation
- ✅ Context-aware prompt generation for Gemini API
- ✅ Multi-intensity roasting (Light, Medium, Brutal)
- ✅ App-specific humor and references
- ✅ Category-focused roasting (health, career, social_life, etc.)
- ✅ Hinglish language style for Indian users

### 5. Complete Simulation System
- ✅ End-to-end user processing pipeline
- ✅ Real-time prediction and roast generation
- ✅ Demonstration on sample users
- ✅ Production-ready architecture

## 🚀 Quick Start

### Prerequisites
```bash
Python 3.8+
pip (Python package manager)
```

### Installation
1. Clone or download the project files
2. Install required dependencies:
```bash
pip install -r requirements.txt
```

### Running the Analysis
```bash
python screen_time_roast_analyzer.py
```

## 📁 Project Structure

```
ML_Screen_roaster/
├── screen_time_roast_analyzer.py  # Main analysis script
├── sample_roast_data.csv          # Sample user data
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

## 📈 Data Schema

The system expects CSV data with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `userId` | String | Unique user identifier |
| `fcmToken` | String | Firebase Cloud Messaging token |
| `roast_category_1` | String | Primary roast category (health, career, etc.) |
| `roast_category_2` | String | Secondary roast category (can be empty) |
| `roast_intensity` | String | Roast intensity level (light, medium, brutal) |
| `date` | String | Usage date (YYYY-MM-DD format) |
| `app_name` | String | Application name (Instagram, TikTok, etc.) |
| `usage_minutes` | Integer | Screen time in minutes |

## 🤖 Machine Learning Model

### Features Used
- **roast_intensity**: User's preferred roast intensity
- **app_name**: Application being used
- **day_of_week**: Day of the week (derived from date)

### Model Performance
- **Algorithm**: Decision Tree Regressor
- **MAE**: ~40 minutes (varies with data)
- **R² Score**: ~0.64 (varies with data)
- **Features**: One-hot encoded categorical variables

## 🎭 Roast Generation System

### Intensity Levels

#### 🟢 Light
- Playful and gentle teasing
- Friendly humor between friends
- Makes users smile rather than cringe

#### 🟡 Medium  
- Witty and clever with balanced humor
- Good reality check with entertainment
- Includes sass but stays fun

#### 🔴 Brutal
- Savage humor without holding back
- Ruthlessly funny and hilariously harsh
- Maximum entertainment value

### App-Specific Context
- **Instagram**: Endless scrolling, curated lives, food photos
- **TikTok**: Short-form video addiction, dance trends
- **YouTube**: Video rabbit holes, procrastination
- **Twitter**: Hot takes, social media drama
- **Reddit**: Deep community dives, comment threads

### Category Focus Areas
- **Health**: Physical and mental well-being impact
- **Career**: Productivity and professional goals
- **Social Life**: Real-world relationships and social skills
- **Finance**: Opportunity cost and money-making potential
- **Laziness**: Procrastination and responsibility avoidance

## 📊 Sample Output

```
🎯 USER 1: user_087
📱 App: Reddit
⏱️  Actual Usage: 85 minutes
🔮 Predicted Usage: 150 minutes
🔥 Roast Intensity: BRUTAL
🎯 Roast Category: health
📅 Day: Tuesday

🤖 GENERATED GEMINI API PROMPT:
Generate a brutal intensity, witty, and funny roast in Hinglish 
for a user predicted to spend 2 hours and 29 minutes on Reddit...
```

## 🔧 Customization

### Adding New Apps
Update the `app_contexts` dictionary in the `generate_roast_prompt` method:

```python
app_contexts = {
    'YourApp': "description of app-specific behavior",
    # ... existing apps
}
```

### Adding New Categories
Update the `category_focus` dictionary:

```python
category_focus = {
    'your_category': "focus area description",
    # ... existing categories
}
```

### Modifying Roast Intensity
Update the `intensity_instructions` dictionary:

```python
intensity_instructions = {
    'your_intensity': "instruction for this intensity level",
    # ... existing intensities
}
```

## 🔮 Future Enhancements

### Immediate Next Steps
- [ ] Integrate actual Gemini API calls
- [ ] Add user authentication system
- [ ] Implement real-time data collection
- [ ] Create web interface

### Advanced Features
- [ ] Multi-language support beyond Hinglish
- [ ] Advanced ML models (Random Forest, XGBoost)
- [ ] Real-time usage tracking
- [ ] Social sharing of roasts
- [ ] Personalized improvement suggestions
- [ ] Gamification elements

### Technical Improvements
- [ ] Database integration (PostgreSQL/MongoDB)
- [ ] API endpoint creation (FastAPI/Flask)
- [ ] Docker containerization
- [ ] Cloud deployment (AWS/GCP)
- [ ] Monitoring and logging
- [ ] A/B testing framework

## 🛠️ Development

### Code Structure
The main class `ScreenTimeRoastAnalyzer` follows a modular approach:

1. **Data Processing**: `load_and_prepare_data()`
2. **Analysis**: `exploratory_data_analysis()`
3. **Modeling**: `prepare_modeling_data()`, `build_and_train_model()`
4. **Roast Generation**: `generate_roast_prompt()`
5. **Simulation**: `run_roast_simulation()`, `demonstrate_roast_system()`

### Testing
To test with your own data:
1. Replace `sample_roast_data.csv` with your data file
2. Ensure your CSV follows the required schema
3. Run the script: `python screen_time_roast_analyzer.py`

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For questions or support, please create an issue in the project repository.

---

**Made with ❤️ for digital wellness and humor!** 🚀