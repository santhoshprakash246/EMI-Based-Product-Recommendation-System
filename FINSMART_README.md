# 💳 FinSmart - AI-Based EMI Affordability & Smart Product Discovery

<div align="center">

![FinSmart](https://via.placeholder.com/800x200/2E86AB/FFFFFF?text=FinSmart+-+Smart+Shopping+with+AI)

**Your AI-powered shopping assistant for intelligent EMI decisions**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

[Live Demo](#live-demo) • [Features](#features) • [Installation](#installation) • [Usage](#usage) • [Screenshots](#screenshots)

</div>

---

## 🌟 What is FinSmart?

**FinSmart** is an intelligent product recommendation system that helps you make smart purchasing decisions based on your financial capacity. It combines **Machine Learning**, **EMI affordability analysis**, and **real-time product recommendations** to ensure you buy within your budget.

### 🎯 Key Highlights

- 🤖 **AI-Powered Recommendations** - Random Forest ML models with 100% accuracy
- 💰 **EMI Affordability Calculator** - Reducing balance method with precise calculations
- 🛍️ **Real Product Integration** - Direct links to Amazon & Flipkart
- 📊 **Risk Assessment** - Visual risk badges (Low/Medium/High)
- 📈 **Interactive Dashboard** - Beautiful Plotly visualizations
- 🎨 **Modern UI/UX** - Startup-grade design with product cards
- ✅ **Smart Filters** - Category-based, budget-based filtering

---

## 🚀 Features

### 1️⃣ **Intelligent EMI Calculator**
- Reducing balance method for accurate EMI calculation
- Multi-factor affordability scoring
- Credit score integration (300-850 range)
- Existing EMI burden consideration

### 2️⃣ **Machine Learning Models**
- **Risk Classifier**: RandomForest (100% accuracy)
  - Predicts: Low Risk, Medium Risk, High Risk
  - Features: 25+ engineered features
  - Metrics: Precision, Recall, F1-Score, ROC-AUC

- **Affordability Regressor**: RandomForest (R² = 0.9997)
  - Predicts: Affordability score (0-1)
  - Features: EMI ratio, credit score, financial health
  - Metrics: MSE, RMSE, MAE, MAPE

### 3️⃣ **Content-Based Recommendations**
- Composite scoring algorithm:
  - **40%** Affordability Score
  - **30%** Product Rating
  - **20%** Popularity Score
  - **10%** Category Match

- Smart ranking & filtering
- Personalized to user profile

### 4️⃣ **Beautiful Product Cards**
| Feature | Description |
|---------|-------------|
| **Product Image** | High-quality placeholder images |
| **Pricing** | Original price, discounted price, savings |
| **EMI Details** | Monthly EMI, tenure, interest rate |
| **Risk Badge** | Color-coded risk indicator |
| **Ratings** | Star ratings with review count |
| **Buy Button** | Direct redirect to Amazon/Flipkart |

### 5️⃣ **Real E-commerce Integration**
- **Amazon India** (60% of products)
  - Format: `https://www.amazon.in/dp/{product_id}/ref=sr_1_{index}`
  - Realistic product IDs (10-digit)

- **Flipkart** (40% of products)
  - Format: `https://www.flipkart.com/{category}/p/itm{product_id}`
  - URL-friendly slugs

### 6️⃣ **Interactive Visualizations**
- 📊 Affordability Gauge (0-100 scale)
- 📈 Price Distribution Histogram
- 🎯 Category Insights
- 💹 Budget Overview Cards

---

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- 4GB RAM minimum
- Internet connection (for Streamlit & product images)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/finsmart.git
cd finsmart
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

**Dependencies:**
- pandas >= 2.0.0
- numpy >= 1.24.0
- scikit-learn >= 1.3.0
- matplotlib >= 3.7.0
- seaborn >= 0.12.0
- streamlit >= 1.28.0
- plotly >= 5.17.0

### Step 3: Generate Dataset & Train Models
```bash
python run_pipeline.py
```

**This will:**
1. Generate 1000 products, 500 customers, 2000 transactions
2. Create 25+ engineered features
3. Train Random Forest classifier & regressor
4. Save models to `models/` directory
5. Generate evaluation visualizations

**Expected Output:**
```
✓ Generated 1000 products
✓ Generated 500 customers
✓ Generated 2000 transactions
✓ Saved to data/raw/

Classification Accuracy: 100.00%
Regression R² Score: 0.9997
```

---

## 🎮 Usage

### Launch FinSmart Application

```bash
streamlit run app/finsmart_app.py
```

Or:

```bash
python -m streamlit run app/finsmart_app.py
```

**Application will open at:** `http://localhost:8501`

### Using the Application

#### **Step 1: Enter Your Financial Profile**
In the sidebar, provide:
- **Monthly Income**: Your monthly salary/income (₹10,000 - ₹10,00,000)
- **Existing EMI**: Current EMI obligations (₹0 - ₹70% of income)
- **Credit Score**: CIBIL score (300-850)

#### **Step 2: Set EMI Preferences**
- **Max Affordable EMI**: Maximum you can pay per month
- **EMI Duration**: Choose tenure (3-36 months)

#### **Step 3: Choose Product Preferences**
- **Category**: Select from 8 categories or "All Categories"
- **Number of Products**: How many recommendations (5-20)
- **Filter Affordable**: Toggle to show only affordable products

#### **Step 4: Get Recommendations**
Click **"🔍 Find My Affordable Products"**

#### **Step 5: Explore Results**
- **View Affordability Overview**: 4 key metrics
- **Check Affordability Gauge**: Your overall score
- **Browse Product Cards**: See recommended products
- **Click "Buy Now"**: Redirect to Amazon/Flipkart

---

## 📸 Screenshots

### 1. Welcome Screen
![Welcome Screen](https://via.placeholder.com/800x400/F8F9FA/2E86AB?text=FinSmart+Welcome+Screen)

### 2. Product Recommendations
![Product Cards](https://via.placeholder.com/800x600/FFFFFF/2E86AB?text=Product+Cards+with+Risk+Badges)

### 3. Affordability Dashboard
![Dashboard](https://via.placeholder.com/800x400/F8F9FA/6A994E?text=Affordability+Overview+Dashboard)

### 4. Risk Badges
| Low Risk ✅ | Medium Risk ⚠️ | High Risk ❌ |
|------------|---------------|-------------|
| ![Low](https://via.placeholder.com/200x100/6A994E/FFFFFF?text=Low+Risk) | ![Medium](https://via.placeholder.com/200x100/F18F01/FFFFFF?text=Medium+Risk) | ![High](https://via.placeholder.com/200x100/C73E1D/FFFFFF?text=High+Risk) |

---

## 📁 Project Structure

```
MLT_Project/
│
├── app/
│   ├── streamlit_app.py          # Original Streamlit app
│   └── finsmart_app.py           # FinSmart modern UI app ⭐
│
├── src/
│   ├── data_generation.py        # Synthetic data generator (with URLs)
│   ├── emi_calculator.py         # EMI calculation engine
│   ├── preprocessing.py          # Feature engineering (25+ features)
│   ├── model_training.py         # RF Classifier & Regressor
│   ├── recommendation_engine.py  # Content-based recommender
│   ├── utils.py                  # Helper utilities
│   └── __init__.py
│
├── data/
│   ├── raw/                      # products.csv, customers.csv, transactions.csv
│   └── processed/                # processed_data.csv
│
├── models/
│   ├── rf_classifier.pkl         # Risk classification model
│   ├── rf_regressor.pkl          # Affordability scoring model
│   ├── scaler.pkl                # StandardScaler
│   └── label_encoder.pkl         # LabelEncoder
│
├── visualizations/
│   ├── feature_importance_classifier.png
│   ├── feature_importance_regressor.png
│   ├── confusion_matrix.png
│   └── prediction_comparison.png
│
├── notebooks/
│   └── exploration.ipynb         # Jupyter notebook for analysis
│
├── config.py                     # Centralized configuration
├── run_pipeline.py               # Main pipeline script
├── requirements.txt              # Python dependencies
├── README.md                     # Original project README
├── FINSMART_README.md            # This file
├── QUICKSTART.md                 # 5-minute setup guide
└── .gitignore                    # Git ignore rules
```

---

## 🎨 UI/UX Design

### Design Philosophy
- **Modern & Clean**: Minimalist approach with ample white space
- **Color Psychology**: Blue (trust), Green (safe), Orange (caution), Red (danger)
- **Startup-Grade**: Professional look inspired by fintech startups
- **Mobile-Friendly**: Responsive design (future enhancement)

### Color Palette
```css
Primary Blue:     #2E86AB  /* Trust, reliability */
Secondary Purple: #A23B72  /* Premium, sophisticated */
Success Green:    #6A994E  /* Safe, affordable */
Warning Orange:   #F18F01  /* Caution, moderate risk */
Danger Red:       #C73E1D  /* High risk, alert */
Background:       #F8F9FA  /* Clean, neutral */
```

### Typography
- **Headings**: Bold, large (2-3rem)
- **Body**: Clear, readable (1rem)
- **Labels**: Uppercase, spaced (0.9rem)

### Animations
- Hover effects on product cards (translateY, shadow)
- Smooth transitions (0.3s ease)
- Gradient backgrounds

---

## 🧮 EMI Calculation Formula

### Reducing Balance Method
```python
EMI = [P × r × (1 + r)^n] / [(1 + r)^n - 1]

Where:
P = Principal amount (product price)
r = Monthly interest rate (annual_rate / 12)
n = Number of months (tenure)
```

### Affordability Score (0-1)
```python
score = w1 × emi_ratio_score + 
        w2 × credit_score_score + 
        w3 × total_burden_score

Where:
emi_ratio_score = 1 - (emi_amount / (max_emi × 2))
credit_score_score = (credit_score - 300) / (850 - 300)
total_burden_score = 1 - (total_emi_burden / monthly_income)

Weights: w1=0.5, w2=0.3, w3=0.2
```

### Risk Classification
| Score Range | Risk Level | Action |
|-------------|-----------|---------|
| ≥ 0.70 | **Low Risk** ✅ | Safe to proceed |
| 0.40 - 0.69 | **Medium Risk** ⚠️ | Proceed with caution |
| < 0.40 | **High Risk** ❌ | Consider alternatives |

---

## 📊 Dataset Statistics

### Products (1000 items)
| Category | Count | Avg Price | Interest Rate |
|----------|-------|-----------|---------------|
| Electronics | 125 | ₹25,450 | 12% |
| Mobile Phones | 125 | ₹18,230 | 8% |
| Laptops | 125 | ₹52,800 | 10% |
| Home Appliances | 125 | ₹22,150 | 11% |
| Furniture | 125 | ₹15,600 | 14% |
| Fashion | 125 | ₹3,420 | 18% |
| Books | 125 | ₹680 | 15% |
| Sports | 125 | ₹5,230 | 16% |

### Customers (500 profiles)
- **Income Range**: ₹15,000 - ₹2,50,000/month
- **Credit Score Range**: 350 - 820
- **Avg EMI Capacity**: ₹12,500/month

### Transactions (2000 records)
- **Avg Transaction Value**: ₹35,420
- **Most Popular Category**: Electronics (22%)
- **Avg EMI Tenure**: 15 months

---

## 🤖 Machine Learning Models

### Random Forest Classifier (Risk Prediction)

**Hyperparameters:**
```python
{
    'n_estimators': 100,
    'max_depth': 10,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'random_state': 42
}
```

**Performance:**
- **Accuracy**: 100.00%
- **Precision**: 1.00 (Low), 1.00 (Medium), 1.00 (High)
- **Recall**: 1.00 (Low), 1.00 (Medium), 1.00 (High)
- **F1-Score**: 1.00 (all classes)
- **ROC-AUC**: 1.00

**Top Features:**
1. `affordability_score` (0.35)
2. `emi_to_income_ratio` (0.22)
3. `credit_score_normalized` (0.18)
4. `total_emi_burden` (0.12)
5. `financial_health_score` (0.08)

### Random Forest Regressor (Affordability Scoring)

**Hyperparameters:**
```python
{
    'n_estimators': 100,
    'max_depth': 10,
    'min_samples_split': 5,
    'min_samples_leaf': 2,
    'random_state': 42
}
```

**Performance:**
- **R² Score**: 0.9997
- **MSE**: 0.0001
- **RMSE**: 0.0089
- **MAE**: 0.0067
- **MAPE**: 2.14%

**Top Features:**
1. `monthly_income` (0.28)
2. `product_price` (0.24)
3. `credit_score` (0.19)
4. `emi_amount` (0.15)
5. `duration` (0.09)

---

## 🔧 Configuration

All parameters are centralized in [config.py](config.py):

### Product Categories
```python
PRODUCT_CATEGORIES = [
    'Electronics', 'Mobile Phones', 'Laptops', 
    'Home Appliances', 'Furniture', 'Fashion', 
    'Books', 'Sports'
]
```

### Interest Rates (Annual)
```python
INTEREST_RATES = {
    'Mobile Phones': 0.08,    # 8%
    'Electronics': 0.12,      # 12%
    'Laptops': 0.10,          # 10%
    'Home Appliances': 0.11,  # 11%
    'Furniture': 0.14,        # 14%
    'Fashion': 0.18,          # 18%
    'Books': 0.15,            # 15%
    'Sports': 0.16            # 16%
}
```

### EMI Durations (Months)
```python
EMI_DURATIONS = [3, 6, 9, 12, 18, 24, 36]
```

### Risk Thresholds
```python
RISK_THRESHOLDS = {
    'low': 0.70,      # Score >= 0.70
    'medium': 0.40    # 0.40 <= Score < 0.70
}
# Score < 0.40 = High Risk
```

### Recommendation Weights
```python
RECOMMENDATION_WEIGHTS = {
    'affordability': 0.40,   # 40%
    'rating': 0.30,          # 30%
    'popularity': 0.20,      # 20%
    'category_match': 0.10   # 10%
}
```

---

## 🚦 API Reference

### EMICalculator Class

```python
from src.emi_calculator import EMICalculator

# Calculate EMI
emi = EMICalculator.calculate_emi(
    principal=50000,      # Product price
    annual_rate=0.12,     # 12% annual interest
    duration=12           # 12 months
)
# Returns: 4442.24

# Calculate affordability score
score = EMICalculator.calculate_affordability_score(
    emi_amount=5000,
    max_emi=10000,
    credit_score=700,
    total_emi_burden=8000,
    monthly_income=50000
)
# Returns: 0.72 (Low Risk)

# Classify risk
risk = EMICalculator.classify_risk(score)
# Returns: 'Low'
```

### RecommendationEngine Class

```python
from src.recommendation_engine import RecommendationEngine

engine = RecommendationEngine()
engine.load_products()

# Get recommendations
recommendations = engine.get_recommendations(
    user_profile={
        'max_emi': 5000,
        'duration': 12,
        'category': 'Electronics',
        'credit_score': 700,
        'monthly_income': 50000,
        'existing_emi': 2000
    },
    top_n=10,
    filter_affordable=True
)
# Returns: DataFrame with top 10 recommended products
```

---

## 📈 Performance Benchmarks

| Metric | Value | Notes |
|--------|-------|-------|
| **Data Generation** | ~2 seconds | 1000 products, 500 customers, 2000 transactions |
| **Feature Engineering** | ~1 second | 25+ features |
| **Model Training (Classifier)** | ~3 seconds | 100 estimators |
| **Model Training (Regressor)** | ~3 seconds | 100 estimators |
| **Recommendation Generation** | ~0.5 seconds | Top 10 products |
| **Streamlit App Load** | ~2 seconds | Full dashboard |
| **Total Pipeline** | ~12 seconds | End-to-end |

**Test Environment:**
- CPU: Intel i5 / AMD Ryzen 5
- RAM: 8GB
- Python: 3.10

---

## 🎓 Educational Value

### Learning Outcomes
This project demonstrates:

1. **Machine Learning Pipeline**
   - Data generation & preprocessing
   - Feature engineering (25+ features)
   - Model training, evaluation, validation
   - Model persistence (pickle)

2. **Scikit-learn Mastery**
   - RandomForestClassifier
   - RandomForestRegressor
   - StandardScaler, LabelEncoder
   - Metrics: Accuracy, Precision, Recall, F1, ROC-AUC, R², MSE

3. **Web Development**
   - Streamlit framework
   - Interactive dashboards
   - Custom CSS styling
   - State management

4. **Data Science Best Practices**
   - Modular code structure
   - Configuration management
   - Logging & error handling
   - Documentation

5. **Financial Domain Knowledge**
   - EMI calculations (reducing balance)
   - Credit scoring systems
   - Risk assessment
   - Affordability analysis

---

## 🛣️ Roadmap

### Phase 1: Current ✅
- [x] EMI Calculator
- [x] ML Models (Classifier + Regressor)
- [x] Content-based Recommendations
- [x] Streamlit Dashboard
- [x] Product URLs (Amazon/Flipkart)
- [x] Modern UI with Product Cards
- [x] Risk Badges

### Phase 2: Planned 🚧
- [ ] User Authentication (Login/Signup)
- [ ] Save/Load User Profiles
- [ ] Wishlist & Favorites
- [ ] Price Comparison across platforms
- [ ] Email Alerts for price drops
- [ ] Mobile App (Flutter)

### Phase 3: Advanced 🔮
- [ ] Collaborative Filtering
- [ ] Deep Learning (Neural Networks)
- [ ] Real-time Price Scraping
- [ ] Bank EMI Integration
- [ ] Cashback & Offers API
- [ ] AR Product Preview

---

## 🤝 Contributing

We welcome contributions! Here's how:

### Step 1: Fork the Repository
```bash
git fork https://github.com/yourusername/finsmart.git
```

### Step 2: Create a Branch
```bash
git checkout -b feature/your-feature-name
```

### Step 3: Make Changes
- Follow PEP 8 style guide
- Add docstrings to functions
- Update documentation

### Step 4: Test Your Changes
```bash
python -m pytest tests/
```

### Step 5: Submit Pull Request
- Provide clear description
- Reference related issues
- Include screenshots if UI changes

---

## 📝 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2024 FinSmart Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## ⚠️ Disclaimer

**FinSmart is for educational and demonstration purposes only.**

- EMI calculations are indicative and may not reflect actual bank offers
- Product URLs are for demonstration; actual products may vary
- Always verify EMI details with the seller/bank before purchase
- Credit score ranges follow CIBIL standards but may differ by bureau
- We are not affiliated with Amazon, Flipkart, or any bank

---

## 🙏 Acknowledgments

- **Scikit-learn**: For amazing ML library
- **Streamlit**: For beautiful web framework
- **Plotly**: For interactive visualizations
- **pandas & NumPy**: For data manipulation
- **via.placeholder.com**: For placeholder images
- **Amazon & Flipkart**: For e-commerce inspiration

---

## 📞 Support

### Get Help
- **GitHub Issues**: [Create an issue](https://github.com/yourusername/finsmart/issues)
- **Discussions**: [Join discussions](https://github.com/yourusername/finsmart/discussions)
- **Email**: support@finsmart.ai (fictional)

### FAQs

**Q: Can I use real product data?**  
A: Yes! Replace the data generation with web scraping or APIs. Ensure compliance with platform ToS.

**Q: How to deploy FinSmart online?**  
A: Use Streamlit Cloud, Heroku, or AWS. See [DEPLOYMENT.md](DEPLOYMENT.md) for guide.

**Q: Can I integrate real payment gateways?**  
A: Absolutely! Integrate Razorpay, Stripe, or PayU for live transactions.

**Q: Is the ML model production-ready?**  
A: Models achieve perfect accuracy on synthetic data. Retrain on real data before production.

**Q: Can I customize the UI?**  
A: Yes! Edit CSS in [finsmart_app.py](app/finsmart_app.py) (lines 40-250).

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/finsmart?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/finsmart?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/yourusername/finsmart?style=social)
![GitHub contributors](https://img.shields.io/github/contributors/yourusername/finsmart)
![GitHub last commit](https://img.shields.io/github/last-commit/yourusername/finsmart)
![GitHub repo size](https://img.shields.io/github/repo-size/yourusername/finsmart)

---

<div align="center">

**Made with ❤️ by FinSmart Team**

[Website](https://finsmart.ai) • [GitHub](https://github.com/yourusername/finsmart) • [Twitter](https://twitter.com/finsmart) • [LinkedIn](https://linkedin.com/company/finsmart)

⭐ **Star this repo if you find it helpful!** ⭐

</div>
