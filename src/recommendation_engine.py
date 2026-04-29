"""
Recommendation Engine Module
Implements content-based filtering for product recommendations
"""

import pandas as pd
import numpy as np
import os
import sys
import pickle
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *
from src.emi_calculator import EMICalculator


class RecommendationEngine:
    """
    Content-based product recommendation system with ML model integration
    """
    
    def __init__(self):
        """Initialize recommendation engine"""
        self.products_df = None
        self.classifier = None
        self.regressor = None
        self.scaler = None
        self.label_encoder = None
        self.feature_names = None
        
        # Try to load models on initialization
        try:
            self.load_models()
            print("✓ ML models loaded successfully")
        except Exception as e:
            print(f"⚠️ Warning: Could not load ML models: {e}")
            print("  Falling back to manual scoring method")
        
    def load_products(self):
        """
        Load product dataset
        
        Returns:
            pd.DataFrame: Product dataset
        """
        products_path = os.path.join(RAW_DATA_DIR, PRODUCTS_FILE)
        
        if not os.path.exists(products_path):
            raise FileNotFoundError(f"Products file not found at {products_path}")
        
        self.products_df = pd.read_csv(products_path)
        print(f"✓ Loaded {len(self.products_df)} products")
        
        return self.products_df
    
    def load_models(self):
        """Load trained ML models, scaler, and label encoder"""
        classifier_path = os.path.join(MODELS_DIR, CLASSIFIER_MODEL_FILE)
        regressor_path = os.path.join(MODELS_DIR, REGRESSOR_MODEL_FILE)
        scaler_path = os.path.join(MODELS_DIR, SCALER_FILE)
        label_encoder_path = os.path.join(MODELS_DIR, LABEL_ENCODER_FILE)
        
        # Load classifier (risk level prediction)
        if os.path.exists(classifier_path):
            with open(classifier_path, 'rb') as f:
                self.classifier = pickle.load(f)
            print("✓ Loaded risk classifier model")
        else:
            print(f"⚠️ Classifier not found at {classifier_path}")
        
        # Load regressor (affordability score prediction)
        if os.path.exists(regressor_path):
            with open(regressor_path, 'rb') as f:
                self.regressor = pickle.load(f)
            print("✓ Loaded affordability regressor model")
        else:
            print(f"⚠️ Regressor not found at {regressor_path}")
        
        # Load feature scaler
        if os.path.exists(scaler_path):
            with open(scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            print("✓ Loaded feature scaler")
        else:
            print(f"⚠️ Scaler not found at {scaler_path}")
        
        # Load label encoder
        if os.path.exists(label_encoder_path):
            with open(label_encoder_path, 'rb') as f:
                self.label_encoder = pickle.load(f)
            print("✓ Loaded label encoder")
        else:
            print(f"⚠️ Label encoder not found at {label_encoder_path}")
    
    def prepare_features_for_prediction(self, product, user_profile, duration):
        """
        Prepare feature vector for ML model prediction
        
        Args:
            product (pd.Series): Product information
            user_profile (dict): User profile
            duration (int): EMI duration in months
        
        Returns:
            np.array: Feature vector for model prediction
        """
        try:
            # Calculate EMI
            product_price = product.get('final_price', 0)
            interest_rate = product.get('interest_rate', 0.12)
            monthly_emi = EMICalculator.calculate_emi(product_price, interest_rate, duration)
            
            # Extract user profile
            customer_income = user_profile.get('monthly_income', 50000)
            credit_score = user_profile.get('credit_score', 700)
            existing_emi = user_profile.get('existing_emi', 0)
            age = user_profile.get('age', 30)
            
            # Calculate ratios and derived features
            affordability_ratio = monthly_emi / customer_income if customer_income > 0 else 0
            emi_to_income_ratio = monthly_emi / customer_income if customer_income > 0 else 0
            total_emi_burden = existing_emi + monthly_emi
            total_emi_to_income_ratio = total_emi_burden / customer_income if customer_income > 0 else 0
            remaining_income = customer_income - existing_emi
            emi_coverage = monthly_emi / remaining_income if remaining_income > 0 else 0
            remaining_income_percent = (remaining_income - monthly_emi) / customer_income * 100 if customer_income > 0 else 0
            price_to_income_ratio = product_price / customer_income if customer_income > 0 else 0
            credit_score_normalized = min(credit_score / 850.0, 1.0)
            popularity_score = float(product.get('num_reviews', 0)) / 1000.0
            quality_score = float(product.get('rating', 3.0)) / 5.0
            monthly_interest = product_price * interest_rate / 12.0
            financial_health_score = (credit_score_normalized + quality_score) / 2.0
            affordability_quality = affordability_ratio * quality_score
            income_age_ratio = customer_income / (age + 1) if age > 0 else 0
            risk_income_product = affordability_ratio * (1.0 - credit_score_normalized)
            
            # Prepare feature list (same order as training)
            features = [
                product_price, duration, monthly_emi, interest_rate,
                customer_income, credit_score, existing_emi,
                user_profile.get('max_emi', 10000), age, 0,  # account_age_months=0 for new prediction
                product.get('rating', 3.0), product.get('num_reviews', 0), affordability_ratio,
                # Engineered features
                emi_to_income_ratio, total_emi_burden, total_emi_to_income_ratio,
                emi_coverage, price_to_income_ratio, remaining_income,
                remaining_income_percent, credit_score_normalized,
                popularity_score, quality_score, monthly_interest,
                financial_health_score, affordability_quality, income_age_ratio,
                risk_income_product
            ]
            
            return np.array(features).reshape(1, -1)
        except Exception as e:
            print(f"⚠️ Error preparing features: {e}")
            return None
    
    def predict_risk_level_with_model(self, features):
        """
        Predict risk level using trained classifier
        
        Args:
            features (np.array): Feature vector
        
        Returns:
            tuple: (risk_level_string, confidence)
        """
        try:
            if self.classifier is None or self.label_encoder is None:
                return None, 0.0
            
            # Make prediction
            prediction = self.classifier.predict(features)[0]
            probabilities = self.classifier.predict_proba(features)[0]
            confidence = np.max(probabilities)
            
            # Decode prediction
            risk_level = self.label_encoder.inverse_transform([prediction])[0]
            
            return risk_level, float(confidence)
        except Exception as e:
            print(f"⚠️ Error in risk prediction: {e}")
            return None, 0.0
    
    def predict_affordability_score_with_model(self, features):
        """
        Predict affordability score using trained regressor
        
        Args:
            features (np.array): Feature vector
        
        Returns:
            float: Affordability score (0-1)
        """
        try:
            if self.regressor is None:
                return None
            
            # Make prediction
            score = self.regressor.predict(features)[0]
            
            # Ensure score is within 0-1 range
            score = max(0.0, min(1.0, float(score)))
            
            return score
        except Exception as e:
            print(f"⚠️ Error in affordability prediction: {e}")
            return None
    
    def calculate_product_scores(self, products_df, user_profile):
        """
        Calculate comprehensive scores for products using ML models or fallback to manual calculation
        
        Args:
            products_df (pd.DataFrame): Product dataset
            user_profile (dict): User profile containing EMI preferences
        
        Returns:
            pd.DataFrame: Products with calculated scores
        """
        products_df = products_df.copy()
        
        # Extract user preferences
        max_emi = user_profile.get('max_emi', 0)
        duration = user_profile.get('duration', 12)
        preferred_category = user_profile.get('category', None)
        credit_score = user_profile.get('credit_score', 700)
        monthly_income = user_profile.get('monthly_income', 50000)
        existing_emi = user_profile.get('existing_emi', 0)
        
        # Check if we have ML models loaded
        use_ml_models = (self.classifier is not None and self.regressor is not None)
        
        if use_ml_models:
            print("✓ Using trained ML models for predictions")
        else:
            print("ℹ️ ML models not available, using manual scoring method")
        
        scores = []
        
        for idx, product in products_df.iterrows():
            # Calculate EMI for this product
            product_price = product['final_price']
            interest_rate = product['interest_rate']
            
            monthly_emi = EMICalculator.calculate_emi(product_price, interest_rate, duration)
            
            # Calculate max affordable price
            max_price = EMICalculator.calculate_max_affordable_price(max_emi, duration, interest_rate)
            
            # Check if product is affordable
            is_affordable = product_price <= max_price
            
            # Get affordability score and risk level
            if use_ml_models:
                try:
                    # Prepare features for model prediction
                    features = self.prepare_features_for_prediction(product, user_profile, duration)
                    
                    if features is not None:
                        # Get predictions from ML models
                        affordability_score = self.predict_affordability_score_with_model(features)
                        risk_level, risk_confidence = self.predict_risk_level_with_model(features)
                        
                        if affordability_score is None:
                            # Fallback if model prediction fails
                            affordability_score = EMICalculator.calculate_affordability_score(
                                monthly_emi, max_emi, credit_score, existing_emi, monthly_income
                            )
                            risk_level = None
                        
                    else:
                        # Fallback to manual calculation
                        affordability_score = EMICalculator.calculate_affordability_score(
                            monthly_emi, max_emi, credit_score, existing_emi, monthly_income
                        )
                        risk_level = None
                except Exception as e:
                    print(f"⚠️ Model prediction error: {e}, using manual scoring")
                    affordability_score = EMICalculator.calculate_affordability_score(
                        monthly_emi, max_emi, credit_score, existing_emi, monthly_income
                    )
                    risk_level = None
            else:
                # Manual calculation
                affordability_score = EMICalculator.calculate_affordability_score(
                    monthly_emi, max_emi, credit_score, existing_emi, monthly_income
                )
                risk_level = None
            
            # Determine risk level from affordability score if not from model
            if risk_level is None:
                if affordability_score >= RISK_THRESHOLDS['low']:
                    risk_level = 'Low'
                elif affordability_score >= RISK_THRESHOLDS['medium']:
                    risk_level = 'Medium'
                else:
                    risk_level = 'High'
            
            # Normalize product rating (0-1)
            rating_score = product['rating'] / 5.0
            
            # Normalize popularity (based on reviews)
            max_reviews = products_df['num_reviews'].max()
            popularity_score = product['num_reviews'] / max_reviews if max_reviews > 0 else 0
            
            # Category match score
            # Category match score (always 1.0 now since we filter by category in get_recommendations)
            category_match = 1.0
            
            # Calculate weighted composite score
            weights = RECOMMENDATION_WEIGHTS
            composite_score = (
                weights['affordability_score'] * affordability_score +
                weights['product_rating'] * rating_score +
                weights['popularity'] * popularity_score +
                weights['category_match'] * category_match
            )
            
            scores.append({
                'product_id': product['product_id'],
                'monthly_emi': monthly_emi,
                'affordability_score': affordability_score,
                'risk_level': risk_level,
                'rating_score': rating_score,
                'popularity_score': popularity_score,
                'category_match': category_match,
                'composite_score': composite_score,
                'is_affordable': is_affordable,
                'max_affordable_price': max_price
            })
        
        scores_df = pd.DataFrame(scores)
        
        # Merge scores with products
        products_scored = products_df.merge(scores_df, on='product_id')
        
        return products_scored
    
    def rank_products(self, products_scored, filter_affordable=True):
        """
        Rank products based on composite score
        
        Args:
            products_scored (pd.DataFrame): Products with scores
            filter_affordable (bool): Whether to filter only affordable products
        
        Returns:
            pd.DataFrame: Ranked products
        """
        # Filter affordable products if requested
        if filter_affordable:
            products_filtered = products_scored[products_scored['is_affordable'] == True].copy()
        else:
            products_filtered = products_scored.copy()
        
        # Sort by composite score (descending)
        products_ranked = products_filtered.sort_values('composite_score', ascending=False)
        
        # Add rank
        products_ranked['rank'] = range(1, len(products_ranked) + 1)
        
        return products_ranked
    
    def get_recommendations(self, user_profile, top_n=MAX_RECOMMENDATIONS, filter_affordable=True):
        """
        Get product recommendations for user
        
        Args:
            user_profile (dict): User profile with preferences
                - max_emi: Maximum affordable EMI
                - duration: Preferred EMI duration
                - category: Preferred category (optional)
                - credit_score: User's credit score
                - monthly_income: User's monthly income
                - existing_emi: Existing EMI obligations
            top_n (int): Number of recommendations to return
            filter_affordable (bool): Whether to filter only affordable products
        
        Returns:
            pd.DataFrame: Top N recommended products
        """
        print("="*60)
        print("Generating Product Recommendations")
        print("="*60)
        
        # Load products if not loaded
        if self.products_df is None:
            self.load_products()
        
        # Filter in-stock products
        available_products = self.products_df[self.products_df['in_stock'] == True].copy()
        
        # Filter by category if specified - STRICT FILTER
        preferred_category = user_profile.get('category', None)
        if preferred_category and preferred_category != 'Any':
            # Strip whitespace from both category columns and filter value
            available_products['category'] = available_products['category'].str.strip()
            preferred_category = preferred_category.strip()
            
            # Apply strict category filter - only matching products
            available_products = available_products[available_products['category'] == preferred_category].copy()
            
            if len(available_products) == 0:
                print(f"⚠️ WARNING: No products found for category '{preferred_category}'")
                print(f"Available categories: {self.products_df['category'].unique()}")
                return pd.DataFrame()  # Return empty dataframe if no products match
        
        print(f"\nUser Profile:")
        print(f"  Max EMI: ₹{user_profile.get('max_emi', 0):,.2f}")
        print(f"  Duration: {user_profile.get('duration', 12)} months")
        print(f"  Preferred Category: {preferred_category if preferred_category else 'Any'}")
        print(f"  Credit Score: {user_profile.get('credit_score', 700)}")
        
        # Calculate scores
        products_scored = self.calculate_product_scores(available_products, user_profile)
        
        # Rank products
        products_ranked = self.rank_products(products_scored, filter_affordable)
        
        # Get top N
        recommendations = products_ranked.head(top_n)
        
        print(f"\n✓ Generated {len(recommendations)} recommendations")
        print(f"  (Filtered affordable: {filter_affordable})")
        
        return recommendations
    
    def get_similar_products(self, product_id, top_n=5):
        """
        Get products similar to a given product (content-based)
        
        Args:
            product_id (str): Product ID
            top_n (int): Number of similar products to return
        
        Returns:
            pd.DataFrame: Similar products
        """
        if self.products_df is None:
            self.load_products()
        
        # Find the target product
        target_product = self.products_df[self.products_df['product_id'] == product_id]
        
        if len(target_product) == 0:
            print(f"Product {product_id} not found")
            return pd.DataFrame()
        
        target_product = target_product.iloc[0]
        
        # Filter products in same category
        same_category = self.products_df[
            (self.products_df['category'] == target_product['category']) &
            (self.products_df['product_id'] != product_id)
        ].copy()
        
        if len(same_category) == 0:
            return pd.DataFrame()
        
        # Calculate similarity based on price, rating, and interest rate
        target_features = np.array([
            target_product['final_price'],
            target_product['rating'],
            target_product['interest_rate']
        ]).reshape(1, -1)
        
        candidate_features = same_category[['final_price', 'rating', 'interest_rate']].values
        
        # Calculate cosine similarity
        similarities = cosine_similarity(target_features, candidate_features)[0]
        
        # Add similarity scores
        same_category['similarity_score'] = similarities
        
        # Sort by similarity
        similar_products = same_category.sort_values('similarity_score', ascending=False).head(top_n)
        
        return similar_products
    
    def explain_recommendation(self, product, user_profile):
        """
        Generate explanation for why a product was recommended
        
        Args:
            product (pd.Series): Product details
            user_profile (dict): User profile
        
        Returns:
            str: Explanation text
        """
        max_emi = user_profile.get('max_emi', 0)
        monthly_emi = product['monthly_emi']
        affordability_score = product['affordability_score']
        
        # Determine affordability level
        if affordability_score >= 0.7:
            affordability_text = "Highly affordable"
        elif affordability_score >= 0.4:
            affordability_text = "Moderately affordable"
        else:
            affordability_text = "Stretches your budget"
        
        # EMI comparison
        emi_ratio = (monthly_emi / max_emi) * 100 if max_emi > 0 else 0
        
        explanation = f"""
        📊 Recommendation Explanation:
        
        • {affordability_text} - Uses {emi_ratio:.1f}% of your EMI limit
        • Product Rating: {product['rating']:.1f}⭐ ({product['num_reviews']} reviews)
        • Affordability Score: {affordability_score:.2f}/1.00
        • Monthly EMI: ₹{monthly_emi:,.2f}
        • Category: {product['category']}
        """
        
        return explanation.strip()
    
    def get_affordability_insights(self, user_profile):
        """
        Get insights about user's affordability and purchasing power
        
        Args:
            user_profile (dict): User profile
        
        Returns:
            dict: Affordability insights
        """
        max_emi = user_profile.get('max_emi', 0)
        duration = user_profile.get('duration', 12)
        
        insights = {}
        
        # Calculate max affordable prices for different categories
        for category, interest_rate in INTEREST_RATES.items():
            max_price = EMICalculator.calculate_max_affordable_price(max_emi, duration, interest_rate)
            insights[category] = {
                'max_price': max_price,
                'interest_rate': interest_rate * 100
            }
        
        # Count affordable products per category
        if self.products_df is not None:
            for category in PRODUCT_CATEGORIES:
                category_products = self.products_df[self.products_df['category'] == category]
                affordable_count = len(category_products[
                    category_products['final_price'] <= insights[category]['max_price']
                ])
                insights[category]['affordable_products'] = affordable_count
        
        return insights


def main():
    """
    Demo recommendation engine
    """
    print("="*60)
    print("Recommendation Engine Demo")
    print("="*60)
    
    # Initialize engine
    engine = RecommendationEngine()
    
    # Sample user profile
    user_profile = {
        'max_emi': 8000,
        'duration': 12,
        'category': 'Electronics',
        'credit_score': 720,
        'monthly_income': 60000,
        'existing_emi': 5000
    }
    
    # Get recommendations
    recommendations = engine.get_recommendations(user_profile, top_n=10)
    
    if len(recommendations) > 0:
        print("\n" + "="*60)
        print("TOP RECOMMENDATIONS")
        print("="*60)
        
        for idx, product in recommendations.iterrows():
            print(f"\n{int(product['rank'])}. {product['product_name']}")
            print(f"   Price: ₹{product['final_price']:,.2f}")
            print(f"   Monthly EMI: ₹{product['monthly_emi']:,.2f}")
            print(f"   Rating: {product['rating']:.1f}⭐")
            print(f"   Affordability Score: {product['affordability_score']:.2f}")
            print(f"   Composite Score: {product['composite_score']:.3f}")
    
    # Get affordability insights
    print("\n" + "="*60)
    print("AFFORDABILITY INSIGHTS")
    print("="*60)
    
    insights = engine.get_affordability_insights(user_profile)
    
    print(f"\nWith ₹{user_profile['max_emi']:,.2f} EMI for {user_profile['duration']} months:\n")
    for category, info in insights.items():
        print(f"{category:.<25} ₹{info['max_price']:>10,.2f} "
              f"(Rate: {info['interest_rate']:.1f}%)")


if __name__ == "__main__":
    main()
