"""
Utility Functions
Helper functions for the EMI Affordability & Recommendation System
"""

import os
import sys
import json
import pickle
import pandas as pd
import numpy as np
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *


def ensure_directories():
    """
    Ensure all required directories exist
    """
    directories = [
        RAW_DATA_DIR,
        PROCESSED_DATA_DIR,
        MODELS_DIR,
        VISUALIZATIONS_DIR
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Ensured directory exists: {directory}")


def save_model(model, filename):
    """
    Save a model to disk
    
    Args:
        model: Model object to save
        filename (str): Filename for the model
    """
    filepath = os.path.join(MODELS_DIR, filename)
    
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"✓ Saved model to: {filepath}")
    return filepath


def load_model(filename):
    """
    Load a model from disk
    
    Args:
        filename (str): Filename of the model
    
    Returns:
        Loaded model object
    """
    filepath = os.path.join(MODELS_DIR, filename)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Model file not found: {filepath}")
    
    with open(filepath, 'rb') as f:
        model = pickle.load(f)
    
    print(f"✓ Loaded model from: {filepath}")
    return model


def save_dataframe(df, filename, directory=PROCESSED_DATA_DIR):
    """
    Save DataFrame to CSV
    
    Args:
        df (pd.DataFrame): DataFrame to save
        filename (str): Filename for the CSV
        directory (str): Directory to save to
    """
    filepath = os.path.join(directory, filename)
    df.to_csv(filepath, index=False)
    print(f"✓ Saved DataFrame to: {filepath}")
    return filepath


def load_dataframe(filename, directory=PROCESSED_DATA_DIR):
    """
    Load DataFrame from CSV
    
    Args:
        filename (str): Filename of the CSV
        directory (str): Directory to load from
    
    Returns:
        pd.DataFrame: Loaded DataFrame
    """
    filepath = os.path.join(directory, filename)
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    df = pd.read_csv(filepath)
    print(f"✓ Loaded DataFrame from: {filepath}")
    return df


def get_project_stats():
    """
    Get statistics about the project data and models
    
    Returns:
        dict: Project statistics
    """
    stats = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data': {},
        'models': {},
        'directories': {}
    }
    
    # Data statistics
    try:
        products_path = os.path.join(RAW_DATA_DIR, PRODUCTS_FILE)
        if os.path.exists(products_path):
            df_products = pd.read_csv(products_path)
            stats['data']['num_products'] = len(df_products)
            stats['data']['categories'] = df_products['category'].nunique()
            stats['data']['avg_price'] = float(df_products['final_price'].mean())
    except:
        pass
    
    try:
        customers_path = os.path.join(RAW_DATA_DIR, CUSTOMERS_FILE)
        if os.path.exists(customers_path):
            df_customers = pd.read_csv(customers_path)
            stats['data']['num_customers'] = len(df_customers)
    except:
        pass
    
    try:
        transactions_path = os.path.join(RAW_DATA_DIR, TRANSACTIONS_FILE)
        if os.path.exists(transactions_path):
            df_transactions = pd.read_csv(transactions_path)
            stats['data']['num_transactions'] = len(df_transactions)
    except:
        pass
    
    # Model statistics
    model_files = [CLASSIFIER_MODEL_FILE, REGRESSOR_MODEL_FILE, SCALER_FILE, LABEL_ENCODER_FILE]
    for model_file in model_files:
        model_path = os.path.join(MODELS_DIR, model_file)
        stats['models'][model_file] = os.path.exists(model_path)
    
    # Directory statistics
    for name, path in [
        ('raw_data', RAW_DATA_DIR),
        ('processed_data', PROCESSED_DATA_DIR),
        ('models', MODELS_DIR),
        ('visualizations', VISUALIZATIONS_DIR)
    ]:
        stats['directories'][name] = {
            'exists': os.path.exists(path),
            'path': path
        }
        
        if os.path.exists(path):
            files = os.listdir(path)
            stats['directories'][name]['num_files'] = len(files)
    
    return stats


def print_project_stats():
    """
    Print project statistics in a formatted way
    """
    stats = get_project_stats()
    
    print("="*60)
    print("PROJECT STATISTICS")
    print("="*60)
    print(f"\nTimestamp: {stats['timestamp']}")
    
    print("\n--- Data ---")
    if stats['data']:
        for key, value in stats['data'].items():
            if isinstance(value, float):
                print(f"  {key}: {value:,.2f}")
            else:
                print(f"  {key}: {value}")
    else:
        print("  No data found")
    
    print("\n--- Models ---")
    for model_name, exists in stats['models'].items():
        status = "✓" if exists else "✗"
        print(f"  {status} {model_name}")
    
    print("\n--- Directories ---")
    for dir_name, info in stats['directories'].items():
        status = "✓" if info['exists'] else "✗"
        num_files = info.get('num_files', 0)
        print(f"  {status} {dir_name}: {num_files} files")
    
    print("\n" + "="*60)


