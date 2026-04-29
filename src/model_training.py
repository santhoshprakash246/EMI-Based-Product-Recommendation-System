"""
Model Training Module
Trains classification and regression models for EMI affordability prediction
"""

import pandas as pd
import numpy as np
import os
import sys
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, roc_auc_score, roc_curve,
    mean_squared_error, mean_absolute_error, r2_score
)
from sklearn.preprocessing import LabelEncoder

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *


class ModelTrainer:
    """
    Handles training and evaluation of ML models
    """
    
    def __init__(self):
        """Initialize the model trainer"""
        self.classifier = None
        self.regressor = None
        self.label_encoder = LabelEncoder()
        self.feature_importance = {}
        
    def load_processed_data(self):
        """
        Load processed dataset
        
        Returns:
            pd.DataFrame: Processed dataset
        """
        print("Loading processed dataset...")
        
        processed_path = os.path.join(PROCESSED_DATA_DIR, PROCESSED_DATA_FILE)
        
        if not os.path.exists(processed_path):
            raise FileNotFoundError(
                f"Processed data not found at {processed_path}. "
                "Please run preprocessing first."
            )
        
        df = pd.read_csv(processed_path)
        print(f"✓ Loaded dataset with shape: {df.shape}")
        
        return df
    
    def prepare_train_test_split(self, df, feature_columns):
        """
        Prepare train-test split for modeling
        
        Args:
            df (pd.DataFrame): Processed dataset
            feature_columns (list): List of feature column names
        
        Returns:
            tuple: (X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test)
        """
        print("\nPreparing train-test split...")
        
        # Filter only available features
        available_features = [col for col in feature_columns if col in df.columns]
        
        # Features
        X = df[available_features].copy()
        
        # Handle any missing values
        X = X.fillna(X.mean())
        
        # Classification target: Risk Level
        y_classification = df['risk_level'].copy()
        
        # Encode risk levels (Low=0, Medium=1, High=2)
        self.label_encoder.fit(['Low', 'Medium', 'High'])
        y_class_encoded = self.label_encoder.transform(y_classification)
        
        # Regression target: Affordability Score
        y_regression = df['affordability_score'].copy()
        
        # Train-test split (same split for both tasks)
        X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test = train_test_split(
            X, y_class_encoded, y_regression,
            test_size=TEST_SIZE,
            random_state=RANDOM_STATE,
            stratify=y_class_encoded
        )
        
        print(f"✓ Training set size: {len(X_train)}")
        print(f"✓ Test set size: {len(X_test)}")
        
        return X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test
    
    def train_classifier(self, X_train, y_train):
        """
        Train Random Forest Classifier for risk prediction
        
        Args:
            X_train (pd.DataFrame): Training features
            y_train (np.array): Training labels
        
        Returns:
            RandomForestClassifier: Trained classifier
        """
        print("\n" + "="*60)
        print("Training Risk Classification Model")
        print("="*60)
        
        # Initialize classifier
        self.classifier = RandomForestClassifier(**RF_CLASSIFIER_PARAMS)
        
        # Train model
        print("Training Random Forest Classifier...")
        self.classifier.fit(X_train, y_train)
        
        # Feature importance
        self.feature_importance['classifier'] = pd.DataFrame({
            'feature': X_train.columns,
            'importance': self.classifier.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("✓ Classifier training complete")
        
        # Cross-validation
        cv_scores = cross_val_score(self.classifier, X_train, y_train, cv=5, scoring='accuracy')
        print(f"\nCross-Validation Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        return self.classifier
    
    def train_regressor(self, X_train, y_train):
        """
        Train Random Forest Regressor for affordability score prediction
        
        Args:
            X_train (pd.DataFrame): Training features
            y_train (np.array): Training targets
        
        Returns:
            RandomForestRegressor: Trained regressor
        """
        print("\n" + "="*60)
        print("Training Affordability Score Regression Model")
        print("="*60)
        
        # Initialize regressor
        self.regressor = RandomForestRegressor(**RF_REGRESSOR_PARAMS)
        
        # Train model
        print("Training Random Forest Regressor...")
        self.regressor.fit(X_train, y_train)
        
        # Feature importance
        self.feature_importance['regressor'] = pd.DataFrame({
            'feature': X_train.columns,
            'importance': self.regressor.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("✓ Regressor training complete")
        
        # Cross-validation
        cv_scores = cross_val_score(self.regressor, X_train, y_train, cv=5, scoring='r2')
        print(f"\nCross-Validation R² Score: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        return self.regressor
    
    def evaluate_classifier(self, X_test, y_test):
        """
        Evaluate classification model
        
        Args:
            X_test (pd.DataFrame): Test features
            y_test (np.array): Test labels
        
        Returns:
            dict: Evaluation metrics
        """
        print("\n" + "="*60)
        print("Evaluating Classification Model")
        print("="*60)
        
        # Predictions
        y_pred = self.classifier.predict(X_test)
        y_pred_proba = self.classifier.predict_proba(X_test)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        # ROC-AUC (multiclass)
        try:
            roc_auc = roc_auc_score(y_test, y_pred_proba, multi_class='ovr', average='weighted')
        except:
            roc_auc = 0.0
        
        print(f"\nClassification Metrics:")
        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1-Score:  {f1:.4f}")
        print(f"  ROC-AUC:   {roc_auc:.4f}")
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        print(f"\nConfusion Matrix:")
        print(cm)
        
        # Classification Report
        target_names = self.label_encoder.classes_
        print(f"\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=target_names, zero_division=0))
        
        metrics = {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'roc_auc': roc_auc,
            'confusion_matrix': cm,
            'predictions': y_pred,
            'probabilities': y_pred_proba
        }
        
        return metrics
    
    def evaluate_regressor(self, X_test, y_test):
        """
        Evaluate regression model
        
        Args:
            X_test (pd.DataFrame): Test features
            y_test (np.array): Test targets
        
        Returns:
            dict: Evaluation metrics
        """
        print("\n" + "="*60)
        print("Evaluating Regression Model")
        print("="*60)
        
        # Predictions
        y_pred = self.regressor.predict(X_test)
        
        # Metrics
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # MAPE (Mean Absolute Percentage Error)
        mape = np.mean(np.abs((y_test - y_pred) / (y_test + 1e-10))) * 100
        
        print(f"\nRegression Metrics:")
        print(f"  MSE:  {mse:.4f}")
        print(f"  RMSE: {rmse:.4f}")
        print(f"  MAE:  {mae:.4f}")
        print(f"  R²:   {r2:.4f}")
        print(f"  MAPE: {mape:.2f}%")
        
        metrics = {
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'r2': r2,
            'mape': mape,
            'predictions': y_pred
        }
        
        return metrics
    
    def plot_feature_importance(self, model_type='classifier', top_n=15):
        """
        Plot feature importance
        
        Args:
            model_type (str): 'classifier' or 'regressor'
            top_n (int): Number of top features to plot
        """
        if model_type not in self.feature_importance:
            print(f"Feature importance not available for {model_type}")
            return
        
        importance_df = self.feature_importance[model_type].head(top_n)
        
        plt.figure(figsize=(10, 8))
        plt.barh(importance_df['feature'], importance_df['importance'])
        plt.xlabel('Importance')
        plt.ylabel('Feature')
        plt.title(f'Top {top_n} Feature Importances - {model_type.capitalize()}')
        plt.gca().invert_yaxis()
        plt.tight_layout()
        
        # Save plot
        os.makedirs(VISUALIZATIONS_DIR, exist_ok=True)
        plot_path = os.path.join(VISUALIZATIONS_DIR, f'feature_importance_{model_type}.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved feature importance plot to: {plot_path}")
        plt.close()
    
    def plot_confusion_matrix(self, cm):
        """
        Plot confusion matrix heatmap
        
        Args:
            cm (np.array): Confusion matrix
        """
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                   xticklabels=self.label_encoder.classes_,
                   yticklabels=self.label_encoder.classes_)
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.title('Confusion Matrix - Risk Classification')
        plt.tight_layout()
        
        # Save plot
        plot_path = os.path.join(VISUALIZATIONS_DIR, 'confusion_matrix.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved confusion matrix to: {plot_path}")
        plt.close()
    
    def plot_prediction_comparison(self, y_test, y_pred, model_type='regressor'):
        """
        Plot actual vs predicted values
        
        Args:
            y_test (np.array): Actual values
            y_pred (np.array): Predicted values
            model_type (str): Model type for title
        """
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, y_pred, alpha=0.5)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        plt.xlabel('Actual Affordability Score')
        plt.ylabel('Predicted Affordability Score')
        plt.title('Actual vs Predicted - Affordability Score')
        plt.tight_layout()
        
        # Save plot
        plot_path = os.path.join(VISUALIZATIONS_DIR, 'prediction_comparison.png')
        plt.savefig(plot_path, dpi=300, bbox_inches='tight')
        print(f"✓ Saved prediction comparison plot to: {plot_path}")
        plt.close()
    
    def save_models(self):
        """Save trained models"""
        os.makedirs(MODELS_DIR, exist_ok=True)
        
        # Save classifier
        if self.classifier is not None:
            classifier_path = os.path.join(MODELS_DIR, CLASSIFIER_MODEL_FILE)
            with open(classifier_path, 'wb') as f:
                pickle.dump(self.classifier, f)
            print(f"✓ Saved classifier to: {classifier_path}")
        
        # Save regressor
        if self.regressor is not None:
            regressor_path = os.path.join(MODELS_DIR, REGRESSOR_MODEL_FILE)
            with open(regressor_path, 'wb') as f:
                pickle.dump(self.regressor, f)
            print(f"✓ Saved regressor to: {regressor_path}")
        
        # Save label encoder
        encoder_path = os.path.join(MODELS_DIR, LABEL_ENCODER_FILE)
        with open(encoder_path, 'wb') as f:
            pickle.dump(self.label_encoder, f)
        print(f"✓ Saved label encoder to: {encoder_path}")
    
    def load_models(self):
        """Load trained models"""
        classifier_path = os.path.join(MODELS_DIR, CLASSIFIER_MODEL_FILE)
        regressor_path = os.path.join(MODELS_DIR, REGRESSOR_MODEL_FILE)
        encoder_path = os.path.join(MODELS_DIR, LABEL_ENCODER_FILE)
        
        if os.path.exists(classifier_path):
            with open(classifier_path, 'rb') as f:
                self.classifier = pickle.load(f)
            print(f"✓ Loaded classifier from: {classifier_path}")
        
        if os.path.exists(regressor_path):
            with open(regressor_path, 'rb') as f:
                self.regressor = pickle.load(f)
            print(f"✓ Loaded regressor from: {regressor_path}")
        
        if os.path.exists(encoder_path):
            with open(encoder_path, 'rb') as f:
                self.label_encoder = pickle.load(f)
            print(f"✓ Loaded label encoder from: {encoder_path}")
    
    def train_and_evaluate(self, df, feature_columns):
        """
        Complete training and evaluation pipeline
        
        Args:
            df (pd.DataFrame): Processed dataset
            feature_columns (list): List of feature columns
        
        Returns:
            dict: All evaluation metrics
        """
        print("="*60)
        print("Starting Model Training Pipeline")
        print("="*60)
        
        # Prepare data
        X_train, X_test, y_class_train, y_class_test, y_reg_train, y_reg_test = \
            self.prepare_train_test_split(df, feature_columns)
        
        # Train models
        self.train_classifier(X_train, y_class_train)
        self.train_regressor(X_train, y_reg_train)
        
        # Evaluate models
        classifier_metrics = self.evaluate_classifier(X_test, y_class_test)
        regressor_metrics = self.evaluate_regressor(X_test, y_reg_test)
        
        # Generate visualizations
        print("\nGenerating visualizations...")
        self.plot_feature_importance('classifier', top_n=15)
        self.plot_feature_importance('regressor', top_n=15)
        self.plot_confusion_matrix(classifier_metrics['confusion_matrix'])
        self.plot_prediction_comparison(y_reg_test, regressor_metrics['predictions'])
        
        # Save models
        print("\nSaving models...")
        self.save_models()
        
        print("\n" + "="*60)
        print("Training Pipeline Complete!")
        print("="*60)
        
        return {
            'classifier': classifier_metrics,
            'regressor': regressor_metrics
        }


if __name__ == "__main__":
    # Train models
    trainer = ModelTrainer()
    
    # Load data
    df = trainer.load_processed_data()
    
    # Get feature columns from preprocessing
    from src.preprocessing import DataPreprocessor
    preprocessor = DataPreprocessor()
    feature_columns = preprocessor.select_model_features(df)
    
    # Train and evaluate
    metrics = trainer.train_and_evaluate(df, feature_columns)
    
    print("\n=== FINAL SUMMARY ===")
    print(f"Classification Accuracy: {metrics['classifier']['accuracy']:.4f}")
    print(f"Regression R² Score: {metrics['regressor']['r2']:.4f}")
