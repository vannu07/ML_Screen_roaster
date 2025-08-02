#!/usr/bin/env python3
"""
Simulation Module for Screen Time Roast Analyzer
Main script to run the entire pipeline and simulate the user experience.
"""

import pandas as pd
import numpy as np
import logging
from typing import Dict, List, Tuple
import os
import sys

# Add src to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data_processor import DataProcessor
from model_trainer import ModelTrainer
from prompt_generator import generate_roast_prompt

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ScreenTimeSimulator:
    """Main simulator class that orchestrates the entire pipeline."""
    
    def __init__(self, data_path: str = "data/sample_roast_data.csv"):
        """
        Initialize the simulator.
        
        Args:
            data_path: Path to the data file
        """
        self.data_path = data_path
        self.processor = DataProcessor()
        self.trainer = ModelTrainer()
        self.processed_data = None
        self.trained_model = None
        
    def run_complete_pipeline(self) -> Dict:
        """
        Run the complete ML pipeline from data loading to model training.
        
        Returns:
            Dictionary with pipeline results
        """
        logger.info("🚀 Starting complete Screen Time Roast Analyzer pipeline...")
        
        # Step 1: Load and process data
        logger.info("📊 Step 1: Loading and processing data...")
        self.processed_data, data_insights = self.processor.process_complete(self.data_path)
        
        # Step 2: Train model
        logger.info("🤖 Step 2: Training ML model...")
        training_results = self.trainer.train_model(self.processed_data, model_type='random_forest')
        
        # Step 3: Evaluate model
        logger.info("📈 Step 3: Evaluating model performance...")
        evaluation_results = self.trainer.evaluate_model(self.processed_data)
        
        pipeline_results = {
            'data_insights': data_insights,
            'training_results': training_results,
            'evaluation_results': evaluation_results,
            'pipeline_status': 'completed'
        }
        
        logger.info("✅ Complete pipeline finished successfully!")
        return pipeline_results
    
    def simulate_user_experience(self, num_samples: int = 5) -> List[Dict]:
        """
        Simulate the user experience with sample users.
        
        Args:
            num_samples: Number of sample users to simulate
            
        Returns:
            List of simulation results
        """
        if self.processed_data is None:
            raise ValueError("Pipeline not run yet. Call run_complete_pipeline() first.")
        
        logger.info(f"🎭 Simulating user experience with {num_samples} sample users...")
        
        # Select random sample users
        sample_users = self.processed_data.sample(n=min(num_samples, len(self.processed_data)))
        
        simulation_results = []
        
        for idx, (_, user_data) in enumerate(sample_users.iterrows(), 1):
            logger.info(f"👤 Processing User {idx}...")
            
            # Extract user information
            user_info = {
                'user_id': user_data.get('userId', f'user_{idx}'),
                'app_name': user_data.get('app_name', 'Unknown'),
                'actual_usage': user_data.get('usage_minutes', 0),
                'roast_category': user_data.get('roast_category_1', 'productivity'),
                'roast_intensity': user_data.get('roast_intensity', 'medium'),
                'day_of_week': user_data.get('day_of_week', 'Monday')
            }
            
            # Make prediction
            user_df = pd.DataFrame([user_data])
            predicted_usage = self.trainer.predict_usage(user_df)[0]
            
            # Generate roast prompt
            roast_prompt = generate_roast_prompt(
                app_name=user_info['app_name'],
                predicted_usage=predicted_usage,
                roast_category=user_info['roast_category'],
                roast_intensity=user_info['roast_intensity']
            )
            
            # Compile results
            result = {
                'user_info': user_info,
                'predicted_usage': predicted_usage,
                'prediction_accuracy': abs(user_info['actual_usage'] - predicted_usage),
                'roast_prompt': roast_prompt
            }
            
            simulation_results.append(result)
            
            # Display results
            self._display_user_simulation(idx, result)
        
        logger.info("✅ User experience simulation completed!")
        return simulation_results
    
    def _display_user_simulation(self, user_num: int, result: Dict) -> None:
        """
        Display simulation results for a single user.
        
        Args:
            user_num: User number
            result: Simulation result dictionary
        """
        user_info = result['user_info']
        predicted = result['predicted_usage']
        actual = user_info['actual_usage']
        accuracy = result['prediction_accuracy']
        
        print(f"\n{'='*60}")
        print(f"👤 USER {user_num} SIMULATION RESULTS")
        print(f"{'='*60}")
        
        print(f"📱 App: {user_info['app_name']}")
        print(f"🆔 User ID: {user_info['user_id']}")
        print(f"📅 Day: {user_info['day_of_week']}")
        print(f"🎯 Roast Category: {user_info['roast_category']}")
        print(f"🔥 Roast Intensity: {user_info['roast_intensity']}")
        
        print(f"\n📊 USAGE PREDICTION:")
        print(f"   Actual Usage: {actual:.0f} minutes ({actual/60:.1f} hours)")
        print(f"   Predicted Usage: {predicted:.0f} minutes ({predicted/60:.1f} hours)")
        print(f"   Prediction Error: {accuracy:.0f} minutes")
        
        accuracy_percentage = (1 - accuracy / max(actual, predicted)) * 100
        print(f"   Accuracy: {max(0, accuracy_percentage):.1f}%")
        
        print(f"\n🎭 GENERATED ROAST PROMPT:")
        print(f"{'─'*60}")
        print(result['roast_prompt'])
        print(f"{'─'*60}")
    
    def generate_summary_report(self, pipeline_results: Dict, simulation_results: List[Dict]) -> None:
        """
        Generate a comprehensive summary report.
        
        Args:
            pipeline_results: Results from the ML pipeline
            simulation_results: Results from user simulations
        """
        print(f"\n{'='*80}")
        print("📋 SCREEN TIME ROAST ANALYZER - COMPREHENSIVE REPORT")
        print(f"{'='*80}")
        
        # Data Overview
        data_insights = pipeline_results['data_insights']
        print(f"\n📊 DATA OVERVIEW:")
        print(f"   Total Users: {data_insights['user_stats']['total_users']}")
        print(f"   Total Sessions: {data_insights['user_stats']['total_sessions']}")
        print(f"   Unique Apps: {data_insights['user_stats']['unique_apps']}")
        print(f"   Average Usage: {data_insights['user_stats']['avg_usage_minutes']:.1f} minutes")
        print(f"   Total Usage Hours: {data_insights['user_stats']['total_usage_hours']:.1f} hours")
        
        # Model Performance
        training_results = pipeline_results['training_results']
        evaluation_results = pipeline_results['evaluation_results']
        
        print(f"\n🤖 MODEL PERFORMANCE:")
        print(f"   Model Type: {training_results['model_type']}")
        print(f"   R² Score: {training_results['test_r2']:.3f}")
        print(f"   Mean Absolute Error: {training_results['test_mae']:.1f} minutes")
        print(f"   Cross-Validation R²: {training_results['cv_mean_r2']:.3f} ± {training_results['cv_std_r2']:.3f}")
        print(f"   Accuracy within 30min: {evaluation_results['accuracy_within_30min']:.1%}")
        
        # Top Apps Analysis
        app_insights = data_insights['app_insights']
        print(f"\n📱 TOP APPS BY AVERAGE USAGE:")
        sorted_apps = sorted(app_insights.items(), key=lambda x: x[1]['avg_usage'], reverse=True)
        for i, (app, stats) in enumerate(sorted_apps[:5], 1):
            print(f"   {i}. {app}: {stats['avg_usage']:.1f} min avg ({stats['sessions']} sessions)")
        
        # Simulation Summary
        if simulation_results:
            avg_accuracy = np.mean([r['prediction_accuracy'] for r in simulation_results])
            print(f"\n🎭 SIMULATION SUMMARY:")
            print(f"   Simulated Users: {len(simulation_results)}")
            print(f"   Average Prediction Error: {avg_accuracy:.1f} minutes")
            
            # Most common apps in simulation
            sim_apps = [r['user_info']['app_name'] for r in simulation_results]
            unique_apps = list(set(sim_apps))
            print(f"   Apps Simulated: {', '.join(unique_apps)}")
        
        print(f"\n🎯 SYSTEM CAPABILITIES:")
        print(f"   ✅ Data Processing & Feature Engineering")
        print(f"   ✅ ML Model Training & Evaluation")
        print(f"   ✅ Usage Prediction")
        print(f"   ✅ Dynamic Roast Prompt Generation")
        print(f"   ✅ Multi-intensity Roasting (Light/Medium/Brutal)")
        print(f"   ✅ App-specific Context Awareness")
        print(f"   ✅ Cultural Adaptation (Hinglish)")
        
        print(f"\n🚀 READY FOR:")
        print(f"   🔗 Gemini API Integration")
        print(f"   📱 Mobile App Deployment")
        print(f"   🌐 Web Interface")
        print(f"   📊 Real-time Analytics")
        print(f"   🎯 Personalized Interventions")


def main():
    """Main function to run the complete simulation."""
    print("🔥 SCREEN TIME ROAST ANALYZER - SIMULATION")
    print("=" * 60)
    print("🎯 Complete ML Pipeline + User Experience Simulation")
    print("=" * 60)
    
    try:
        # Initialize simulator
        simulator = ScreenTimeSimulator()
        
        # Run complete pipeline
        pipeline_results = simulator.run_complete_pipeline()
        
        # Simulate user experience
        simulation_results = simulator.simulate_user_experience(num_samples=3)
        
        # Generate comprehensive report
        simulator.generate_summary_report(pipeline_results, simulation_results)
        
        print(f"\n{'='*80}")
        print("🎉 SIMULATION COMPLETED SUCCESSFULLY!")
        print("🔗 Next Steps:")
        print("   1. Get Gemini API key for real roast generation")
        print("   2. Deploy to web/mobile platform")
        print("   3. Add real-time data collection")
        print("   4. Implement user feedback system")
        print("=" * 80)
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Simulation failed: {str(e)}")
        return 1


if __name__ == "__main__":
    exit(main())