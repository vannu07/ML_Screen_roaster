#!/usr/bin/env python3
"""
Screen Time Roast Analyzer
A complete Python script to analyze user screen time data and build a system 
for generating dynamic, personalized roasts using the Gemini API.

Author: AI/ML Engineer
Date: 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import mean_absolute_error
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import warnings
warnings.filterwarnings('ignore')

# Set style for better visualizations
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class ScreenTimeRoastAnalyzer:
    """
    A comprehensive class for analyzing screen time data and generating roast prompts.
    """
    
    def __init__(self, csv_file_path):
        """
        Initialize the analyzer with the CSV file path.
        
        Args:
            csv_file_path (str): Path to the CSV file containing user data
        """
        self.csv_file_path = csv_file_path
        self.df = None
        self.model = None
        self.preprocessor = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def load_and_prepare_data(self):
        """
        Step 1: Load and prepare the data with cleaning and feature engineering.
        """
        print("=" * 60)
        print("STEP 1: LOADING AND PREPARING DATA")
        print("=" * 60)
        
        # Load the CSV file
        self.df = pd.read_csv(self.csv_file_path)
        print(f"✓ Loaded data with shape: {self.df.shape}")
        print(f"✓ Columns: {list(self.df.columns)}")
        
        # Data cleaning
        print("\n📊 Data Cleaning:")
        print(f"Missing values before cleaning:\n{self.df.isnull().sum()}")
        
        # Fill missing values in roast_category_2 with 'None'
        self.df['roast_category_2'] = self.df['roast_category_2'].fillna('None')
        print("✓ Filled missing values in 'roast_category_2' with 'None'")
        
        # Convert date column to datetime
        self.df['date'] = pd.to_datetime(self.df['date'])
        print("✓ Converted 'date' column to datetime format")
        
        # Feature engineering
        print("\n🔧 Feature Engineering:")
        # Create day_of_week column
        self.df['day_of_week'] = self.df['date'].dt.day_name()
        print("✓ Created 'day_of_week' column from date")
        
        print(f"\n✓ Final data shape: {self.df.shape}")
        print(f"✓ Missing values after cleaning:\n{self.df.isnull().sum()}")
        
        # Display first few rows
        print("\n📋 First 5 rows of cleaned data:")
        print(self.df.head())
        
    def exploratory_data_analysis(self):
        """
        Step 2: Perform exploratory data analysis and generate insights.
        """
        print("\n" + "=" * 60)
        print("STEP 2: EXPLORATORY DATA ANALYSIS")
        print("=" * 60)
        
        # Top 5 most used apps
        print("\n📱 Top 5 Most Used Apps:")
        top_apps = self.df['app_name'].value_counts().head()
        print(top_apps)
        
        # Average usage minutes for each app
        print("\n⏱️ Average Usage Minutes for Each App:")
        avg_usage = self.df.groupby('app_name')['usage_minutes'].mean().sort_values(ascending=False)
        print(avg_usage.round(2))
        
        # Distribution of roast intensity preferences
        print("\n🔥 Distribution of Roast Intensity Preferences:")
        intensity_dist = self.df['roast_intensity'].value_counts()
        print(intensity_dist)
        print(f"Percentages:\n{(intensity_dist / len(self.df) * 100).round(2)}%")
        
        # Create visualization: Bar chart of total usage minutes for each app
        print("\n📊 Creating visualization...")
        plt.figure(figsize=(12, 8))
        
        # Calculate total usage minutes for each app
        app_usage = self.df.groupby('app_name')['usage_minutes'].sum().sort_values(ascending=True)
        
        # Create horizontal bar chart
        bars = plt.barh(app_usage.index, app_usage.values, color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7'])
        
        # Customize the plot
        plt.title('Total Usage Minutes by App', fontsize=16, fontweight='bold', pad=20)
        plt.xlabel('Total Usage Minutes', fontsize=12)
        plt.ylabel('App Name', fontsize=12)
        
        # Add value labels on bars
        for bar in bars:
            width = bar.get_width()
            plt.text(width + 50, bar.get_y() + bar.get_height()/2, 
                    f'{int(width):,}', ha='left', va='center', fontweight='bold')
        
        plt.grid(axis='x', alpha=0.3)
        plt.tight_layout()
        plt.show()
        
        # Additional insights
        print("\n📈 Additional Insights:")
        print(f"• Total users in dataset: {self.df['userId'].nunique()}")
        print(f"• Date range: {self.df['date'].min().date()} to {self.df['date'].max().date()}")
        print(f"• Average usage per session: {self.df['usage_minutes'].mean():.2f} minutes")
        print(f"• Most common day: {self.df['day_of_week'].mode()[0]}")
        print(f"• Most common roast category: {self.df['roast_category_1'].mode()[0]}")
        
    def prepare_modeling_data(self):
        """
        Prepare data for machine learning modeling.
        """
        print("\n" + "=" * 60)
        print("STEP 3: PREPARING DATA FOR MODELING")
        print("=" * 60)
        
        # Select features for modeling
        feature_columns = ['roast_intensity', 'app_name', 'day_of_week']
        target_column = 'usage_minutes'
        
        X = self.df[feature_columns]
        y = self.df[target_column]
        
        print(f"✓ Selected features: {feature_columns}")
        print(f"✓ Target variable: {target_column}")
        print(f"✓ Feature matrix shape: {X.shape}")
        print(f"✓ Target vector shape: {y.shape}")
        
        # Split the data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print(f"✓ Training set size: {self.X_train.shape[0]} samples")
        print(f"✓ Test set size: {self.X_test.shape[0]} samples")
        
        # Create preprocessor for one-hot encoding
        self.preprocessor = ColumnTransformer(
            transformers=[
                ('cat', OneHotEncoder(drop='first', sparse_output=False), feature_columns)
            ]
        )
        
        print("✓ Created one-hot encoder for categorical features")
        
    def build_and_train_model(self):
        """
        Step 3: Build and train the Decision Tree Regressor model.
        """
        print("\n🤖 BUILDING AND TRAINING MODEL")
        print("-" * 40)
        
        # Create pipeline with preprocessor and model
        self.model = Pipeline([
            ('preprocessor', self.preprocessor),
            ('regressor', DecisionTreeRegressor(random_state=42, max_depth=10))
        ])
        
        # Train the model
        print("🔄 Training Decision Tree Regressor...")
        self.model.fit(self.X_train, self.y_train)
        print("✓ Model training completed!")
        
        # Make predictions
        y_pred = self.model.predict(self.X_test)
        
        # Calculate and print MAE
        mae = mean_absolute_error(self.y_test, y_pred)
        print(f"📊 Model Performance:")
        print(f"   Mean Absolute Error (MAE): {mae:.2f} minutes")
        
        # Additional metrics
        from sklearn.metrics import r2_score, mean_squared_error
        r2 = r2_score(self.y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(self.y_test, y_pred))
        
        print(f"   R² Score: {r2:.3f}")
        print(f"   Root Mean Squared Error (RMSE): {rmse:.2f} minutes")
        
        # Feature importance (after preprocessing)
        feature_names = self.model.named_steps['preprocessor'].get_feature_names_out()
        importances = self.model.named_steps['regressor'].feature_importances_
        
        print(f"\n🎯 Top 5 Most Important Features:")
        feature_importance = list(zip(feature_names, importances))
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        
        for i, (feature, importance) in enumerate(feature_importance[:5]):
            print(f"   {i+1}. {feature}: {importance:.3f}")
    
    def generate_roast_prompt(self, app_name, predicted_usage, roast_category, roast_intensity):
        """
        Step 4: Generate a detailed, context-aware prompt for the Gemini API.
        
        Args:
            app_name (str): Name of the app
            predicted_usage (float): Predicted usage minutes
            roast_category (str): Category for roasting (e.g., 'health', 'career')
            roast_intensity (str): Intensity level ('light', 'medium', 'brutal')
            
        Returns:
            str: Formatted prompt for Gemini API
        """
        
        # Convert predicted usage to hours and minutes for better readability
        hours = int(predicted_usage // 60)
        minutes = int(predicted_usage % 60)
        
        if hours > 0:
            time_str = f"{hours} hour{'s' if hours != 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''}"
        else:
            time_str = f"{minutes} minute{'s' if minutes != 1 else ''}"
        
        # Create intensity-specific instructions
        intensity_instructions = {
            'light': "Keep it playful and gentle, like a friendly tease between friends. Use humor that makes them smile rather than cringe.",
            'medium': "Make it witty and clever with a good balance of humor and reality check. Include some sass but keep it entertaining.",
            'brutal': "Go all out with savage humor! Be ruthlessly funny and don't hold back. Make it hilariously harsh but still entertaining."
        }
        
        # Create app-specific context
        app_contexts = {
            'Instagram': "their endless scrolling through perfectly curated lives and food photos",
            'TikTok': "their addiction to short-form videos and dance trends",
            'YouTube': "their rabbit hole of random videos and procrastination",
            'Twitter': "their obsession with hot takes and social media drama",
            'Reddit': "their deep dives into random communities and endless comment threads"
        }
        
        app_context = app_contexts.get(app_name, f"their {app_name} usage habits")
        
        # Create category-specific focus areas
        category_focus = {
            'health': "how this screen time is affecting their physical and mental well-being",
            'career': "how this is impacting their productivity and professional goals",
            'social_life': "how this is affecting their real-world relationships and social skills",
            'finance': "the opportunity cost and how they could be making money instead",
            'laziness': "their procrastination habits and avoidance of responsibilities",
            'None': "their general screen time habits and digital lifestyle"
        }
        
        focus_area = category_focus.get(roast_category, "their screen time habits")
        
        # Construct the detailed prompt
        prompt = f"""Generate a {roast_intensity} intensity, witty, and funny roast in Hinglish (Hindi-English mix) for a user who is predicted to spend {time_str} on {app_name}.

