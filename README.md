# 🔥 Screen Time Roast Analyzer

A comprehensive, production-ready Python system that analyzes user screen time data and generates dynamic, personalized roasts using machine learning and the Gemini API.

## 🎯 Project Overview

This project creates an intelligent system that:
- Analyzes user screen time patterns across different apps
- Predicts future usage behavior using machine learning
- Generates personalized, humorous roasts in Hinglish (Hindi-English mix)
- Provides detailed insights into digital consumption habits

## 📁 Project Structure

```
ML_Screen_roaster/
├── src/                          # Source code
│   ├── data/                     # Data processing modules
│   │   ├── data_loader.py        # Data loading utilities
│   │   └── data_processor.py     # Data cleaning and feature engineering
│   ├── models/                   # Machine learning modules
│   │   ├── predictor.py          # ML model training and prediction
│   │   └── evaluator.py          # Model evaluation and analysis
│   ├── roast/                    # Roast generation modules
│   │   ├── generator.py          # Roast prompt generation
│   │   └── gemini_client.py      # Gemini API integration
│   ├── utils/                    # Utility modules
│   │   ├── config.py             # Configuration management
│   │   ├── logger.py             # Logging utilities
│   │   └── validators.py         # Data validation
│   └── main.py                   # Main application entry point
├── tests/                        # Test suite
│   ├── test_data_processor.py    # Data processing tests
│   └── test_roast_generator.py   # Roast generation tests
├── scripts/                      # Utility scripts
│   ├── run_analysis.py           # Main analysis runner
│   └── setup_environment.py      # Environment setup
├── data/                         # Data files
│   └── sample_roast_data.csv     # Sample dataset
├── docs/                         # Documentation
├── output/                       # Analysis results (created at runtime)
├── logs/                         # Log files (created at runtime)
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or download the project**
2. **Set up the environment:**
   ```bash
   python scripts/setup_environment.py
   ```

3. **Or install manually:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Analysis

**Option 1: Using the runner script (Recommended)**
```bash
python scripts/run_analysis.py
```

**Option 2: Using the main module**
```bash
python src/main.py
```

**Option 3: With custom options**
```bash
python scripts/run_analysis.py --num-users 10 --save-results --api-key YOUR_API_KEY
```

## 📊 Features

### ✅ Complete Data Pipeline
- **Data Loading**: Robust CSV loading with validation
- **Data Cleaning**: Missing value handling, outlier detection
- **Feature Engineering**: Time-based features, usage categories
- **Data Validation**: Comprehensive input validation

### ✅ Machine Learning System
- **Models**: Decision Tree and Random Forest regressors
- **Features**: One-hot encoded categorical variables
- **Evaluation**: MAE, R², RMSE, cross-validation
- **Analysis**: Feature importance, learning curves

### ✅ Intelligent Roast Generation
- **Multi-Intensity**: Light, Medium, Brutal roasting levels
- **App-Specific**: Contextual humor for each app
- **Category-Focused**: Health, career, social life themes
- **Cultural**: Hinglish language with Indian references

### ✅ Production-Ready Architecture
- **Modular Design**: Clean separation of concerns
- **Configuration**: Centralized config management
- **Logging**: Comprehensive logging system
- **Testing**: Unit tests for core functionality
- **Documentation**: Extensive inline documentation

## 🎭 Roast System

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

### Sample Roasts

**Instagram - Brutal (Finance)**
> "Bhai, itna time Instagram pe? 📱 Dusron ki perfect life dekhte dekhte apni life hi bhool gaye! Paisa kamane ke bajaye paisa waste karne mein expert ho gaye ho! 💸"

**TikTok - Light (Laziness)**
> "Arre yaar, 4 ghante TikTok pe? 🕺 Itne mein toh dance class join kar lete! But chill hai, Saturday hai, thoda entertainment toh banta hai! 😄"

## 🤖 Machine Learning

### Model Performance
- **Algorithm**: Decision Tree Regressor
- **Accuracy**: ~64% (R² score)
- **Error**: ~40 minutes MAE
- **Features**: App type, roast intensity, day of week

### Key Insights
- **Top Apps**: Instagram (270 min avg), TikTok (260 min avg)
- **Usage Patterns**: Higher usage on weekends
- **Prediction Accuracy**: Good for most app categories

## 🔧 Configuration

The system is highly configurable through `src/utils/config.py`:

```python
# Model settings
model.test_size = 0.2
model.max_depth = 10

