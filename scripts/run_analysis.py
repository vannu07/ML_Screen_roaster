#!/usr/bin/env python3
"""
Script to run the complete Screen Time Roast Analysis.
This is the main entry point for running the analysis.
"""

import os
import sys
import argparse
from datetime import datetime

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import ScreenTimeRoastAnalyzer
from utils.config import config
from utils.logger import setup_logger


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Screen Time Roast Analyzer - ML-powered screen time analysis and roast generation'
    )
    
    parser.add_argument(
        '--data-file', '-d',
        type=str,
        help='Path to the CSV data file (uses sample data if not provided)'
    )
    
    parser.add_argument(
        '--api-key', '-k',
        type=str,
        help='Gemini API key (can also be set via GEMINI_API_KEY environment variable)'
    )
    
    parser.add_argument(
        '--num-users', '-n',
        type=int,
        default=5,
        help='Number of users to demonstrate roast generation (default: 5)'
    )
    
    parser.add_argument(
        '--output-dir', '-o',
        type=str,
        default='output',
        help='Output directory for results (default: output)'
    )
    
    parser.add_argument(
        '--save-results', '-s',
        action='store_true',
        help='Save analysis results to file'
    )
    
    parser.add_argument(
        '--log-file', '-l',
        type=str,
        help='Path to log file (optional)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--model-type', '-m',
        type=str,
        choices=['decision_tree', 'random_forest'],
        default='decision_tree',
        help='Type of ML model to use (default: decision_tree)'
    )
    
    return parser.parse_args()


def setup_output_directory(output_dir: str) -> str:
    """Set up output directory with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_output_dir = os.path.join(output_dir, f"analysis_{timestamp}")
    os.makedirs(full_output_dir, exist_ok=True)
    return full_output_dir


def main():
    """Main function."""
    print("🚀 SCREEN TIME ROAST ANALYZER")
    print("=" * 60)
    print("ML-powered screen time analysis and roast generation system")
    print("=" * 60)
    
    # Parse arguments
    args = parse_arguments()
    
    # Setup logging
    if args.log_file:
        setup_logger(log_file=args.log_file, level='DEBUG' if args.verbose else 'INFO')
    
    # Setup output directory
    if args.save_results:
        output_dir = setup_output_directory(args.output_dir)
        print(f"📁 Output directory: {output_dir}")
    
    try:
        # Initialize analyzer
        print("🔧 Initializing analyzer...")
        analyzer = ScreenTimeRoastAnalyzer(
            data_file=args.data_file,
            gemini_api_key=args.api_key
        )
        
        # Display configuration
        print(f"📊 Configuration:")
        print(f"   • Data file: {args.data_file or 'Sample data'}")
        print(f"   • Demo users: {args.num_users}")
        print(f"   • Model type: {args.model_type}")
        print(f"   • Gemini API: {'Configured' if args.api_key else 'Simulated'}")
        print(f"   • Save results: {args.save_results}")
        
        # Run analysis
        print(f"\n🚀 Starting analysis...")
        results = analyzer.run_complete_analysis(num_demo_users=args.num_users)
        
        # Save results if requested
        if args.save_results:
            results_file = os.path.join(output_dir, "analysis_results.json")
            success = analyzer.save_results(results_file, results)
            
            if success:
                print(f"💾 Results saved to: {results_file}")
            
            # Save model if trained
            if analyzer.predictor.is_trained:
                model_file = os.path.join(output_dir, "trained_model.joblib")
                analyzer.predictor.save_model(model_file)
                print(f"🤖 Model saved to: {model_file}")
        
        # Display summary
        print(f"\n📈 ANALYSIS SUMMARY")
        print(f"=" * 40)
        
        status = analyzer.get_system_status()
        print(f"✅ Records processed: {status['total_records']}")
        print(f"🎭 Roasts generated: {results.get('total_processed', 0)}")
        
        if status['model_performance']:
            perf = status['model_performance']
            print(f"🎯 Model accuracy (R²): {perf.get('test_r2', 0):.3f}")
            print(f"📊 Prediction error (MAE): {perf.get('test_mae', 0):.1f} minutes")
        
        print(f"\n🎉 Analysis completed successfully!")
        
        # Next steps
        print(f"\n🔗 NEXT STEPS:")
        if not args.api_key:
            print("   1. Get Gemini API key from: https://makersuite.google.com/app/apikey")
            print("   2. Set GEMINI_API_KEY environment variable")
            print("   3. Re-run with --api-key parameter for real roasts")
        else:
            print("   1. Deploy as web application")
            print("   2. Integrate with real-time data collection")
            print("   3. Set up automated roast delivery system")
        
        return 0
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Analysis interrupted by user")
        return 1
        
    except Exception as e:
        print(f"\n❌ Analysis failed: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())