#!/usr/bin/env python3
"""
Top 10 Apps Analysis Runner
Focused analysis on the most popular mobile applications only.
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data.data_loader import DataLoader
from data.data_processor import DataProcessor
from analysis.top_apps_analyzer import TopAppsAnalyzer
from utils.logger import analysis_logger, setup_logger


def main():
    """Run focused top 10 apps analysis."""
    print("🔥 TOP 10 APPS ANALYSIS - SCREEN TIME ROAST ANALYZER")
    print("=" * 70)
    print("Focused analysis on the most popular mobile applications")
    print("=" * 70)
    
    try:
        # Initialize components
        data_loader = DataLoader()
        data_processor = DataProcessor()
        apps_analyzer = TopAppsAnalyzer()
        
        # Load data
        analysis_logger.step(1, "LOADING DATA")
        raw_data = data_loader.load_sample_data()
        
        if raw_data is None:
            raise ValueError("Failed to load data")
        
        # Process data
        analysis_logger.step(2, "PROCESSING DATA")
        processed_data = data_processor.process_data(raw_data)
        
        # Run top apps analysis
        analysis_logger.step(3, "ANALYZING TOP 10 APPS")
        results = apps_analyzer.analyze_top_apps(processed_data)
        
        # Display comprehensive results
        display_results(results, apps_analyzer)
        
        # Generate individual app reports
        generate_individual_reports(apps_analyzer)
        
        print(f"\n{'='*70}")
        print("🎉 TOP 10 APPS ANALYSIS COMPLETED SUCCESSFULLY!")
        print("📊 Check the visualizations and detailed insights above")
        print("🔗 Next: Use insights for targeted roast generation")
        print("=" * 70)
        
        return 0
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        return 1


def display_results(results: dict, analyzer: TopAppsAnalyzer):
    """Display comprehensive analysis results."""
    
    print(f"\n{'='*70}")
    print("📊 TOP 10 APPS ANALYSIS RESULTS")
    print("=" * 70)
    
    # App Usage Statistics
    print(f"\n📱 APP USAGE STATISTICS")
    print("-" * 50)
    
    usage_stats = results['app_usage_stats']
    for app, stats in usage_stats.items():
        print(f"\n🎯 {app.upper()} ({stats['category']})")
        print(f"   • Average Usage: {stats['avg_usage_minutes']:.1f} minutes")
        print(f"   • Total Sessions: {stats['total_sessions']:,}")
        print(f"   • Unique Users: {stats['unique_users']:,}")
        print(f"   • Total Hours: {stats['total_usage_hours']:.1f} hours")
        print(f"   • Usage Range: {stats['min_usage_minutes']:.0f}-{stats['max_usage_minutes']:.0f} minutes")
        
        # Usage distribution
        dist = stats['usage_distribution']
        print(f"   • User Types: Light({dist['light_users']}) | Moderate({dist['moderate_users']}) | Heavy({dist['heavy_users']})")
    
    # Category Analysis
    print(f"\n📂 CATEGORY ANALYSIS")
    print("-" * 50)
    
    category_stats = results['category_analysis']
    for category, stats in category_stats.items():
        print(f"\n📁 {category.upper()}")
        print(f"   • Apps: {', '.join(stats['apps_list'])}")
        print(f"   • Average Usage: {stats['avg_usage_minutes']:.1f} minutes")
        print(f"   • Total Sessions: {stats['total_sessions']:,}")
        print(f"   • Preferred Intensity: {stats['user_preference']}")
    
    # App Rankings
    print(f"\n🏆 APP RANKINGS")
    print("-" * 50)
    
    rankings = results['app_rankings']
    
    print("\n🥇 BY AVERAGE USAGE:")
    for i, (app, metrics) in enumerate(rankings['by_avg_usage'][:5], 1):
        print(f"   {i}. {app}: {metrics['avg_usage']:.1f} minutes")
    
    print("\n📊 BY TOTAL USAGE:")
    for i, (app, metrics) in enumerate(rankings['by_total_usage'][:5], 1):
        print(f"   {i}. {app}: {metrics['total_usage']:.0f} total minutes")
    
    print("\n👥 BY USER COUNT:")
    for i, (app, metrics) in enumerate(rankings['by_user_count'][:5], 1):
        print(f"   {i}. {app}: {metrics['user_count']} users")
    
    # Global Comparison
    print(f"\n🌍 GLOBAL VS LOCAL COMPARISON")
    print("-" * 50)
    
    comparison = results['comparative_analysis']
    for app, comp in comparison.items():
        status = "🔴 ABOVE" if comp['usage_level'] == 'above' else "🟢 BELOW" if comp['usage_level'] == 'below' else "🟡 EQUAL"
        print(f"\n{app}:")
        print(f"   • Local: {comp['local_average']:.1f} min | Global: {comp['global_average']} min")
        print(f"   • Difference: {comp['difference_minutes']:+.1f} min ({comp['percentage_difference']:+.1f}%) {status}")
    
    # User Behavior Insights
    print(f"\n👥 USER BEHAVIOR INSIGHTS")
    print("-" * 50)
    
    behavior = results['user_behavior']
    
    print(f"\n📱 Multi-App Usage:")
    print(f"   • Single-app users: {behavior['multi_app_usage']['single_app_users']}")
    print(f"   • Multi-app users: {behavior['multi_app_usage']['multi_app_users']}")
    print(f"   • Average apps per user: {behavior['multi_app_usage']['avg_apps_per_user']:.1f}")
    
    print(f"\n⏱️ Usage Intensity:")
    print(f"   • Light users (≤2h): {behavior['usage_intensity']['light_users']}")
    print(f"   • Moderate users (2-6h): {behavior['usage_intensity']['moderate_users']}")
    print(f"   • Heavy users (>6h): {behavior['usage_intensity']['heavy_users']}")
    print(f"   • Average daily usage: {behavior['usage_intensity']['avg_daily_usage']:.1f} minutes")
    
    # Key Insights
    print(f"\n💡 KEY INSIGHTS")
    print("-" * 50)
    
    insights = results['insights_summary']
    
    if insights['most_addictive_app']:
        app_info = insights['most_addictive_app']
        print(f"\n🎯 Most Addictive App: {app_info['app']} ({app_info['avg_minutes']:.1f} min avg)")
    
    if insights['most_popular_category']:
        cat_info = insights['most_popular_category']
        print(f"📂 Most Popular Category: {cat_info['category']} ({cat_info['count']} sessions)")
    
    if insights['peak_usage_day']:
        day_info = insights['peak_usage_day']
        print(f"📅 Peak Usage Day: {day_info['day']} ({day_info['avg_minutes']:.1f} min avg)")
    
    # Recommendations
    if insights['recommendations']:
        print(f"\n🔗 RECOMMENDATIONS:")
        for i, rec in enumerate(insights['recommendations'], 1):
            print(f"   {i}. {rec}")


def generate_individual_reports(analyzer: TopAppsAnalyzer):
    """Generate detailed reports for individual apps."""
    
    print(f"\n{'='*70}")
    print("📋 INDIVIDUAL APP REPORTS")
    print("=" * 70)
    
    available_apps = analyzer.top_apps_data['app_name'].unique()
    
    for app in available_apps[:3]:  # Show top 3 detailed reports
        print(f"\n📱 DETAILED REPORT: {app.upper()}")
        print("-" * 50)
        
        report = analyzer.generate_app_report(app)
        
        if 'error' in report:
            print(f"❌ {report['error']}")
            continue
        
        # Basic info
        print(f"Category: {report['category']}")
        
        # Usage statistics
        stats = report['usage_statistics']
        print(f"\n📊 Usage Statistics:")
        print(f"   • Total Sessions: {stats['total_sessions']:,}")
        print(f"   • Unique Users: {stats['unique_users']:,}")
        print(f"   • Average Usage: {stats['avg_usage_minutes']:.1f} minutes")
        print(f"   • Median Usage: {stats['median_usage_minutes']:.1f} minutes")
        print(f"   • Total Hours: {stats['total_usage_hours']:.1f} hours")
        print(f"   • Usage Range: {stats['usage_range']}")
        
        # User preferences
        prefs = report['user_preferences']
        print(f"\n🎭 User Preferences:")
        print(f"   • Most Preferred Roast: {prefs['most_preferred_intensity']}")
        print(f"   • Intensity Distribution: {prefs['roast_intensity_distribution']}")
        
        # Time patterns
        if report['time_patterns']:
            patterns = report['time_patterns']
            print(f"\n📅 Time Patterns:")
            print(f"   • Peak Day: {patterns['peak_day']} ({patterns['peak_usage']:.1f} min)")
        
        # Global comparison
        if report['global_comparison']:
            comp = report['global_comparison']
            print(f"\n🌍 Global Comparison:")
            print(f"   • Local Average: {comp['local_average']:.1f} minutes")
            print(f"   • Global Average: {comp['global_average']} minutes")
            print(f"   • Difference: {comp['difference']:+.1f} minutes ({comp['percentage_difference']:+.1f}%)")


if __name__ == "__main__":
    exit(main())