# Roast settings
roast.intensity_instructions = {...}
roast.app_contexts = {...}

# API settings
gemini.model_name = 'gemini-pro'
gemini.temperature = 0.7
```

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

Run specific tests:
```bash
python -m pytest tests/test_data_processor.py -v
```

## 📈 Usage Examples

### Basic Analysis
```python
from src.main import ScreenTimeRoastAnalyzer

analyzer = ScreenTimeRoastAnalyzer()
results = analyzer.run_complete_analysis(num_demo_users=5)
```

### Custom Data
```python
analyzer = ScreenTimeRoastAnalyzer(data_file="your_data.csv")
results = analyzer.run_complete_analysis()
```

### With Gemini API
```python
analyzer = ScreenTimeRoastAnalyzer(gemini_api_key="your_api_key")
results = analyzer.run_complete_analysis()
```

## 🔑 Gemini API Setup

1. **Get API Key**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Install Client**: `pip install google-generativeai`
3. **Set Environment Variable**: 
   ```bash
   export GEMINI_API_KEY=your_api_key_here
   ```
4. **Or pass directly**:
   ```bash
   python scripts/run_analysis.py --api-key your_api_key_here
   ```

## 📊 Data Schema

Your CSV data should have these columns:

| Column | Type | Description |
|--------|------|-------------|
| `userId` | String | Unique user identifier |
| `app_name` | String | Application name |
| `usage_minutes` | Integer | Screen time in minutes |
| `roast_intensity` | String | light/medium/brutal |
| `roast_category_1` | String | Primary category |
| `date` | String | Date (YYYY-MM-DD) |

## 🚀 Advanced Usage

### Command Line Options
```bash
python scripts/run_analysis.py \
  --data-file data/custom_data.csv \
  --num-users 10 \
  --save-results \
  --output-dir results \
  --api-key YOUR_API_KEY \
  --verbose
```

### Programmatic Usage
```python
from src.data.data_loader import DataLoader
from src.models.predictor import UsagePredictor
from src.roast.generator import RoastGenerator

# Load data
loader = DataLoader()
data = loader.load_sample_data()

# Train model
predictor = UsagePredictor()
# ... training code

# Generate roasts
generator = RoastGenerator()
prompt = generator.generate_roast_prompt(...)
```

## 🔮 Future Enhancements

### Immediate (Week 1-2)
- [ ] Web interface (FastAPI/Streamlit)
- [ ] Real-time data integration
- [ ] User authentication system
- [ ] Database storage (PostgreSQL)

### Short-term (Month 1-2)
- [ ] Mobile app (React Native/Flutter)
- [ ] Advanced ML models (XGBoost, Neural Networks)
- [ ] Social sharing features
- [ ] Multi-language support

### Long-term (Month 3-6)
- [ ] Enterprise B2B solutions
- [ ] Gamification elements
- [ ] AI-powered improvement suggestions
- [ ] International expansion

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 📞 Support

- **Issues**: Create an issue in the repository
- **Documentation**: Check the `docs/` directory
- **Examples**: See `scripts/` for usage examples

## 🎉 Acknowledgments

- **Gemini API**: Google's generative AI platform
- **scikit-learn**: Machine learning library
- **pandas**: Data manipulation and analysis
- **Community**: Open source contributors

---

**Made with ❤️ for digital wellness and humor!** 🚀

*Transform screen time awareness into entertainment with ML-powered personalized roasts!*