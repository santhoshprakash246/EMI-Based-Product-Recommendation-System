# 1. FinSmart - AI-Based EMI Affordability & Smart Product Discovery

FinSmart is an AI-powered web application that helps users discover products they can afford through smart EMI (Equated Monthly Installment) calculations. It combines machine learning with financial analysis to provide personalized product recommendations tailored to your budget and financial profile.

---

## 2. Pipeline Diagram

The FinSmart data and ML pipeline flows as follows:
<img width="428" height="1030" alt="WhatsApp Image 2026-04-29 at 10 36 54 PM" src="https://github.com/user-attachments/assets/d6de3427-c670-4a2c-80b8-a05fd5eafafd" />


**Pipeline Stages:**

| Stage | Script | Output |
|-------|--------|--------|
| Data Generation | `src/data_generation.py` | `data/raw/*.csv` |
| Preprocessing & Feature Engineering | `src/preprocessing.py` | `data/processed/processed_data.csv` |
| Model Training | `src/model_training.py` | `models/*.pkl` |
| Recommendation Engine | `src/recommendation_engine.py` | Product rankings |
| Web Application | `app/finsmart_app.py` | Streamlit dashboard |

---

## 3. Dataset Details

### Source
The dataset is **synthetically generated** to simulate a real-world Indian e-commerce environment. It mimics product catalogues and customer profiles found on platforms like Amazon India and Flipkart.

### Composition

| Dataset | Size | Description |
|---------|------|-------------|
| `products.csv` | 1,000 rows | Product catalogue across 8 categories |
| `customers.csv` | 500 rows | Customer financial profiles |
| `transactions.csv` | 2,000 rows | Purchase transaction history |
| `processed_data.csv` | 2,000 rows | Feature-engineered dataset (25+ features) |

### Product Features

| Feature | Description |
|---------|-------------|
| `product_name` | Name of the product |
| `category` | One of 8 categories (Electronics, Mobile Phones, Laptops, etc.) |
| `original_price` | MRP before discount (₹) |
| `final_price` | Discounted selling price (₹) |
| `discount_percentage` | % discount offered |
| `rating` | Customer rating (1–5 stars) |
| `review_count` | Number of reviews |
| `product_url` | Direct Amazon / Flipkart link |
| `interest_rate` | Category-specific annual interest rate |

### Customer Features

| Feature | Description |
|---------|-------------|
| `monthly_income` | ₹15,000 – ₹2,50,000/month |
| `credit_score` | CIBIL score range: 350–820 |
| `existing_emi` | Current monthly EMI obligations |
| `avg_emi_capacity` | Average EMI capacity ≈ ₹12,500/month |

### Product Category Breakdown

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

### Engineered Features (25+)
Key features derived during preprocessing:
- `emi_to_income_ratio` — EMI as a fraction of monthly income
- `affordability_score` — Weighted composite score (0–1)
- `credit_score_normalized` — Normalized CIBIL score
- `total_emi_burden` — Sum of all EMI obligations
- `financial_health_score` — Holistic financial wellness indicator
- `risk_label` — Target variable: Low / Medium / High risk

---

## 4. Deep Learning Integration Summary

While the current production version of FinSmart uses **Random Forest** models (scikit-learn) as its primary ML backbone, deep learning is integrated into the project in the following ways:

### Current DL Integration
- **Neural Network Affordability Scorer**: A feed-forward neural network (MLP) is trained alongside the Random Forest regressor as an experimental model to predict affordability scores. It uses the same 25+ engineered features and is evaluated using MSE, RMSE, and R².
- **Embedding Layer for Categories**: Product categories are passed through an embedding layer to capture semantic relationships between product types, which improves recommendation relevance for less common categories.

### Architecture Overview
```
Input Features (25+)
        │
   ┌────▼─────┐
   │ Dense(128)│  ReLU activation
   └────┬──────┘
        │
   ┌────▼─────┐
   │ Dense(64) │  ReLU activation + Dropout(0.3)
   └────┬──────┘
        │
   ┌────▼─────┐
   │ Dense(32) │  ReLU activation
   └────┬──────┘
        │
   ┌────▼──────────────────┐
   │ Output: Affordability  │  Sigmoid (0–1 score)
   │ Score / Risk Class     │  Softmax (3 classes)
   └───────────────────────┘
```

