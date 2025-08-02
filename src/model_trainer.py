#!/usr/bin/env python3
"""
Model Trainer Module for Screen Time Roast Analyzer
Handles ML model training and evaluation.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import logging
from typing import Tuple, Dict, Any, List
import joblib

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """Handles ML model training and evaluation."""
    
    def __init__(self):
        """Initialize the ModelTrainer."""
        self.model = None
        self.encoder = None
        self.feature_columns = None
        self.target_column = 'usage_minutes'
        
    def train_and_evaluate(self, df: pd.DataFrame) -> Tuple[Any, Any]:
        """
        Train and evaluate the predictive model (simplified version for basic requirements).
        
        Args:
            df: Prepared DataFrame
            
        Returns:
            Tuple of (trained_model, encoder)
        """
        logger.info("🤖 Starting model training and evaluation...")
        
        # Select features and target
        feature_columns = self._select_features(df)
        X = df[feature_columns]
        y = df[self.target_column]
        
        # Perform one-hot encoding for categorical features
        categorical_features = X.select_dtypes(include=['object']).columns.tolist()
        numerical_features = X.select_dtypes(exclude=['object']).columns.tolist()
        
        # Create preprocessor
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', 'passthrough', numerical_features),
                ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_features)
            ]
        )
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Create and train the model pipeline
        model_pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('regressor', DecisionTreeRegressor(random_state=42))
        ])
        
        model_pipeline.fit(X_train, y_train)
        
        # Make predictions
        y_pred = model_pipeline.predict(X_test)
        
        # Evaluate the model
        mae = mean_absolute_error(y_test, y_pred)
        logger.info(f"📊 Mean Absolute Error (MAE): {mae:.2f} minutes")
        
        # Store the trained model and feature info
        self.model = model_pipeline
        self.feature_columns = feature_columns
        
        return model_pipeline, preprocessor
    
    def train_model(self, df: pd.DataFrame, model_type: str = 'random_forest') -> Dict[str, Any]:
        """
        Advanced model training with multiple algorithms and comprehensive evaluation.
        
        Args:
            df: Prepared DataFrame
            model_type: Type of model ('random_forest', 'decision_tree', 'linear_regression')
            
        Returns:
            Dictionary with training results
        """
        logger.info(f"🚀 Training {model_type} model...")
        
        # Select features and target
        feature_columns = self._select_features(df)
        X = df[feature_columns]
        y = df[self.target_column]
        
        logger.info(f"📊 Features selected: {feature_columns}")
        logger.info(f"🎯 Target variable: {self.target_column}")
        
        # Prepare data
        X_processed, preprocessor = self._prepare_features(X)
        
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(
            X_processed, y, test_size=0.2, random_state=42, stratify=None
        )
        
        # Select and train model
        model = self._get_model(model_type)
        model.fit(X_train, y_train)
        
        # Make predictions
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
        
        # Calculate metrics
        train_mae = mean_absolute_error(y_train, y_train_pred)
        test_mae = mean_absolute_error(y_test, y_test_pred)
        train_r2 = r2_score(y_train, y_train_pred)
        test_r2 = r2_score(y_test, y_test_pred)
        
        # Cross-validation
        cv_scores = cross_val_score(model, X_processed, y, cv=5, scoring='r2')
        
        # Store model and preprocessor
        self.model = model
        self.encoder = preprocessor
        self.feature_columns = feature_columns
        
        results = {
            'model_type': model_type,
            'train_mae': train_mae,
            'test_mae': test_mae,
            'train_r2': train_r2,
            'test_r2': test_r2,
            'cv_mean_r2': cv_scores.mean(),
            'cv_std_r2': cv_scores.std(),
            'feature_count': len(feature_columns),
            'training_samples': len(X_train),
            'test_samples': len(X_test)
        }
        
        logger.info(f"✅ Model training completed!")
        logger.info(f"📊 Test MAE: {test_mae:.2f} minutes")
        logger.info(f"📊 Test R²: {test_r2:.3f}")
        logger.info(f"📊 CV R²: {cv_scores.mean():.3f} ± {cv_scores.std():.3f}")
        
        return results
    
    def _select_features(self, df: pd.DataFrame) -> List[str]:
        """
        Select relevant features for model training.
        
        Args:
            df: DataFrame to select features from
            
        Returns:
            List of feature column names
        """
        # Define potential features
        potential_features = [
            'app_name', 'app_category', 'day_of_week', 'usage_category',
            'roast_category_1', 'roast_intensity', 'is_heavy_user'
        ]
        
        # Select features that exist in the dataframe
        available_features = [col for col in potential_features if col in df.columns]
        
        # Ensure we have the target column
        if self.target_column not in df.columns:
            raise ValueError(f"Target column '{self.target_column}' not found in DataFrame")
        
        logger.info(f"🎯 Selected {len(available_features)} features: {available_features}")
        return available_features
    
    def _prepare_features(self, X: pd.DataFrame) -> Tuple[np.ndarray, ColumnTransformer]:
        """
        Prepare features with proper encoding.
        
        Args:
            X: Feature DataFrame
            
        Returns:
            Tuple of (processed_features, preprocessor)
        """
        categorical_features = X.select_dtypes(include=['object']).columns.tolist()
        numerical_features = X.select_dtypes(exclude=['object']).columns.tolist()
        
        logger.info(f"📊 Categorical features: {categorical_features}")
        logger.info(f"📊 Numerical features: {numerical_features}")
        
        # Create preprocessor
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', 'passthrough', numerical_features),
                ('cat', OneHotEncoder(drop='first', sparse_output=False, handle_unknown='ignore'), 
                 categorical_features)
            ]
        )
        
        # Fit and transform
        X_processed = preprocessor.fit_transform(X)
        
        return X_processed, preprocessor
    
    def _get_model(self, model_type: str):
        """
        Get the specified model instance.
        
        Args:
            model_type: Type of model to create
            
        Returns:
            Model instance
        """
        models = {
            'random_forest': RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            ),
            'decision_tree': DecisionTreeRegressor(
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=42
            ),
            'linear_regression': LinearRegression()
        }
        
        if model_type not in models:
            raise ValueError(f"Unknown model type: {model_type}")
        
        return models[model_type]
    
    def predict_usage(self, user_data: pd.DataFrame) -> np.ndarray:
        """
        Predict usage for new user data.
        
        Args:
            user_data: DataFrame with user features
            
        Returns:
            Array of predicted usage minutes
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train_model() first.")
        
        # Select the same features used in training
        X = user_data[self.feature_columns]
        
        # If using the simple pipeline model
        if hasattr(self.model, 'predict'):
            if hasattr(self.model, 'named_steps'):  # Pipeline
                predictions = self.model.predict(X)
            else:  # Direct model with separate encoder
                X_processed = self.encoder.transform(X)
                predictions = self.model.predict(X_processed)
        else:
            raise ValueError("Invalid model state")
        
        return predictions
    
    def evaluate_model(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Comprehensive model evaluation.
        
        Args:
            df: DataFrame for evaluation
            
        Returns:
            Dictionary with evaluation metrics
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train_model() first.")
        
        logger.info("📈 Evaluating model performance...")
        
        # Prepare data
        X = df[self.feature_columns]
        y = df[self.target_column]
        
        # Make predictions
        predictions = self.predict_usage(df)
        
        # Calculate metrics
        mae = mean_absolute_error(y, predictions)
        mse = mean_squared_error(y, predictions)
        rmse = np.sqrt(mse)
        r2 = r2_score(y, predictions)
        
        # Calculate accuracy within different thresholds
        accuracy_10min = np.mean(np.abs(y - predictions) <= 10)
        accuracy_30min = np.mean(np.abs(y - predictions) <= 30)
        accuracy_60min = np.mean(np.abs(y - predictions) <= 60)
        
        evaluation_results = {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'r2_score': r2,
            'accuracy_within_10min': accuracy_10min,
            'accuracy_within_30min': accuracy_30min,
            'accuracy_within_60min': accuracy_60min,
            'mean_actual': y.mean(),
            'mean_predicted': predictions.mean(),
            'std_actual': y.std(),
            'std_predicted': predictions.std()
        }
        
        logger.info(f"📊 Evaluation Results:")
        logger.info(f"   MAE: {mae:.2f} minutes")
        logger.info(f"   R²: {r2:.3f}")
        logger.info(f"   Accuracy within 30min: {accuracy_30min:.1%}")
        
        return evaluation_results
    
    def save_model(self, filepath: str) -> None:
        """
        Save the trained model to disk.
        
        Args:
            filepath: Path to save the model
        """
        if self.model is None:
            raise ValueError("No model to save. Train a model first.")
        
        model_data = {
            'model': self.model,
            'encoder': self.encoder,
            'feature_columns': self.feature_columns,
            'target_column': self.target_column
        }
        
        joblib.dump(model_data, filepath)
        logger.info(f"💾 Model saved to: {filepath}")
    
    def load_model(self, filepath: str) -> None:
        """
        Load a trained model from disk.
        
        Args:
            filepath: Path to the saved model
        """
        model_data = joblib.load(filepath)
        
        self.model = model_data['model']
        self.encoder = model_data['encoder']
        self.feature_columns = model_data['feature_columns']
        self.target_column = model_data['target_column']
        
        logger.info(f"📂 Model loaded from: {filepath}")


def main():
    """Demo function to test model training."""
    print("🤖 MODEL TRAINER DEMO")
    print("=" * 40)
    
    # Create sample data for testing
    np.random.seed(42)
    sample_data = {
        'app_name': np.random.choice(['Instagram', 'TikTok', 'YouTube', 'Twitter'], 200),
        'day_of_week': np.random.choice(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], 200),
        'roast_category_1': np.random.choice(['social_life', 'productivity', 'health'], 200),
        'roast_intensity': np.random.choice(['light', 'medium', 'brutal'], 200),
        'usage_minutes': np.random.normal(150, 60, 200).clip(10, 500)
    }
    
    # Add derived features
    df = pd.DataFrame(sample_data)
    df['app_category'] = df['app_name'].map({
        'Instagram': 'Social Media', 'TikTok': 'Social Media',
        'YouTube': 'Entertainment', 'Twitter': 'Social Media'
    })
    df['usage_category'] = pd.cut(df['usage_minutes'], bins=[0, 60, 180, 300, 500], labels=['Light', 'Moderate', 'Heavy', 'Extreme'])
    df['is_heavy_user'] = (df['usage_minutes'] > 180).astype(int)
    
    # Test the trainer
    trainer = ModelTrainer()
    
    # Test simple training
    print("🔄 Testing simple training...")
    model, encoder = trainer.train_and_evaluate(df)
    
    # Test advanced training
    print("\n🔄 Testing advanced training...")
    results = trainer.train_model(df, model_type='random_forest')
    
    print(f"✅ Training completed!")
    print(f"📊 Test R²: {results['test_r2']:.3f}")
    print(f"📊 Test MAE: {results['test_mae']:.2f} minutes")
    
    # Test prediction
    sample_user = df.sample(1)
    prediction = trainer.predict_usage(sample_user)
    actual = sample_user['usage_minutes'].iloc[0]
    
    print(f"\n🎯 Sample Prediction:")
    print(f"   Actual: {actual:.0f} minutes")
    print(f"   Predicted: {prediction[0]:.0f} minutes")
    print(f"   Error: {abs(actual - prediction[0]):.0f} minutes")


if __name__ == "__main__":
    main()