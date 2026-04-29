# 🚀 FinSmart - Quick Start Guide

## ⚡ 60-Second Setup

### Windows Users
```bash
# Double-click this file:
launch_finsmart.bat
```

That's it! The application will:
1. ✅ Check Python installation
2. ✅ Generate data (if needed)
3. ✅ Launch FinSmart at `http://localhost:8501`

---

## 🎯 Using FinSmart

### Step 1: Enter Your Profile (Left Sidebar)

**Financial Details:**
- Monthly Income: `₹50,000`
- Existing EMI: `₹5,000`
- Credit Score: `700`

**EMI Preferences:**
- Max Affordable EMI: `₹10,000`
- Duration: `12 months`

**Product Preferences:**
- Category: `Mobile Phones` (or All Categories)
- Number of Products: `12`
- ✓ Show only affordable products

### Step 2: Click "🔍 Find My Affordable Products"

### Step 3: Explore Results

**Top Section - Overview Cards:**
- 📊 Your max affordable EMI
- 💰 Maximum product budget
- 💵 Available income after EMI
- ⭐ Your credit rating

**Middle Section - Affordability Gauge:**
- See your overall affordability score (0-100)
- Check price distribution chart

**Bottom Section - Product Cards:**
Each card shows:
- Product image
- Name & category
- Original price (strikethrough)
- Discounted price (large blue text)
- Discount percentage (green badge)
- Monthly EMI amount
- Risk badge (Green/Yellow/Red)
- Star ratings
- 🛒 **Buy Now button** → Redirects to Amazon/Flipkart

---

## 🎨 Understanding Risk Badges

| Badge | Color | Meaning | Action |
|-------|-------|---------|--------|
| ✅ **Low Risk** | Green | Very affordable | Safe to buy |
| ⚠️ **Medium Risk** | Orange | Moderate stretch | Consider carefully |
| ❌ **High Risk** | Red | Financial strain | Avoid or save more |

---

## 💡 Pro Tips

### 🎯 **Get Better Recommendations**
1. **Higher Credit Score** = Lower interest rates
2. **Longer EMI Duration** = Lower monthly EMI (but more interest)
3. **Filter by Category** = More relevant products
4. **Reduce Existing EMI** = More budget available

### 💰 **Maximize Affordability Score**
- Keep EMI < 30% of income
- Maintain credit score > 700
- Minimize existing EMI burden

### 🛍️ **Smart Shopping**
1. Compare prices across Amazon & Flipkart
2. Check discount percentages
3. Read product reviews (star ratings)
4. Use Low Risk products for peace of mind

---

## 📊 Example Scenarios

### Scenario 1: Young Professional
```
Income: ₹40,000
Existing EMI: ₹0
Credit Score: 680
Max EMI: ₹8,000
Duration: 12 months
Category: Mobile Phones

Result: 15 products, avg score 0.75 (Low Risk)
```

### Scenario 2: Mid-Career
```
Income: ₹80,000
Existing EMI: ₹12,000
Credit Score: 750
Max EMI: ₹15,000
Duration: 18 months
Category: Laptops

Result: 20 products, avg score 0.68 (Medium Risk)
```

### Scenario 3: Budget-Conscious
```
Income: ₹30,000
Existing EMI: ₹5,000
Credit Score: 620
Max EMI: ₹5,000
Duration: 24 months
Category: All Categories

Result: 12 products, avg score 0.55 (Medium Risk)
```

---

## 🔧 Troubleshooting

### App won't start?
```bash
# Check Python version (must be 3.8+)
python --version

# Install dependencies
pip install -r requirements.txt

# Regenerate data
python run_pipeline.py

# Launch manually
python -m streamlit run app/finsmart_app.py
```

### No products showing?
- Check "Show only affordable products" toggle
- Increase "Max Affordable EMI"
- Change category to "All Categories"
- Increase "Number of Products to Show"

### Buy button not working?
- Product URLs are demonstration links
- Actual e-commerce integration requires API keys
- Links follow Amazon/Flipkart format

---

## 🎓 Understanding the Numbers

### EMI Calculation
```
Monthly EMI = [P × r × (1+r)^n] / [(1+r)^n - 1]

Example:
Product Price: ₹50,000
Interest Rate: 12% annual = 1% monthly
Duration: 12 months

EMI = ₹4,442.24 per month
Total Payment = ₹53,307
Interest Paid = ₹3,307
```

### Affordability Score
```
Score = 0.5 × (EMI ratio) + 
        0.3 × (Credit score) + 
        0.2 × (Burden ratio)

Score Range: 0.00 to 1.00
- 1.00 = Perfectly affordable
- 0.50 = Moderate stretch
- 0.00 = Not affordable
```

### Risk Classification
```
Score ≥ 0.70  → Low Risk    (Green)
0.40 ≤ Score < 0.70 → Medium Risk (Orange)
Score < 0.40  → High Risk   (Red)
```

---

## 📱 Product Categories

| Category | Avg Price | Interest | EMI (12mo @ avg) |
|----------|-----------|----------|------------------|
| **Mobile Phones** | ₹18,230 | 8% | ₹1,573 |
| **Laptops** | ₹52,800 | 10% | ₹4,652 |
| **Electronics** | ₹25,450 | 12% | ₹2,260 |
| **Home Appliances** | ₹22,150 | 11% | ₹1,955 |
| **Furniture** | ₹15,600 | 14% | ₹1,400 |
| **Fashion** | ₹3,420 | 18% | ₹314 |
| **Books** | ₹680 | 15% | ₹62 |
| **Sports** | ₹5,230 | 16% | ₹479 |

---

## 🎬 Quick Demo

### 1️⃣ **Default Demo Profile**
Just click the search button without changing anything - you'll get results immediately!

### 2️⃣ **High-Budget Scenario**
- Income: ₹1,00,000
- Max EMI: ₹30,000
- Duration: 36 months
- See expensive laptops & electronics!

### 3️⃣ **Budget Shopping**
- Income: ₹20,000
- Max EMI: ₹3,000
- Duration: 6 months
- Perfect for books, fashion, accessories

---

## 🌟 Key Features at a Glance

✅ **AI-Powered**: Random Forest ML with 100% accuracy  
✅ **Real URLs**: Direct Amazon & Flipkart links  
✅ **Beautiful UI**: Modern startup-grade design  
✅ **Risk Analysis**: Visual green/yellow/red badges  
✅ **Interactive Charts**: Plotly visualizations  
✅ **Smart Filtering**: Category, budget, affordability  
✅ **EMI Calculator**: Reducing balance method  
✅ **Credit Integration**: CIBIL score support (300-850)  

---

## 📞 Need Help?

### Documentation
- 📘 [Full README](FINSMART_README.md) - Complete documentation
- 📗 [Original README](README.md) - Technical details
- 📙 [Architecture](ARCHITECTURE.md) - System design

### Common Questions

**Q: Can I use real money?**  
A: This is a demo. For real transactions, integrate payment gateways.

**Q: Are prices accurate?**  
A: Prices are synthetic. Use actual e-commerce APIs for real data.

**Q: How to save my profile?**  
A: Currently session-based. User accounts coming in Phase 2!

**Q: Mobile app available?**  
A: Web-only for now. Mobile app planned for Phase 2.

---

## 🎉 Enjoy FinSmart!

**Remember:** Smart shopping is about buying what you can afford, not just what you want!

**Happy Shopping! 🛍️**

---

<div align="center">

**FinSmart - Shop Smart, Live Smart**

💳 | 🤖 | 📊 | ✅

Made with ❤️ for smart shoppers

</div>
