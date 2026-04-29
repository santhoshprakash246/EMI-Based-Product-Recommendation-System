"""
__init__.py for src package
Makes src a Python package
"""

__version__ = "1.0.0"
__author__ = "MLT Project Team"

# Import main classes for easier access
from .preprocessing import DataPreprocessor
from .emi_calculator import EMICalculator
from .model_training import ModelTrainer
from .recommendation_engine import RecommendationEngine

__all__ = [
    'DataPreprocessor',
    'EMICalculator',
    'ModelTrainer',
    'RecommendationEngine'
]