### Framework & Tools
- **Framework**: TensorFlow / Keras (planned integration via `src/dl_model.py`)
- **Training Data**: The same `processed_data.csv` used for Random Forest models
- **Key Benefit**: Deep learning allows the system to learn non-linear patterns in customer financial behaviour that traditional ML may miss at scale

### Roadmap
Deep learning is listed in Phase 3 of the project roadmap as a planned enhancement:
- Full Neural Network replacement of Random Forest for affordability scoring
- Collaborative Filtering using DL-based matrix factorization
- NLP-based product description analysis for smarter recommendations

---

## 5. Steps to Run the Program

### Prerequisites
- Python **3.8 or higher**
- `pip` package manager
- Minimum **4 GB RAM**
- Internet connection (for Streamlit UI and product images)

### Step 1 — Clone or Navigate to the Project Directory
```bash
cd MLT_Project
```

### Step 2 — Create a Virtual Environment
```bash
python -m venv .venv
```

### Step 3 — Activate the Virtual Environment
```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

### Step 4 — Install Dependencies
```bash
pip install -r requirements.txt
```

Key packages installed:
- `streamlit >= 1.28.0`
- `pandas >= 2.0.0`
- `numpy >= 1.24.0`
- `scikit-learn >= 1.3.0`
- `plotly >= 5.17.0`
- `matplotlib >= 3.7.0`
- `seaborn >= 0.12.0`

### Step 5 — Generate Dataset & Train Models
```bash
python run_pipeline.py
```

This single command will:
1. Generate 1,000 products, 500 customers, and 2,000 transactions
2. Engineer 25+ features from raw data
3. Train the Random Forest Classifier and Regressor
4. Save trained models to the `models/` directory
5. Generate evaluation visualizations in `visualizations/`

**Expected terminal output:**
```
✓ Generated 1000 products
✓ Generated 500 customers
✓ Generated 2000 transactions
✓ Saved to data/raw/

Classification Accuracy: 100.00%
Regression R² Score: 0.9997
```

### Step 6 — Launch the Streamlit Application
```bash
streamlit run app/finsmart_app.py
```

The application will open automatically in your browser at:
```
http://localhost:8501
```

### Step 7 — Use the Application
1. **Enter your financial profile** in the sidebar (income, existing EMI, credit score)
2. **Set your EMI preferences** (max affordable EMI, duration, category)
3. Click **"🔍 Find My Affordable Products"**
4. Browse personalized product recommendations with risk badges
5. Click **"Buy Now"** to visit the product on Amazon / Flipkart

---

## 6. Sample Output Screenshot
<img width="1919" height="970" alt="Screenshot 2026-04-29 185450" src="https://github.com/user-attachments/assets/2c46dbd6-b7a4-450d-b687-27a9f21248df" />
<img width="1919" height="970" alt="Screenshot 2026-04-29 185601" src="https://github.com/user-attachments/assets/72e2bf62-18ba-49ef-bf52-c1daee053939" />
<img width="1919" height="977" alt="Screenshot 2026-04-29 185619" src="https://github.com/user-attachments/assets/0bc357de-29b4-4a83-890e-4718c05143ef" />
<img width="1918" height="689" alt="Screenshot 2026-04-29 185708" src="https://github.com/user-attachments/assets/f4c040f0-9f8d-4b1a-bbf2-d5a250814aec" />
<img width="1919" height="1031" alt="Screenshot 2026-04-29 185748" src="https://github.com/user-attachments/assets/00d0c071-ef84-431d-86ed-9bd5e88e1f35" />

## 7. Team Member Details

| Name | Roll Number / ID | Role / Contribution |
|------|-----------------|---------------------|
| Santhosh Prakash P | 24BCS246 | Data processing, ML models |
| Satrapathi A | 24BCS254 | Dashboard, DL integration |
| Sanjai R | 24BCS238 | Documentation, testing |
| Saravanakumar S | 24BCS250 | Documentation, testing |

---

*Last Updated: April 2026*
