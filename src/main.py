#!/usr/bin/env python3
"""
Main application file for Screen Time Roast Analyzer.
This is the entry point for the complete analysis pipeline.
"""

import os
import sys
from typing import Optional

# Add src to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from data.data_loader import DataLoader
from data.data_processor import DataProcessor
from models.predictor import UsagePredictor
from models.evaluator import ModelEvaluator
from roast.generator import RoastGenerator
from roast.gemini_client import GeminiClient
from utils.config import config
from utils.logger import analysis_logger, setup_logger


class ScreenTimeRoastAnalyzer:
    """
    Main application class that orchestrates the complete analysis pipeline.
    """
    
    def __init__(self, data_file: Optional[str] = None, gemini_api_key: Optional[str] = None):
        """
        Initialize the Screen Time Roast Analyzer.
        
        Args:
            data_file: Path to the data file (optional, uses sample data if not provided)
            gemini_api_key: Gemini API key (optional)
        """
        self.data_file = data_file
        self.gemini_api_key = gemini_api_key
        
        # Initialize components
        self.data_loader = DataLoader()
        self.data_processor = DataProcessor()
        self.predictor = UsagePredictor()
        self.evaluator = ModelEvaluator()
        self.roast_generator = RoastGenerator()
        self.gemini_client = GeminiClient(gemini_api_key)
        
        # Data storage
        self.raw_data = None
        self.processed_data = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
        analysis_logger.success("Screen Time Roast Analyzer initialized")
    
    def run_complete_analysis(self, num_demo_users: int = 5) -> dict:
        """
        Run the complete analysis pipeline.
        
        Args:
            num_demo_users: Number of users to demonstrate roast generation
            
        Returns:
            Dictionary with analysis results
        """
        analysis_logger.step(0, "STARTING COMPLETE SCREEN TIME ROAST ANALYSIS")
        
        try:
            # Step 1: Load data
            self._load_data()
            
            # Step 2: Process data
            self._process_data()
            
            # Step 3: Train model
            self._train_model()
            
            # Step 4: Evaluate model
            self._evaluate_model()
            
            # Step 5: Generate roasts
            results = self._demonstrate_roast_system(num_demo_users)
            
            analysis_logger.step(6, "ANALYSIS COMPLETED SUCCESSFULLY")
            return results
            
        except Exception as e:
            analysis_logger.error(f"Analysis failed: {str(e)}")
            raise
    
    def _load_data(self) -> None:
        """Load and validate data."""
        analysis_logger.step(1, "LOADING AND VALIDATING DATA")
        
        if self.data_file:
            self.raw_data = self.data_loader.load_csv(self.data_file)
        else:
            self.raw_data = self.data_loader.load_sample_data()
        
        if self.raw_data is None:
            raise ValueError("Failed to load data")
        
        # Log data information
        data_info = self.data_loader.get_data_info()
        analysis_logger.success(f"Loaded {data_info['shape'][0]} records with {data_info['shape'][1]} columns")
        analysis_logger.info(f"Unique users: {data_info['unique_users']}")
        analysis_logger.info(f"Date range: {data_info['date_range']}")
    
    def _process_data(self) -> None:
        """Process and clean the data."""
        self.processed_data = self.data_processor.process_data(self.raw_data)
        
        # Get insights
        insights = self.data_processor.get_data_insights()
        analysis_logger.section("Data Insights")
        analysis_logger.info(f"Most active day: {insights.get('most_active_day', 'N/A')}")
        
        if 'top_apps_by_usage' in insights:
            top_app = list(insights['top_apps_by_usage'].keys())[0]
            analysis_logger.info(f"Top app by usage: {top_app}")
    
    def _train_model(self) -> None:
        """Train the machine learning model."""
        # Prepare features
        X, y = self.data_processor.prepare_modeling_features()
        
        # Prepare data for modeling
        self.predictor.prepare_data(X, y)
        
        # Train model
        self.predictor.train_model('decision_tree')
        
        # Store data for evaluation
        self.X_train = self.predictor.X_train
        self.X_test = self.predictor.X_test
        self.y_train = self.predictor.y_train
        self.y_test = self.predictor.y_test
    
    def _evaluate_model(self) -> None:
        """Evaluate the trained model."""
        analysis_logger.step(4, "MODEL EVALUATION AND ANALYSIS")
        
        # Make predictions
        y_pred_train = self.predictor.predict(self.X_train)
        y_pred_test = self.predictor.predict(self.X_test)
        
        # Evaluate predictions
        train_metrics = self.evaluator.evaluate_predictions(self.y_train, y_pred_train, "training")
        test_metrics = self.evaluator.evaluate_predictions(self.y_test, y_pred_test, "test")
        
        # Cross-validation
        cv_results = self.evaluator.cross_validate_model(self.predictor.pipeline, 
                                                        self.X_train, self.y_train)
        
        # Feature importance analysis
        if self.predictor.feature_names is not None:
            importance_df = self.evaluator.analyze_feature_importance(
                self.predictor.pipeline, self.predictor.feature_names
            )
        
        # Generate plots
        self.evaluator.plot_prediction_analysis(self.y_test, y_pred_test, "Test Set Analysis")
        self.evaluator.plot_learning_curves(self.predictor.pipeline, self.X_train, self.y_train)
    
    def _demonstrate_roast_system(self, num_users: int) -> dict:
        """Demonstrate the roast generation system."""
        analysis_logger.step(5, "ROAST GENERATION DEMONSTRATION")
        
        # Get sample users
        sample_users = self.data_loader.get_sample_users(num_users)
        
        if sample_users is None:
            raise ValueError("No sample users available")
        
        results = []
        
        for i, (_, user_data) in enumerate(sample_users.iterrows()):
            analysis_logger.progress(f"Processing user {i+1}/{num_users}")
            
            try:
                # Prepare user features for prediction
                user_features = {
                    'roast_intensity': user_data['roast_intensity'],
                    'app_name': user_data['app_name'],
                    'day_of_week': user_data.get('day_of_week', 'Monday')
                }
                
                # Make prediction
                predicted_usage = self.predictor.predict_single_user(user_features)
                
                # Generate roast prompt
                roast_prompt = self.roast_generator.generate_roast_prompt(
                    app_name=user_data['app_name'],
                    predicted_usage=predicted_usage,
                    roast_category=user_data['roast_category_1'],
                    roast_intensity=user_data['roast_intensity'],
                    user_context={
                        'day_of_week': user_data.get('day_of_week'),
                        'is_weekend': user_data.get('is_weekend', False)
                    }
                )
                
                # Generate actual roast
                actual_roast = self.gemini_client.generate_roast(roast_prompt)
                
                # Store result
                result = {
                    'user_id': user_data['userId'],
                    'app_name': user_data['app_name'],
                    'actual_usage': user_data['usage_minutes'],
                    'predicted_usage': predicted_usage,
                    'roast_intensity': user_data['roast_intensity'],
                    'roast_category': user_data['roast_category_1'],
                    'day_of_week': user_data.get('day_of_week', 'N/A'),
                    'roast_prompt': roast_prompt,
                    'generated_roast': actual_roast
                }
                
                results.append(result)
                
                # Display result
                self._display_roast_result(result, i+1)
                
            except Exception as e:
                analysis_logger.error(f"Error processing user {user_data['userId']}: {str(e)}")
                continue
        
        analysis_logger.success(f"Generated roasts for {len(results)} users")
        return {'roast_results': results, 'total_processed': len(results)}
    
    def _display_roast_result(self, result: dict, user_number: int) -> None:
        """Display a single roast result."""
        print(f"\n{'='*50}")
        print(f"🎯 USER {user_number}: {result['user_id']}")
        print(f"{'='*50}")
        print(f"📱 App: {result['app_name']}")
        print(f"⏱️  Actual Usage: {result['actual_usage']} minutes")
        print(f"🔮 Predicted Usage: {result['predicted_usage']:.0f} minutes")
        print(f"🔥 Roast Intensity: {result['roast_intensity'].upper()}")
        print(f"🎯 Roast Category: {result['roast_category']}")
        print(f"📅 Day: {result['day_of_week']}")
        
        print(f"\n🎭 GENERATED ROAST:")
        print(f"{'-'*50}")
        print(f"💬 {result['generated_roast']}")
        print(f"{'-'*50}")
    
    def save_results(self, output_file: str, results: dict) -> bool:
        """
        Save analysis results to file.
        
        Args:
            output_file: Path to output file
            results: Results dictionary to save
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import json
            
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_file), exist_ok=True)
            
            # Add model summary to results
            results['model_summary'] = self.predictor.get_model_summary()
            results['data_insights'] = self.data_processor.get_data_insights()
            
            # Save to JSON
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False, default=str)
            
            analysis_logger.success(f"Results saved to: {output_file}")
            return True
            
        except Exception as e:
            analysis_logger.error(f"Failed to save results: {str(e)}")
            return False
    
    def get_system_status(self) -> dict:
        """Get the status of all system components."""
        return {
            'data_loaded': self.raw_data is not None,
            'data_processed': self.processed_data is not None,
            'model_trained': self.predictor.is_trained,
            'gemini_configured': self.gemini_client.is_configured,
            'total_records': len(self.processed_data) if self.processed_data is not None else 0,
            'model_performance': self.predictor.model_metrics if self.predictor.is_trained else {}
        }


def main():
    """Main function to run the complete analysis."""
    print("🚀 STARTING SCREEN TIME ROAST ANALYZER")
    print("=" * 60)
    
    try:
        # Initialize analyzer
        analyzer = ScreenTimeRoastAnalyzer()
        
        # Run complete analysis
        results = analyzer.run_complete_analysis(num_demo_users=5)
        
        # Save results if configured
        if config.save_results:
            output_file = os.path.join("output", "analysis_results.json")
            analyzer.save_results(output_file, results)
        
        # Display system status
        status = analyzer.get_system_status()
        print(f"\n{'='*60}")
        print("📊 SYSTEM STATUS")
        print(f"{'='*60}")
        print(f"✅ Data Loaded: {status['data_loaded']}")
        print(f"✅ Data Processed: {status['data_processed']}")
        print(f"✅ Model Trained: {status['model_trained']}")
        print(f"🤖 Gemini Configured: {status['gemini_configured']}")
        print(f"📈 Total Records: {status['total_records']}")
        
        if status['model_performance']:
            print(f"🎯 Model R² Score: {status['model_performance'].get('test_r2', 0):.3f}")
            print(f"📊 Model MAE: {status['model_performance'].get('test_mae', 0):.2f} minutes")
        
        print(f"\n🎉 ANALYSIS COMPLETED SUCCESSFULLY!")
        print("🔗 Next steps:")
        print("   1. Get Gemini API key for real roast generation")
        print("   2. Deploy as web application")
        print("   3. Integrate with real-time data collection")
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())