ROAST REQUIREMENTS:
- Intensity Level: {roast_intensity.upper()} - {intensity_instructions[roast_intensity]}
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

        return prompt
    
    def run_roast_simulation(self, user_data):
        """
        Step 5: Main simulation function that processes a single user and generates roast.
        
        Args:
            user_data (pd.Series): A single row of user data
            
        Returns:
            dict: Dictionary containing user info, prediction, and generated prompt
        """
        
        # Extract user information
        user_id = user_data['userId']
        app_name = user_data['app_name']
        actual_usage = user_data['usage_minutes']
        roast_intensity = user_data['roast_intensity']
        roast_category = user_data['roast_category_1']
        day_of_week = user_data['day_of_week']
        
        # Prepare data for prediction
        user_features = pd.DataFrame({
            'roast_intensity': [roast_intensity],
            'app_name': [app_name],
            'day_of_week': [day_of_week]
        })
        
        # Make prediction
        predicted_usage = self.model.predict(user_features)[0]
        
        # Generate roast prompt
        roast_prompt = self.generate_roast_prompt(
            app_name=app_name,
            predicted_usage=predicted_usage,
            roast_category=roast_category,
            roast_intensity=roast_intensity
        )
        
        return {
            'user_id': user_id,
            'app_name': app_name,
            'actual_usage': actual_usage,
            'predicted_usage': predicted_usage,
            'roast_intensity': roast_intensity,
            'roast_category': roast_category,
            'day_of_week': day_of_week,
            'roast_prompt': roast_prompt
        }
    
    def demonstrate_roast_system(self, num_users=5):
        """
        Demonstrate the roast system on the first N users from the dataset.
        
        Args:
            num_users (int): Number of users to demonstrate on
        """
        print("\n" + "=" * 60)
        print("STEP 5: ROAST SYSTEM DEMONSTRATION")
        print("=" * 60)
        
        print(f"🎭 Running roast simulation on first {num_users} users...\n")
        
        for i in range(min(num_users, len(self.df))):
            user_data = self.df.iloc[i]
            result = self.run_roast_simulation(user_data)
            
            print(f"{'='*50}")
            print(f"🎯 USER {i+1}: {result['user_id']}")
            print(f"{'='*50}")
            print(f"📱 App: {result['app_name']}")
            print(f"⏱️  Actual Usage: {result['actual_usage']} minutes")
            print(f"🔮 Predicted Usage: {result['predicted_usage']:.0f} minutes")
            print(f"🔥 Roast Intensity: {result['roast_intensity'].upper()}")
            print(f"🎯 Roast Category: {result['roast_category']}")
            print(f"📅 Day: {result['day_of_week']}")
            
            print(f"\n🤖 GENERATED GEMINI API PROMPT:")
            print(f"{'-'*50}")
            print(result['roast_prompt'])
            print(f"{'-'*50}")
            
            print(f"\n💡 In a real application, this prompt would be sent to the Gemini API")
            print(f"   to generate the actual roast response for the user.\n")
    
    def run_complete_analysis(self):
        """
        Run the complete analysis pipeline.
        """
        print("🚀 STARTING COMPLETE SCREEN TIME ROAST ANALYSIS")
        print("=" * 60)
        
        try:
            # Step 1: Load and prepare data
            self.load_and_prepare_data()
            
            # Step 2: Exploratory Data Analysis
            self.exploratory_data_analysis()
            
            # Step 3: Prepare data and build model
            self.prepare_modeling_data()
            self.build_and_train_model()
            
            # Step 4 & 5: Demonstrate roast system
            self.demonstrate_roast_system(num_users=5)
            
            print("\n" + "=" * 60)
            print("✅ ANALYSIS COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print("🎉 The Screen Time Roast Analyzer is ready for production!")
            print("🔗 Next steps: Integrate with actual Gemini API for live roast generation")
            
        except Exception as e:
            print(f"\n❌ Error occurred during analysis: {str(e)}")
            raise

def main():
    """
    Main function to run the complete screen time roast analysis.
    """
    # Initialize the analyzer
    csv_file_path = "sample_roast_data.csv"
    analyzer = ScreenTimeRoastAnalyzer(csv_file_path)
    
    # Run complete analysis
    analyzer.run_complete_analysis()

if __name__ == "__main__":
    main()