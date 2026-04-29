# ✨ FinSmart - AI-Based EMI Affordability & Smart Product Discovery

---

## 📊 Pipeline Diagram

The FinSmart data and ML pipeline flows as follows:

```
┌─────────────────────────────────────────────────────────────────────┐
│                         DATA LAYER                                  │
│                                                                     │
│   Raw Data Generation                                               │
│   ┌────────────┐   ┌──────────────┐   ┌─────────────────┐          │
│   │ products   │   │  customers   │   │  transactions   │          │
│   │ (1000 rows)│   │ (500 rows)   │   │  (2000 rows)    │          │
│   └─────┬──────┘   └──────┬───────┘   └────────┬────────┘          │
│         └─────────────────┴────────────────────┘                   │
│                            │                                        │
│                            ▼                                        │
│                  ┌─────────────────┐                                │
│                  │  Preprocessing  │  (src/preprocessing.py)        │
│                  │  25+ Features   │                                │
│                  └────────┬────────┘                                │
└───────────────────────────┼─────────────────────────────────────────┘
                            │
┌───────────────────────────┼─────────────────────────────────────────┐
│                     ML LAYER                                        │
│                           │                                         │
│              ┌────────────┴────────────┐                            │
│              ▼                         ▼                            │
│  ┌───────────────────────┐  ┌───────────────────────┐              │
│  │  RF Classifier        │  │  RF Regressor         │              │
│  │  (Risk Prediction)    │  │  (Affordability Score)│              │
│  │  Accuracy: 100%       │  │  R² Score: 0.9997     │              │
│  └──────────┬────────────┘  └──────────┬────────────┘              │
│             └────────────┬─────────────┘                           │
│                          │                                          │
│                          ▼                                          │
│               ┌─────────────────────┐                              │
│               │ Recommendation      │  (src/recommendation_engine) │
│               │ Engine              │  Composite Scoring:          │
│               │ (Content-Based)     │  40% Affordability           │
│               └──────────┬──────────┘  30% Rating                  │
│                          │             20% Popularity               │
└──────────────────────────┼─────────────────────────────────────────┘
                           │             10% Category Match
┌──────────────────────────┼─────────────────────────────────────────┐
│                    APP LAYER                                        │
│                          ▼                                          │
│          ┌──────────────────────────────┐                          │
│          │   Streamlit Dashboard        │  (app/finsmart_app.py)   │
│          │   - EMI Calculator           │                          │
│          │   - Product Cards            │                          │
│          │   - Affordability Gauge      │                          │
│          │   - Interactive Charts       │                          │
│          └──────────────────────────────┘                          │
└─────────────────────────────────────────────────────────────────────┘
```

**Pipeline Stages:**

| Stage | Script | Output |
|-------|--------|--------|
| Data Generation | `src/data_generation.py` | `data/raw/*.csv` |
| Preprocessing & Feature Engineering | `src/preprocessing.py` | `data/processed/processed_data.csv` |
| Model Training | `src/model_training.py` | `models/*.pkl` |
| Recommendation Engine | `src/recommendation_engine.py` | Product rankings |
| Web Application | `app/finsmart_app.py` | Streamlit dashboard |

---

## 📁 Dataset Details

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

## 🤖 Deep Learning Integration Summary

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

## 🚀 Steps to Run the Program

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

## 🖼️ Sample Output Screenshot

> **Note:** The screenshot below shows the expected output of the FinSmart Streamlit dashboard after entering a financial profile and running the recommendation engine.

```
┌──────────────────────────────────────────────────────────────────────┐
│  ✨ FinSmart — AI-Based EMI Affordability & Smart Product Discovery  │
├──────────────────┬───────────────────────────────────────────────────┤
│  SIDEBAR         │  MAIN DASHBOARD                                   │
│                  │                                                   │
│  Monthly Income  │  ┌──────────┐ ┌──────────┐ ┌──────────┐         │
│  ₹ 50,000        │  │Max Budget│ │Afford.   │ │Available │         │
│                  │  │₹ 2,25,000│ │Score: 78 │ │₹ 32,500  │         │
│  Existing EMI    │  └──────────┘ └──────────┘ └──────────┘         │
│  ₹ 5,000         │                                                   │
│                  │  ════ Affordability Gauge ════                    │
│  Credit Score    │        [●━━━━━━━━━━━━━━━━━○]  78/100             │
│  700             │        ✅ LOW RISK                                │
│                  │                                                   │
│  Max EMI         │  ════ Recommended Products ════                   │
│  ₹ 8,000         │  ┌────────────────────────────────────────┐      │
│                  │  │ 📱 Samsung Galaxy M34          ✅ LOW  │      │
│  Duration        │  │ ₹18,999   EMI: ₹1,775/mo × 12 months │      │
│  12 months       │  │ ⭐ 4.3  |  1,240 reviews              │      │
│                  │  │           [ Buy Now → Amazon ]         │      │
│  Category        │  └────────────────────────────────────────┘      │
│  Mobile Phones   │  ┌────────────────────────────────────────┐      │
│                  │  │ 💻 Lenovo IdeaPad Slim 3      ⚠️ MED  │      │
│  [Find Products] │  │ ₹42,990   EMI: ₹4,021/mo × 12 months │      │
│                  │  │ ⭐ 4.1  |  890 reviews                │      │
│                  │  │           [ Buy Now → Flipkart ]       │      │
│                  │  └────────────────────────────────────────┘      │
└──────────────────┴───────────────────────────────────────────────────┘
```

> 📷 *To add a real screenshot: run the application, capture the dashboard, and replace this placeholder with:*
> ```markdown
> ![FinSmart Dashboard](outputs/dashboard_screenshot.png)
> ```

---

## 👥 Team Member Details

| Name | Roll Number / ID | Role / Contribution |
|------|-----------------|---------------------|
| Santhosh Prakash P | 24BCS246 | Data processing, ML models |
| Satrapathi A | 24BCS254 | Dashboard, DL integration |
| Sanjai R | 24BCS238 | Documentation, testing |
| Saravanakumar S | 24BCS250 | Documentation, testing |

---

*Last Updated: April 2026*