def validate_user_input(max_emi, duration, monthly_income, existing_emi=0):
    """
    Validate user input for EMI calculations
    
    Args:
        max_emi (float): Maximum affordable EMI
        duration (int): EMI duration in months
        monthly_income (float): Monthly income
        existing_emi (float): Existing EMI obligations
    
    Returns:
        tuple: (is_valid, error_message)
    """
    errors = []
    
    if max_emi <= 0:
        errors.append("Maximum EMI must be greater than 0")
    
    if duration not in EMI_DURATIONS:
        errors.append(f"Duration must be one of {EMI_DURATIONS}")
    
    if monthly_income <= 0:
        errors.append("Monthly income must be greater than 0")
    
    if existing_emi < 0:
        errors.append("Existing EMI cannot be negative")
    
    if existing_emi >= monthly_income:
        errors.append("Existing EMI cannot exceed monthly income")
    
    total_emi = max_emi + existing_emi
    if total_emi > monthly_income:
        errors.append("Total EMI (max + existing) cannot exceed monthly income")
    
    if total_emi > monthly_income * 0.7:
        errors.append("Warning: Total EMI exceeds 70% of income (high risk)")
    
    is_valid = len(errors) == 0
    error_message = "; ".join(errors) if errors else None
    
    return is_valid, error_message


def format_recommendation_report(recommendations, user_profile):
    """
    Format recommendations as a text report
    
    Args:
        recommendations (pd.DataFrame): Recommended products
        user_profile (dict): User profile
    
    Returns:
        str: Formatted report
    """
    report = []
    report.append("="*60)
    report.append("PRODUCT RECOMMENDATION REPORT")
    report.append("="*60)
    report.append("")
    
    # User profile summary
    report.append("USER PROFILE")
    report.append("-" * 60)
    report.append(f"Max Affordable EMI: ₹{user_profile['max_emi']:,.2f}")
    report.append(f"EMI Duration: {user_profile['duration']} months")
    report.append(f"Monthly Income: ₹{user_profile['monthly_income']:,.2f}")
    report.append(f"Credit Score: {user_profile['credit_score']}")
    report.append("")
    
    # Recommendations
    report.append(f"TOP {len(recommendations)} RECOMMENDATIONS")
    report.append("-" * 60)
    
    for idx, product in recommendations.iterrows():
        report.append(f"\n{int(product['rank'])}. {product['product_name']}")
        report.append(f"   Category: {product['category']}")
        report.append(f"   Price: ₹{product['final_price']:,.2f}")
        report.append(f"   Monthly EMI: ₹{product['monthly_emi']:,.2f}")
        report.append(f"   Rating: {product['rating']:.1f}⭐ ({int(product['num_reviews'])} reviews)")
        report.append(f"   Affordability Score: {product['affordability_score']:.2f}")
        
        # Risk level
        from src.emi_calculator import EMICalculator
        risk = EMICalculator.classify_risk(product['affordability_score'])
        report.append(f"   Risk Level: {risk}")
    
    report.append("\n" + "="*60)
    
    return "\n".join(report)


def export_recommendations_to_csv(recommendations, filename="recommendations_export.csv"):
    """
    Export recommendations to CSV file
    
    Args:
        recommendations (pd.DataFrame): Recommended products
        filename (str): Output filename
    
    Returns:
        str: Path to exported file
    """
    # Select relevant columns
    export_cols = [
        'rank', 'product_name', 'category', 'final_price', 'monthly_emi',
        'rating', 'num_reviews', 'affordability_score', 'composite_score'
    ]
    
    export_df = recommendations[export_cols].copy()
    
    # Save to CSV
    filepath = os.path.join(PROCESSED_DATA_DIR, filename)
    export_df.to_csv(filepath, index=False)
    
    print(f"✓ Exported recommendations to: {filepath}")
    return filepath


def calculate_savings_potential(product_price, discount_percent):
    """
    Calculate savings from discount
    
    Args:
        product_price (float): Final product price
        discount_percent (float): Discount percentage
    
    Returns:
        float: Savings amount
    """
    original_price = product_price / (1 - discount_percent/100)
    savings = original_price - product_price
    return round(savings, 2)


def get_emi_comparison_table(price, interest_rate):
    """
    Get EMI comparison table for different durations
    
    Args:
        price (float): Product price
        interest_rate (float): Annual interest rate
    
    Returns:
        pd.DataFrame: EMI comparison table
    """
    from src.emi_calculator import EMICalculator
    
    comparisons = EMICalculator.compare_emi_options(price, interest_rate)
    
    df = pd.DataFrame(comparisons)
    df = df[['duration_months', 'monthly_emi', 'total_payment', 'total_interest']]
    df.columns = ['Duration (months)', 'Monthly EMI (₹)', 'Total Payment (₹)', 'Total Interest (₹)']
    
    return df


def check_system_ready():
    """
    Check if the system is ready to use (data and models exist)
    
    Returns:
        tuple: (is_ready, missing_items)
    """
    missing = []
    
    # Check data files
    data_files = [
        (RAW_DATA_DIR, PRODUCTS_FILE),
        (RAW_DATA_DIR, CUSTOMERS_FILE),
        (RAW_DATA_DIR, TRANSACTIONS_FILE)
    ]
    
    for directory, filename in data_files:
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            missing.append(f"Data file: {filename}")
    
    # Check model files (optional - can run without models)
    # Model files are created during training
    
    is_ready = len(missing) == 0
    
    return is_ready, missing


if __name__ == "__main__":
    # Test utilities
    print("Testing utility functions...\n")
    
    # Ensure directories
    ensure_directories()
    
    # Print project stats
    print_project_stats()
    
    # Check system readiness
    is_ready, missing = check_system_ready()
    print(f"\nSystem Ready: {is_ready}")
    if not is_ready:
        print("Missing items:")
        for item in missing:
            print(f"  - {item}")
