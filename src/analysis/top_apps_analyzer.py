#!/usr/bin/env python3
"""
Top 10 Apps Analysis for Screen Time Roast Analyzer.
Focused analysis on the most popular mobile applications.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional
from utils.config import config
from utils.logger import analysis_logger


class TopAppsAnalyzer:
    """Specialized analyzer for top 10 mobile applications."""
    
    def __init__(self, config_instance=None):
        """Initialize the top apps analyzer."""
        self.config = config_instance or config
        self.df = None
        self.top_apps_data = None
        self.app_insights = {}
        
        # Define top 10 most popular apps globally
        self.top_10_apps = [
            'Instagram', 'TikTok', 'YouTube', 'WhatsApp', 'Facebook',
            'Twitter', 'Snapchat', 'Reddit', 'Netflix', 'Spotify'
        ]
        
        # App categories for better analysis
        self.app_categories = {
            'Instagram': 'Social Media',
            'TikTok': 'Short Video',
            'YouTube': 'Video Streaming',
            'WhatsApp': 'Messaging',
            'Facebook': 'Social Media',
            'Twitter': 'Social Media',
            'Snapchat': 'Social Media',
            'Reddit': 'Social Forum',
            'Netflix': 'Entertainment',
            'Spotify': 'Music Streaming'
        }
        
        # Average global usage patterns (in minutes per day)
        self.global_averages = {
            'Instagram': 195,
            'TikTok': 168,
            'YouTube': 142,
            'WhatsApp': 85,
            'Facebook': 125,
            'Twitter': 95,
            'Snapchat': 110,
            'Reddit': 135,
            'Netflix': 180,
            'Spotify': 75
        }
    
    def analyze_top_apps(self, df: pd.DataFrame) -> Dict:
        """
        Comprehensive analysis of top 10 apps.
        
        Args:
            df: DataFrame with user data
            
        Returns:
            Dictionary with comprehensive app analysis
        """
        analysis_logger.step(1, "TOP 10 APPS COMPREHENSIVE ANALYSIS")
        
        self.df = df.copy()
        
        # Filter for top 10 apps only
        self._filter_top_apps()
        
        # Perform comprehensive analysis
        results = {
            'app_usage_stats': self._analyze_usage_patterns(),
            'category_analysis': self._analyze_by_category(),
            'intensity_preferences': self._analyze_roast_intensity(),
            'time_patterns': self._analyze_time_patterns(),
            'user_behavior': self._analyze_user_behavior(),
            'comparative_analysis': self._compare_with_global_averages(),
            'app_rankings': self._rank_apps(),
            'insights_summary': self._generate_insights()
        }
        
        # Generate visualizations
        self._create_visualizations()
        
        analysis_logger.success("Top 10 apps analysis completed")
        return results
    
    def _filter_top_apps(self) -> None:
        """Filter data to include only top 10 apps."""
        available_apps = self.df['app_name'].unique()
        
        # Find which top 10 apps are in our data
        apps_in_data = [app for app in self.top_10_apps if app in available_apps]
        
        if not apps_in_data:
            analysis_logger.warning("No top 10 apps found in data, using all available apps")
            apps_in_data = list(available_apps)[:10]
        
        # Filter data
        self.top_apps_data = self.df[self.df['app_name'].isin(apps_in_data)].copy()
        
        analysis_logger.info(f"Analyzing {len(apps_in_data)} apps: {', '.join(apps_in_data)}")
        analysis_logger.info(f"Filtered data shape: {self.top_apps_data.shape}")
    
    def _analyze_usage_patterns(self) -> Dict:
        """Analyze usage patterns for each app."""
        analysis_logger.section("App Usage Patterns Analysis")
        
        usage_stats = {}
        
        for app in self.top_apps_data['app_name'].unique():
            app_data = self.top_apps_data[self.top_apps_data['app_name'] == app]
            
            stats = {
                'total_sessions': len(app_data),
                'unique_users': app_data['userId'].nunique(),
                'avg_usage_minutes': app_data['usage_minutes'].mean(),
                'median_usage_minutes': app_data['usage_minutes'].median(),
                'max_usage_minutes': app_data['usage_minutes'].max(),
                'min_usage_minutes': app_data['usage_minutes'].min(),
                'std_usage_minutes': app_data['usage_minutes'].std(),
                'total_usage_hours': app_data['usage_minutes'].sum() / 60,
                'category': self.app_categories.get(app, 'Other'),
                'usage_distribution': {
                    'light_users': len(app_data[app_data['usage_minutes'] <= 60]),
                    'moderate_users': len(app_data[(app_data['usage_minutes'] > 60) & (app_data['usage_minutes'] <= 180)]),
                    'heavy_users': len(app_data[app_data['usage_minutes'] > 180])
                }
            }
            
            usage_stats[app] = stats
            
            # Log key insights
            analysis_logger.info(f"📱 {app}:")
            analysis_logger.info(f"   • Average usage: {stats['avg_usage_minutes']:.1f} minutes")
            analysis_logger.info(f"   • Total sessions: {stats['total_sessions']}")
            analysis_logger.info(f"   • Unique users: {stats['unique_users']}")
            analysis_logger.info(f"   • Category: {stats['category']}")
        
        return usage_stats
    
    def _analyze_by_category(self) -> Dict:
        """Analyze apps by category."""
        analysis_logger.section("Category-wise Analysis")
        
        # Add category column
        self.top_apps_data['category'] = self.top_apps_data['app_name'].map(self.app_categories)
        
        category_stats = {}
        
        for category in self.top_apps_data['category'].unique():
            if pd.isna(category):
                continue
                
            cat_data = self.top_apps_data[self.top_apps_data['category'] == category]
            
            stats = {
                'apps_count': cat_data['app_name'].nunique(),
                'apps_list': list(cat_data['app_name'].unique()),
                'total_sessions': len(cat_data),
                'avg_usage_minutes': cat_data['usage_minutes'].mean(),
                'total_usage_hours': cat_data['usage_minutes'].sum() / 60,
                'user_preference': cat_data['roast_intensity'].mode()[0] if len(cat_data) > 0 else 'medium'
            }
            
            category_stats[category] = stats
            
            analysis_logger.info(f"📂 {category}:")
            analysis_logger.info(f"   • Apps: {', '.join(stats['apps_list'])}")
            analysis_logger.info(f"   • Average usage: {stats['avg_usage_minutes']:.1f} minutes")
            analysis_logger.info(f"   • Total sessions: {stats['total_sessions']}")
        
        return category_stats
    
    def _analyze_roast_intensity(self) -> Dict:
        """Analyze roast intensity preferences by app."""
        analysis_logger.section("Roast Intensity Preferences by App")
        
        intensity_stats = {}
        
        for app in self.top_apps_data['app_name'].unique():
            app_data = self.top_apps_data[self.top_apps_data['app_name'] == app]
            
            intensity_dist = app_data['roast_intensity'].value_counts()
            intensity_pct = (intensity_dist / len(app_data) * 100).round(1)
            
            stats = {
                'most_preferred': intensity_dist.index[0] if len(intensity_dist) > 0 else 'medium',
                'distribution': intensity_dist.to_dict(),
                'percentages': intensity_pct.to_dict(),
                'total_users': len(app_data)
            }
            
            intensity_stats[app] = stats
            
            analysis_logger.info(f"🔥 {app} - Most preferred: {stats['most_preferred']}")
            for intensity, pct in stats['percentages'].items():
                analysis_logger.info(f"   • {intensity}: {pct}%")
        
        return intensity_stats
    
    def _analyze_time_patterns(self) -> Dict:
        """Analyze usage patterns by time."""
        analysis_logger.section("Time-based Usage Patterns")
        
        if 'day_of_week' not in self.top_apps_data.columns:
            self.top_apps_data['day_of_week'] = pd.to_datetime(self.top_apps_data['date']).dt.day_name()
        
        time_stats = {}
        
        # Day of week analysis
        for app in self.top_apps_data['app_name'].unique():
            app_data = self.top_apps_data[self.top_apps_data['app_name'] == app]
            
            day_usage = app_data.groupby('day_of_week')['usage_minutes'].agg(['mean', 'count']).round(1)
            
            stats = {
                'peak_day': day_usage['mean'].idxmax(),
                'peak_day_avg': day_usage['mean'].max(),
                'lowest_day': day_usage['mean'].idxmin(),
                'lowest_day_avg': day_usage['mean'].min(),
                'daily_averages': day_usage['mean'].to_dict(),
                'daily_sessions': day_usage['count'].to_dict()
            }
            
            time_stats[app] = stats
            
            analysis_logger.info(f"📅 {app}:")
            analysis_logger.info(f"   • Peak day: {stats['peak_day']} ({stats['peak_day_avg']:.1f} min)")
            analysis_logger.info(f"   • Lowest day: {stats['lowest_day']} ({stats['lowest_day_avg']:.1f} min)")
        
        return time_stats
    
    def _analyze_user_behavior(self) -> Dict:
        """Analyze user behavior patterns."""
        analysis_logger.section("User Behavior Analysis")
        
        behavior_stats = {}
        
        # Multi-app users
        user_app_counts = self.top_apps_data.groupby('userId')['app_name'].nunique()
        
        behavior_stats['multi_app_usage'] = {
            'single_app_users': (user_app_counts == 1).sum(),
            'multi_app_users': (user_app_counts > 1).sum(),
            'avg_apps_per_user': user_app_counts.mean(),
            'max_apps_per_user': user_app_counts.max()
        }
        
        # Usage intensity by user
        user_total_usage = self.top_apps_data.groupby('userId')['usage_minutes'].sum()
        
        behavior_stats['usage_intensity'] = {
            'light_users': (user_total_usage <= 120).sum(),  # <= 2 hours
            'moderate_users': ((user_total_usage > 120) & (user_total_usage <= 360)).sum(),  # 2-6 hours
            'heavy_users': (user_total_usage > 360).sum(),  # > 6 hours
            'avg_daily_usage': user_total_usage.mean(),
            'max_daily_usage': user_total_usage.max()
        }
        
        # App switching patterns
        user_sessions = self.top_apps_data.groupby('userId').size()
        behavior_stats['session_patterns'] = {
            'avg_sessions_per_user': user_sessions.mean(),
            'max_sessions_per_user': user_sessions.max(),
            'single_session_users': (user_sessions == 1).sum(),
            'multi_session_users': (user_sessions > 1).sum()
        }
        
        analysis_logger.info("👥 User Behavior Insights:")
        analysis_logger.info(f"   • Multi-app users: {behavior_stats['multi_app_usage']['multi_app_users']}")
        analysis_logger.info(f"   • Average apps per user: {behavior_stats['multi_app_usage']['avg_apps_per_user']:.1f}")
        analysis_logger.info(f"   • Heavy users (>6h): {behavior_stats['usage_intensity']['heavy_users']}")
        analysis_logger.info(f"   • Average daily usage: {behavior_stats['usage_intensity']['avg_daily_usage']:.1f} min")
        
        return behavior_stats
    
    def _compare_with_global_averages(self) -> Dict:
        """Compare local usage with global averages."""
        analysis_logger.section("Global vs Local Usage Comparison")
        
        comparison = {}
        
        for app in self.top_apps_data['app_name'].unique():
            if app in self.global_averages:
                app_data = self.top_apps_data[self.top_apps_data['app_name'] == app]
                local_avg = app_data['usage_minutes'].mean()
                global_avg = self.global_averages[app]
                
                difference = local_avg - global_avg
                percentage_diff = (difference / global_avg) * 100
                
                comparison[app] = {
                    'local_average': local_avg,
                    'global_average': global_avg,
                    'difference_minutes': difference,
                    'percentage_difference': percentage_diff,
                    'usage_level': 'above' if difference > 0 else 'below' if difference < 0 else 'equal'
                }
                
                analysis_logger.info(f"🌍 {app}:")
                analysis_logger.info(f"   • Local: {local_avg:.1f} min | Global: {global_avg} min")
                analysis_logger.info(f"   • Difference: {difference:+.1f} min ({percentage_diff:+.1f}%)")
        
        return comparison
    
    def _rank_apps(self) -> Dict:
        """Rank apps by various metrics."""
        analysis_logger.section("App Rankings")
        
        app_metrics = {}
        
        for app in self.top_apps_data['app_name'].unique():
            app_data = self.top_apps_data[self.top_apps_data['app_name'] == app]
            
            app_metrics[app] = {
                'avg_usage': app_data['usage_minutes'].mean(),
                'total_usage': app_data['usage_minutes'].sum(),
                'user_count': app_data['userId'].nunique(),
                'session_count': len(app_data),
                'engagement_score': app_data['usage_minutes'].mean() * app_data['userId'].nunique()
            }
        
        rankings = {
            'by_avg_usage': sorted(app_metrics.items(), key=lambda x: x[1]['avg_usage'], reverse=True),
            'by_total_usage': sorted(app_metrics.items(), key=lambda x: x[1]['total_usage'], reverse=True),
            'by_user_count': sorted(app_metrics.items(), key=lambda x: x[1]['user_count'], reverse=True),
            'by_engagement': sorted(app_metrics.items(), key=lambda x: x[1]['engagement_score'], reverse=True)
        }
        
        analysis_logger.info("🏆 App Rankings:")
        analysis_logger.info("   By Average Usage:")
        for i, (app, metrics) in enumerate(rankings['by_avg_usage'][:5], 1):
            analysis_logger.info(f"   {i}. {app}: {metrics['avg_usage']:.1f} min")
        
        return rankings
    
    def _generate_insights(self) -> Dict:
        """Generate key insights from the analysis."""
        analysis_logger.section("Key Insights Summary")
        
        insights = {
            'most_addictive_app': None,
            'most_popular_category': None,
            'peak_usage_day': None,
            'user_behavior_pattern': None,
            'roast_preferences': {},
            'recommendations': []
        }
        
        # Most addictive app (highest average usage)
        app_averages = self.top_apps_data.groupby('app_name')['usage_minutes'].mean()
        insights['most_addictive_app'] = {
            'app': app_averages.idxmax(),
            'avg_minutes': app_averages.max()
        }
        
        # Most popular category
        if 'category' in self.top_apps_data.columns:
            category_counts = self.top_apps_data['category'].value_counts()
            insights['most_popular_category'] = {
                'category': category_counts.index[0],
                'count': category_counts.iloc[0]
            }
        
        # Peak usage day
        if 'day_of_week' in self.top_apps_data.columns:
            day_usage = self.top_apps_data.groupby('day_of_week')['usage_minutes'].mean()
            insights['peak_usage_day'] = {
                'day': day_usage.idxmax(),
                'avg_minutes': day_usage.max()
            }
        
        # Generate recommendations
        insights['recommendations'] = self._generate_recommendations()
        
        # Log key insights
        analysis_logger.info("💡 Key Insights:")
        if insights['most_addictive_app']:
            analysis_logger.info(f"   • Most addictive: {insights['most_addictive_app']['app']} ({insights['most_addictive_app']['avg_minutes']:.1f} min)")
        if insights['most_popular_category']:
            analysis_logger.info(f"   • Most popular category: {insights['most_popular_category']['category']}")
        if insights['peak_usage_day']:
            analysis_logger.info(f"   • Peak usage day: {insights['peak_usage_day']['day']}")
        
        return insights
    
    def _generate_recommendations(self) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        # Analyze usage patterns for recommendations
        app_averages = self.top_apps_data.groupby('app_name')['usage_minutes'].mean()
        high_usage_apps = app_averages[app_averages > 180].index.tolist()
        
        if high_usage_apps:
            recommendations.append(f"Consider setting time limits for high-usage apps: {', '.join(high_usage_apps)}")
        
        # Category-based recommendations
        if 'category' in self.top_apps_data.columns:
            social_media_usage = self.top_apps_data[self.top_apps_data['category'] == 'Social Media']['usage_minutes'].sum()
            if social_media_usage > 300:  # More than 5 hours
                recommendations.append("High social media usage detected - consider digital detox periods")
        
        # Time-based recommendations
        if 'day_of_week' in self.top_apps_data.columns:
            weekend_usage = self.top_apps_data[self.top_apps_data['day_of_week'].isin(['Saturday', 'Sunday'])]['usage_minutes'].mean()
            weekday_usage = self.top_apps_data[~self.top_apps_data['day_of_week'].isin(['Saturday', 'Sunday'])]['usage_minutes'].mean()
            
            if weekend_usage > weekday_usage * 1.5:
                recommendations.append("Weekend usage is significantly higher - maintain consistent daily limits")
        
        return recommendations
    
    def _create_visualizations(self) -> None:
        """Create comprehensive visualizations."""
        if not self.config.visualization.show_plots:
            return
        
        analysis_logger.section("Creating Visualizations")
        
        # Set up the plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Create a comprehensive dashboard
        fig = plt.figure(figsize=(20, 16))
        
        # 1. App Usage Comparison (Top subplot)
        ax1 = plt.subplot(3, 3, (1, 3))
        app_usage = self.top_apps_data.groupby('app_name')['usage_minutes'].mean().sort_values(ascending=True)
        bars = ax1.barh(app_usage.index, app_usage.values, color=sns.color_palette("viridis", len(app_usage)))
        ax1.set_title('Average Usage Time by App', fontsize=16, fontweight='bold')
        ax1.set_xlabel('Average Usage (minutes)')
        
        # Add value labels
        for bar in bars:
            width = bar.get_width()
            ax1.text(width + 2, bar.get_y() + bar.get_height()/2, f'{width:.0f}', 
                    ha='left', va='center', fontweight='bold')
        
        # 2. Category Distribution (Middle left)
        ax2 = plt.subplot(3, 3, 4)
        if 'category' in self.top_apps_data.columns:
            category_counts = self.top_apps_data['category'].value_counts()
            ax2.pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%', startangle=90)
            ax2.set_title('App Categories Distribution', fontweight='bold')
        
        # 3. Roast Intensity Preferences (Middle center)
        ax3 = plt.subplot(3, 3, 5)
        intensity_counts = self.top_apps_data['roast_intensity'].value_counts()
        colors = ['lightgreen', 'orange', 'red']
        ax3.bar(intensity_counts.index, intensity_counts.values, color=colors)
        ax3.set_title('Roast Intensity Preferences', fontweight='bold')
        ax3.set_ylabel('Count')
        
        # 4. Daily Usage Patterns (Middle right)
        ax4 = plt.subplot(3, 3, 6)
        if 'day_of_week' in self.top_apps_data.columns:
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            day_usage = self.top_apps_data.groupby('day_of_week')['usage_minutes'].mean().reindex(day_order)
            ax4.plot(day_usage.index, day_usage.values, marker='o', linewidth=2, markersize=8)
            ax4.set_title('Average Usage by Day', fontweight='bold')
            ax4.set_ylabel('Average Usage (minutes)')
            ax4.tick_params(axis='x', rotation=45)
        
        # 5. Usage Distribution (Bottom left)
        ax5 = plt.subplot(3, 3, 7)
        ax5.hist(self.top_apps_data['usage_minutes'], bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        ax5.set_title('Usage Time Distribution', fontweight='bold')
        ax5.set_xlabel('Usage Minutes')
        ax5.set_ylabel('Frequency')
        
        # 6. App vs Global Comparison (Bottom center)
        ax6 = plt.subplot(3, 3, 8)
        apps_in_global = [app for app in self.top_apps_data['app_name'].unique() if app in self.global_averages]
        if apps_in_global:
            local_avgs = [self.top_apps_data[self.top_apps_data['app_name'] == app]['usage_minutes'].mean() for app in apps_in_global]
            global_avgs = [self.global_averages[app] for app in apps_in_global]
            
            x = np.arange(len(apps_in_global))
            width = 0.35
            
            ax6.bar(x - width/2, local_avgs, width, label='Local', alpha=0.8)
            ax6.bar(x + width/2, global_avgs, width, label='Global', alpha=0.8)
            ax6.set_title('Local vs Global Usage', fontweight='bold')
            ax6.set_ylabel('Average Usage (minutes)')
            ax6.set_xticks(x)
            ax6.set_xticklabels(apps_in_global, rotation=45)
            ax6.legend()
        
        # 7. Top Users Analysis (Bottom right)
        ax7 = plt.subplot(3, 3, 9)
        user_usage = self.top_apps_data.groupby('userId')['usage_minutes'].sum().sort_values(ascending=False).head(10)
        ax7.bar(range(len(user_usage)), user_usage.values, color='coral')
        ax7.set_title('Top 10 Users by Total Usage', fontweight='bold')
        ax7.set_xlabel('User Rank')
        ax7.set_ylabel('Total Usage (minutes)')
        
        plt.tight_layout()
        plt.show()
        
        analysis_logger.success("Visualizations created successfully")
    
    def generate_app_report(self, app_name: str) -> Dict:
        """Generate detailed report for a specific app."""
        if app_name not in self.top_apps_data['app_name'].values:
            return {"error": f"App '{app_name}' not found in data"}
        
        app_data = self.top_apps_data[self.top_apps_data['app_name'] == app_name]
        
        report = {
            'app_name': app_name,
            'category': self.app_categories.get(app_name, 'Other'),
            'usage_statistics': {
                'total_sessions': len(app_data),
                'unique_users': app_data['userId'].nunique(),
                'avg_usage_minutes': app_data['usage_minutes'].mean(),
                'median_usage_minutes': app_data['usage_minutes'].median(),
                'total_usage_hours': app_data['usage_minutes'].sum() / 60,
                'usage_range': f"{app_data['usage_minutes'].min()}-{app_data['usage_minutes'].max()} minutes"
            },
            'user_preferences': {
                'roast_intensity_distribution': app_data['roast_intensity'].value_counts().to_dict(),
                'most_preferred_intensity': app_data['roast_intensity'].mode()[0],
                'category_preferences': app_data['roast_category_1'].value_counts().head().to_dict()
            },
            'time_patterns': {},
            'global_comparison': {},
            'recommendations': []
        }
        
        # Add time patterns if available
        if 'day_of_week' in app_data.columns:
            day_usage = app_data.groupby('day_of_week')['usage_minutes'].mean()
            report['time_patterns'] = {
                'peak_day': day_usage.idxmax(),
                'peak_usage': day_usage.max(),
                'daily_averages': day_usage.to_dict()
            }
        
        # Add global comparison if available
        if app_name in self.global_averages:
            local_avg = app_data['usage_minutes'].mean()
            global_avg = self.global_averages[app_name]
            report['global_comparison'] = {
                'local_average': local_avg,
                'global_average': global_avg,
                'difference': local_avg - global_avg,
                'percentage_difference': ((local_avg - global_avg) / global_avg) * 100
            }
        
        return report