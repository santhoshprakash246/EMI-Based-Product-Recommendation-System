"""
Configuration file for EMI Affordability & Product Recommendation System
"""

import os

# ============================================
# PROJECT PATHS
# ============================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
MODELS_DIR = os.path.join(BASE_DIR, 'models', 'saved_models')
VISUALIZATIONS_DIR = os.path.join(BASE_DIR, 'visualizations')

# ============================================
# DATA GENERATION PARAMETERS
# ============================================
NUM_PRODUCTS = 1000  # Number of products in the dataset
NUM_CUSTOMERS = 500  # Number of customer profiles

# ============================================
# PRODUCT CATEGORIES
# ============================================
PRODUCT_CATEGORIES = [
    'Electronics',
    'Home Appliances',
    'Furniture',
    'Mobile Phones',
    'Laptops',
    'Fashion',
    'Sports Equipment',
    'Kitchen Appliances'
]

# ============================================
# EMI CONFIGURATION
# ============================================
# Interest rates (annual) by category
INTEREST_RATES = {
    'Electronics': 0.12,      # 12% annual
    'Home Appliances': 0.10,  # 10% annual
    'Furniture': 0.08,        # 8% annual
    'Mobile Phones': 0.15,    # 15% annual
    'Laptops': 0.12,          # 12% annual
    'Fashion': 0.18,          # 18% annual
    'Sports Equipment': 0.10, # 10% annual
    'Kitchen Appliances': 0.09 # 9% annual
}

# Standard EMI durations (in months)
EMI_DURATIONS = [3, 6, 9, 12, 18, 24, 36]

# ============================================
# AFFORDABILITY RISK THRESHOLDS
# ============================================
# Based on EMI to income ratio and affordability score
RISK_THRESHOLDS = {
    'low': 0.7,      # Affordability score >= 0.7: Low Risk
    'medium': 0.4    # 0.4 <= Affordability score < 0.7: Medium Risk
                     # Affordability score < 0.4: High Risk
}

# ============================================
# MODEL PARAMETERS
# ============================================
# Random Forest Classifier
RF_CLASSIFIER_PARAMS = {
    'n_estimators': 100,
    'max_depth': 10,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'random_state': 42
}

# Random Forest Regressor (for affordability score prediction)
RF_REGRESSOR_PARAMS = {
    'n_estimators': 100,
    'max_depth': 10,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'random_state': 42
}

# Train-test split ratio
TEST_SIZE = 0.2
RANDOM_STATE = 42

# ============================================
# RECOMMENDATION ENGINE PARAMETERS
# ============================================
# Content-based filtering weights
RECOMMENDATION_WEIGHTS = {
    'affordability_score': 0.4,
    'product_rating': 0.3,
    'popularity': 0.2,
    'category_match': 0.1
}

# Maximum number of products to recommend
MAX_RECOMMENDATIONS = 10

# ============================================
# STREAMLIT APP SETTINGS
# ============================================
APP_TITLE = "🏦 AI-Based EMI Affordability & Product Recommendation System"
APP_ICON = "💳"
LAYOUT = "wide"

# ============================================
# FILE NAMES
# ============================================
PRODUCTS_FILE = 'products.csv'
CUSTOMERS_FILE = 'customers.csv'
TRANSACTIONS_FILE = 'transactions.csv'
PROCESSED_DATA_FILE = 'processed_data.csv'

# Model file names
CLASSIFIER_MODEL_FILE = 'risk_classifier.pkl'
REGRESSOR_MODEL_FILE = 'affordability_regressor.pkl'
SCALER_FILE = 'feature_scaler.pkl'
LABEL_ENCODER_FILE = 'label_encoder.pkl'

# ============================================
# VISUALIZATION SETTINGS
# ============================================
PLOT_STYLE = 'seaborn-v0_8-darkgrid'
FIGURE_SIZE = (12, 6)
COLOR_PALETTE = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#6A994E']
