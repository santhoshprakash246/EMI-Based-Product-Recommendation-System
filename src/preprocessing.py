"""
Data Preprocessing and Feature Engineering Module
Handles data cleaning, transformation, and feature creation
"""

import pandas as pd
import numpy as np
import os
import sys
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pickle

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *
from src.emi_calculator import EMICalculator


class DataPreprocessor:
    """
    Handles data preprocessing and feature engineering
    """
    
    def __init__(self):
        """Initialize the preprocessor"""
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.feature_columns = []
        
    def load_raw_data(self):
        """
        Load raw datasets from CSV files
        
        Returns:
            tuple: (df_products, df_customers, df_transactions)
        """
        print("Loading raw datasets...")
        
        products_path = os.path.join(RAW_DATA_DIR, PRODUCTS_FILE)
        customers_path = os.path.join(RAW_DATA_DIR, CUSTOMERS_FILE)
        transactions_path = os.path.join(RAW_DATA_DIR, TRANSACTIONS_FILE)
        
        df_products = pd.read_csv(products_path)
        df_customers = pd.read_csv(customers_path)
        df_transactions = pd.read_csv(transactions_path)
        
        print(f"✓ Loaded {len(df_products)} products")
        print(f"✓ Loaded {len(df_customers)} customers")
        print(f"✓ Loaded {len(df_transactions)} transactions")
        
        return df_products, df_customers, df_transactions
    
    def merge_datasets(self, df_products, df_customers, df_transactions):
        """
        Merge all datasets into a single dataframe
        
        Args:
            df_products (pd.DataFrame): Product dataset
            df_customers (pd.DataFrame): Customer dataset
            df_transactions (pd.DataFrame): Transaction dataset
        
        Returns:
            pd.DataFrame: Merged dataset
        """
        print("\nMerging datasets...")
        
        # Merge transactions with products
        df_merged = df_transactions.merge(
            df_products[['product_id', 'category', 'rating', 'num_reviews', 'original_price']], 
            on='product_id', 
            how='left'
        )
        
        # Merge with customers
        df_merged = df_merged.merge(
            df_customers[['customer_id', 'age', 'employment_type', 'city_tier', 'account_age_months']], 
            on='customer_id', 
            how='left'
        )
        
        print(f"✓ Merged dataset shape: {df_merged.shape}")
        
        return df_merged
    
    def create_features(self, df):
        """
        Create engineered features for model training
        
        Args:
            df (pd.DataFrame): Merged dataset
        
        Returns:
            pd.DataFrame: Dataset with engineered features
        """
        print("\nCreating engineered features...")
        
        df = df.copy()
        
        # ============================================
        # EMI-RELATED FEATURES
        # ============================================
        
        # 1. EMI to Income Ratio
        df['emi_to_income_ratio'] = df['monthly_emi'] / df['customer_income']
        
        # 2. Total EMI Burden (existing + new)
        df['total_emi_burden'] = df['existing_emi'] + df['monthly_emi']
        df['total_emi_to_income_ratio'] = df['total_emi_burden'] / df['customer_income']
        
        # 3. EMI Coverage (how much cushion does customer have)
        df['emi_coverage'] = df['max_affordable_emi'] / df['monthly_emi']
        df['emi_coverage'] = df['emi_coverage'].fillna(0)
        
        # 4. Price to Income Ratio
        df['price_to_income_ratio'] = df['product_price'] / df['customer_income']
        
        # 5. Remaining Income After EMI
        df['remaining_income'] = df['customer_income'] - df['total_emi_burden']
        df['remaining_income_percent'] = (df['remaining_income'] / df['customer_income']) * 100
        
        # ============================================
        # CREDIT-RELATED FEATURES
        # ============================================
        
        # 6. Credit Score Category
        df['credit_category'] = pd.cut(
            df['customer_credit_score'], 
            bins=[0, 550, 650, 750, 850], 
            labels=['Poor', 'Fair', 'Good', 'Excellent']
        )
        
        # 7. Credit Score Normalized (0-1)
        df['credit_score_normalized'] = (df['customer_credit_score'] - 300) / (850 - 300)
        
        # ============================================
        # PRODUCT-RELATED FEATURES
        # ============================================
        
        # 8. Product Popularity Score (based on reviews)
        max_reviews = df['num_reviews'].max()
        df['popularity_score'] = df['num_reviews'] / max_reviews if max_reviews > 0 else 0
        
        # 9. Product Quality Score (combination of rating and reviews)
        df['quality_score'] = (df['rating'] / 5.0) * 0.7 + df['popularity_score'] * 0.3
        
        # 10. Price Category
        df['price_category'] = pd.cut(
            df['product_price'], 
            bins=[0, 10000, 30000, 60000, float('inf')], 
            labels=['Budget', 'Mid-Range', 'Premium', 'Luxury']
        )
        
        # ============================================
        # DURATION-RELATED FEATURES
        # ============================================
        
        # 11. EMI Duration Category
        df['duration_category'] = pd.cut(
            df['emi_duration_months'], 
            bins=[0, 6, 12, 24, float('inf')], 
            labels=['Short', 'Medium', 'Long', 'Very Long']
        )
        
        # 12. Monthly Interest Amount
        df['monthly_interest'] = df['monthly_emi'] - (df['product_price'] / df['emi_duration_months'])
        df['monthly_interest'] = df['monthly_interest'].apply(lambda x: max(0, x))
        
        # ============================================
        # CUSTOMER PROFILE FEATURES
        # ============================================
        
        # 13. Age Category
        df['age_category'] = pd.cut(
            df['age'], 
            bins=[0, 25, 35, 45, 100], 
            labels=['Young', 'Mid-Career', 'Experienced', 'Senior']
        )
        
        # 14. Financial Health Score (composite metric)
        df['financial_health_score'] = (
            df['credit_score_normalized'] * 0.4 +
            (1 - df['total_emi_to_income_ratio']) * 0.3 +
            (df['remaining_income_percent'] / 100) * 0.3
        )
        df['financial_health_score'] = df['financial_health_score'].clip(0, 1)
        
        # ============================================
        # INTERACTION FEATURES
        # ============================================
        
        # 15. Affordability-Quality Interaction
        df['affordability_quality'] = df['affordability_score'] * df['quality_score']
        
        # 16. Income-Age Interaction
        df['income_age_ratio'] = df['customer_income'] / df['age']
        
        # 17. Risk-Income Interaction
        risk_mapping = {'Low': 0, 'Medium': 1, 'High': 2}
        df['risk_numeric'] = df['risk_level'].map(risk_mapping)
        df['risk_income_product'] = df['risk_numeric'] * df['price_to_income_ratio']
        
        print(f"✓ Created {len(df.columns)} total features")
        
        return df
    
    def encode_categorical_features(self, df, fit=True):
        """
        Encode categorical features
        
        Args:
            df (pd.DataFrame): Dataset with categorical features
            fit (bool): Whether to fit the encoders (True for training, False for prediction)
        
        Returns:
            pd.DataFrame: Dataset with encoded features
        """
        print("\nEncoding categorical features...")
        
        df = df.copy()
        
        # Categorical columns to encode
        categorical_cols = ['category', 'employment_type', 'city_tier', 
                          'credit_category', 'price_category', 
                          'duration_category', 'age_category']
        
        # One-hot encoding
        for col in categorical_cols:
            if col in df.columns:
                dummies = pd.get_dummies(df[col], prefix=col, drop_first=True)
                df = pd.concat([df, dummies], axis=1)
        
        print(f"✓ Encoded categorical features")
        
        return df
    
    def select_model_features(self, df):
        """
        Select features for model training
        
        Args:
            df (pd.DataFrame): Processed dataset
        
        Returns:
            pd.DataFrame: Dataset with selected features
        """
        print("\nSelecting features for modeling...")
        
        # Numerical features
        numerical_features = [
            'product_price', 'emi_duration_months', 'monthly_emi', 'interest_rate',
            'customer_income', 'customer_credit_score', 'existing_emi', 
            'max_affordable_emi', 'age', 'account_age_months',
            'rating', 'num_reviews', 'affordability_ratio',
            
            # Engineered features
            'emi_to_income_ratio', 'total_emi_burden', 'total_emi_to_income_ratio',
            'emi_coverage', 'price_to_income_ratio', 'remaining_income',
            'remaining_income_percent', 'credit_score_normalized',
            'popularity_score', 'quality_score', 'monthly_interest',
            'financial_health_score', 'affordability_quality', 'income_age_ratio',
            'risk_income_product'
        ]
        
        # Get one-hot encoded columns
        encoded_cols = [col for col in df.columns if any(
            col.startswith(prefix) for prefix in [
                'category_', 'employment_type_', 'city_tier_',
                'credit_category_', 'price_category_', 
                'duration_category_', 'age_category_'
            ]
        )]
        
        # Combine all features
        self.feature_columns = numerical_features + encoded_cols
        
        # Filter only available columns
        available_features = [col for col in self.feature_columns if col in df.columns]
        
        print(f"✓ Selected {len(available_features)} features for modeling")
        
        return available_features
    
    def scale_features(self, df, feature_columns, fit=True):
        """
        Scale numerical features
        
        Args:
            df (pd.DataFrame): Dataset
            feature_columns (list): List of feature column names
            fit (bool): Whether to fit the scaler (True for training, False for prediction)
        
        Returns:
            pd.DataFrame: Dataset with scaled features
        """
        df = df.copy()
        
        if fit:
            df[feature_columns] = self.scaler.fit_transform(df[feature_columns])
            print("✓ Fitted and transformed features")
        else:
            df[feature_columns] = self.scaler.transform(df[feature_columns])
            print("✓ Transformed features using existing scaler")
        
        return df
    
    def prepare_data_for_modeling(self, scale_data=True):
        """
        Complete preprocessing pipeline
        
        Args:
            scale_data (bool): Whether to scale features
        
        Returns:
            pd.DataFrame: Fully processed dataset ready for modeling
        """
        print("="*60)
        print("Starting Data Preprocessing Pipeline")
        print("="*60)
        
        # Load data
        df_products, df_customers, df_transactions = self.load_raw_data()
        
        # Merge datasets
        df_merged = self.merge_datasets(df_products, df_customers, df_transactions)
        
        # Create features
        df_featured = self.create_features(df_merged)
        
        # Encode categorical features
        df_encoded = self.encode_categorical_features(df_featured, fit=True)
        
        # Select features
        feature_columns = self.select_model_features(df_encoded)
        
        # Scale features (optional)
        if scale_data:
            df_final = self.scale_features(df_encoded, feature_columns, fit=True)
        else:
            df_final = df_encoded
        
        # Save processed data
        os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)
        processed_path = os.path.join(PROCESSED_DATA_DIR, PROCESSED_DATA_FILE)
        df_final.to_csv(processed_path, index=False)
        print(f"\n✓ Saved processed data to: {processed_path}")
        
        # Save scaler and encoders
        self.save_preprocessor()
        
        print("\n" + "="*60)
        print("Preprocessing Complete!")
        print("="*60)
        
        return df_final, feature_columns
    
    def save_preprocessor(self):
        """Save scaler and encoders"""
        os.makedirs(MODELS_DIR, exist_ok=True)
        
        scaler_path = os.path.join(MODELS_DIR, SCALER_FILE)
        with open(scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)
        print(f"✓ Saved scaler to: {scaler_path}")
    
    def load_preprocessor(self):
        """Load scaler and encoders"""
        scaler_path = os.path.join(MODELS_DIR, SCALER_FILE)
        
        if os.path.exists(scaler_path):
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            print(f"✓ Loaded scaler from: {scaler_path}")
        else:
            print("⚠ Scaler file not found")


if __name__ == "__main__":
    # Run preprocessing pipeline
    preprocessor = DataPreprocessor()
    df_processed, features = preprocessor.prepare_data_for_modeling()
    
    print("\n--- Dataset Info ---")
    print(f"Shape: {df_processed.shape}")
    print(f"\nTarget Distribution:")
    print(df_processed['risk_level'].value_counts())
    print(f"\nAffordability Score Stats:")
    print(df_processed['affordability_score'].describe())
