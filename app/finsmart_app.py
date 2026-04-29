"""
FinSmart - AI-Based EMI Affordability & Smart Product Discovery System
🚀 Enhanced Modern Web Application with Premium UI/UX
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import sys
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import *
from src.emi_calculator import EMICalculator
from src.recommendation_engine import RecommendationEngine


# ============================================
# PAGE CONFIGURATION
# ============================================

st.set_page_config(
    page_title="FinSmart - Smart Product Discovery",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# ENHANCED CUSTOM CSS STYLING WITH RICH GRADIENTS & HIGH CONTRAST
# ============================================

st.markdown("""
    <style>
    /* Deep Rich Color Scheme with Texture & High Contrast */
    :root {
        --primary: #FFD700;
        --primary-light: #FFF700;
        --secondary: #FF6B9D;
        --success: #00FF88;
        --warning: #FFA500;
        --error: #FF4444;
        --info: #00D4FF;
        --dark: #0f0c29;
        --dark-mid: #302b63;
        --dark-light: #24243e;
        --text-primary: #FFFFFF;
        --text-secondary: #E0E0E0;
        --text-accent: #FFD700;
    }
    
    * {
        font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Texture overlay pattern using CSS */
    @keyframes grain {
        0% { background-position: 0 0; }
        100% { background-position: 100% 100%; }
    }
    
    /* ===== MAIN LAYOUT WITH RICH GRADIENT BACKGROUND ===== */
    .main {
        background: 
            linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%),
            repeating-linear-gradient(
                0deg,
                rgba(255, 215, 0, 0.03) 0px,
                rgba(255, 215, 0, 0.03) 1px,
                transparent 1px,
                transparent 3px
            );
        background-size: cover, 3px 3px;
        background-attachment: fixed;
        min-height: 100vh;
        position: relative;
    }
    
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(255, 107, 157, 0.08) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(0, 212, 255, 0.08) 0%, transparent 50%);
        pointer-events: none;
        z-index: 0;
    }
    
    /* ===== HEADER WITH VIBRANT GRADIENT ===== */
    .main-header {
        background: 
            linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%),
            repeating-linear-gradient(
                45deg,
                rgba(255, 215, 0, 0.05) 0px,
                rgba(255, 215, 0, 0.05) 2px,
                transparent 2px,
                transparent 4px
            );
        background-size: cover, 8px 8px;
        padding: 4rem 2rem;
        border-radius: 20px;
        text-align: center;
        color: #FFFFFF;
        margin-bottom: 3rem;
        box-shadow: 
            0 20px 48px rgba(255, 107, 157, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        position: relative;
        overflow: hidden;
        border: 2px solid rgba(255, 215, 0, 0.2);
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200px;
        height: 200px;
        background: rgba(255, 107, 157, 0.15);
        border-radius: 50%;
        animation: float 6s ease-in-out infinite;
    }
    
    .main-header::after {
        content: '';
        position: absolute;
        bottom: -30%;
        left: -30%;
        width: 250px;
        height: 250px;
        background: rgba(0, 212, 255, 0.1);
        border-radius: 50%;
        animation: float 8s ease-in-out infinite reverse;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-20px); }
    }
    
    .main-header h1 {
        font-size: 3.5rem;
        font-weight: 900;
        margin: 0;
        color: #FFFFFF;
        text-shadow: 
            0 2px 10px rgba(255, 107, 157, 0.5),
            0 0 20px rgba(0, 212, 255, 0.3);
        letter-spacing: -0.5px;
        position: relative;
        z-index: 1;
    }
    
    .main-header .subtitle {
        font-size: 1.2rem;
        margin: 0.8rem 0 0 0;
        color: #E0E0E0;
        letter-spacing: 0.3px;
        font-weight: 300;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.5);
        position: relative;
        z-index: 1;
    }
    
    .main-header .tagline {
        font-size: 0.95rem;
        margin-top: 1rem;
        color: #FFD700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.5);
        position: relative;
        z-index: 1;
    }
    
    /* ===== CARDS WITH HIGH CONTRAST ===== */
    .card {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.95), rgba(22, 33, 62, 0.95));
        border-radius: 16px;
        padding: 1.75rem;
        box-shadow: 0 8px 32px rgba(255, 107, 157, 0.2), inset 0 1px 0 rgba(255, 215, 0, 0.1);
        border: 2px solid rgba(255, 215, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        color: #E0E0E0;
    }
    
    .card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 48px rgba(255, 107, 157, 0.35);
        border-color: rgba(255, 215, 0, 0.6);
        background: linear-gradient(135deg, rgba(26, 26, 46, 1), rgba(22, 33, 62, 1));
    }
    
    /* Product Card - High Contrast */
    .product-card {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.98), rgba(22, 33, 62, 0.98));
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0, 212, 255, 0.15), inset 0 1px 0 rgba(255, 215, 0, 0.15);
        border: 2px solid rgba(255, 215, 0, 0.4);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .product-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 50px rgba(255, 107, 157, 0.4), inset 0 1px 0 rgba(0, 255, 136, 0.1);
        border-color: rgba(255, 215, 0, 0.7);
        background: linear-gradient(135deg, rgba(26, 26, 46, 1), rgba(15, 52, 96, 1));
    }
    
    .product-header {
        padding: 1.5rem;
        background: linear-gradient(135deg, rgba(22, 33, 62, 0.8), rgba(15, 52, 96, 0.8));
        border-bottom: 2px solid rgba(255, 215, 0, 0.2);
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
    }
    
    .product-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #FFFFFF;
        margin: 0;
        line-height: 1.4;
        text-shadow: 0 2px 8px rgba(0, 0, 0, 0.6);
    }
    
    .product-category {
        background: linear-gradient(135deg, #FF6B9D, #FFB347);
        color: #FFFFFF;
        padding: 0.5rem 1.2rem;
        border-radius: 24px;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(255, 107, 157, 0.5);
        flex-shrink: 0;
        margin-left: 1rem;
        text-shadow: 0 1px 4px rgba(0, 0, 0, 0.3);
    }
    
    .product-image {
        width: 100%;
        height: 320px;
        object-fit: cover;
        background: linear-gradient(135deg, rgba(22, 33, 62, 0.6), rgba(15, 52, 96, 0.6));
        border-bottom: 2px solid rgba(255, 215, 0, 0.2);
    }
    
    .product-content {
        padding: 1.5rem;
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.9), rgba(22, 33, 62, 0.9));
    }
    
    .rating-section {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        margin-bottom: 1.2rem;
        padding-bottom: 1.2rem;
        border-bottom: 2px solid rgba(255, 215, 0, 0.2);
    }
    
    .rating-stars {
        color: #FFD700;
        font-size: 1.2rem;
        letter-spacing: 2px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    .rating-count {
        color: #E0E0E0;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .price-section {
        display: flex;
        align-items: center;
        gap: 1.2rem;
        margin: 1.5rem 0;
        padding: 1.2rem;
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.6), rgba(22, 33, 62, 0.6));
        border-radius: 12px;
        border-left: 4px solid #FFD700;
    }
    
    .price-original {
        text-decoration: line-through;
        color: #A0A0A0;
        font-size: 1rem;
        font-weight: 500;
    }
    
    .price-final {
        font-size: 2.2rem;
        font-weight: 900;
        color: #FFD700;
        text-shadow: 0 2px 8px rgba(255, 215, 0, 0.4);
    }
    
    .discount-badge {
        background: linear-gradient(135deg, #00FF88, #00DD88);
        color: #000000;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(0, 255, 136, 0.5);
        margin-left: auto;
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
    }
    
    .emi-info {
        background: linear-gradient(135deg, rgba(30, 50, 100, 0.4), rgba(22, 33, 62, 0.4));
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #00D4FF;
        margin: 1.5rem 0;
    }
    
    .emi-label {
        font-size: 0.85rem;
        color: #E0E0E0;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.4rem;
    }
    
    .emi-amount {
        font-size: 1.8rem;
        font-weight: 900;
        color: #FFD700;
        text-shadow: 0 2px 8px rgba(255, 215, 0, 0.4);
    }
    
    .emi-duration {
        font-size: 0.85rem;
        color: #E0E0E0;
        margin-top: 0.5rem;
    }
    
    /* Risk Badge - High Contrast */
    .risk-badge {
        display: inline-block;
        padding: 0.7rem 1.4rem;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
    }
    
    .risk-low {
        background: linear-gradient(135deg, #00FF88, #00DD88);
        color: #000000;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #FFA500, #FFB347);
        color: #FFFFFF;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #FF4444, #FF6666);
        color: #FFFFFF;
    }
    
    /* Stats Card - High Contrast */
    .stats-card {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.95), rgba(22, 33, 62, 0.95));
        padding: 2rem;
        border-radius: 14px;
        box-shadow: 0 8px 24px rgba(255, 107, 157, 0.2), inset 0 1px 0 rgba(255, 215, 0, 0.1);
        border: 2px solid rgba(255, 215, 0, 0.3);
        text-align: center;
        transition: all 0.3s ease;
        border-top: 4px solid #FFD700;
    }
    
    .stats-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 36px rgba(255, 107, 157, 0.35);
        border-color: rgba(255, 215, 0, 0.6);
        background: linear-gradient(135deg, rgba(26, 26, 46, 1), rgba(15, 52, 96, 1));
    }
    
    .stats-label {
        font-size: 0.85rem;
        color: #E0E0E0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
    
    .stats-value {
        font-size: 2rem;
        font-weight: 900;
        color: #FFD700;
        margin: 0.5rem 0;
        text-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
    }
    
    .stats-subtext {
        font-size: 0.8rem;
        color: #E0E0E0;
        margin-top: 0.5rem;
    }
    
    /* Buttons - High Contrast */
    .stButton > button {
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        border: 2px solid #FFD700 !important;
        box-shadow: 0 6px 20px rgba(255, 215, 0, 0.4) !important;
        background: linear-gradient(135deg, #FFD700, #FFA500) !important;
        color: #000000 !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 28px rgba(255, 215, 0, 0.6) !important;
        border-color: #FFFFFF !important;
    }
    
    /* Forms - High Contrast */
    .stNumberInput input, .stSelectbox select, .stSlider {
        border-radius: 10px;
        border: 2px solid rgba(255, 215, 0, 0.4) !important;
        background: rgba(26, 26, 46, 0.8) !important;
        color: #FFFFFF !important;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .stNumberInput input::placeholder {
        color: #A0A0A0;
    }
    
    .stNumberInput input:focus, .stSelectbox select:focus {
        border-color: #FFD700 !important;
        box-shadow: 0 0 0 3px rgba(255, 215, 0, 0.25) !important;
        background: rgba(26, 26, 46, 1) !important;
    }
    
    /* Sidebar - High Contrast Dark */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-right: 2px solid rgba(255, 215, 0, 0.2);
    }
    
    [data-testid="stSidebar"] > div {
        color: #FFFFFF;
    }
    
    .sidebar-title {
        color: #FFD700;
        font-size: 1.3rem;
        font-weight: 800;
        margin: 1rem 0 0.5rem 0;
        letter-spacing: -0.3px;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.5);
    }
    
    .sidebar-subtitle {
        color: #E0E0E0;
        font-size: 0.9rem;
        margin: 0;
        font-weight: 400;
    }
    
    /* Charts */
    .stPlotlyChart {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.8), rgba(22, 33, 62, 0.8));
        border-radius: 14px;
        padding: 1.5rem;
        border: 2px solid rgba(255, 215, 0, 0.3);
        box-shadow: 0 8px 24px rgba(255, 107, 157, 0.15);
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        border-radius: 10px;
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.9), rgba(22, 33, 62, 0.9));
        border: 2px solid rgba(255, 215, 0, 0.3);
        font-weight: 700;
        color: #FFD700;
        text-shadow: 0 1px 4px rgba(0, 0, 0, 0.5);
    }
    
    .streamlit-expanderHeader:hover {
        background: linear-gradient(135deg, rgba(26, 26, 46, 1), rgba(15, 52, 96, 1));
        border-color: rgba(255, 215, 0, 0.6);
    }
    
    /* Alerts */
    .stAlert {
        border-radius: 12px;
        border-left: 4px solid;
        padding: 1rem 1.5rem;
        background: rgba(26, 26, 46, 0.9) !important;
        color: #FFFFFF !important;
        font-weight: 500;
    }
    
    .stWarning {
        border-left-color: #FFA500 !important;
        background: linear-gradient(90deg, rgba(255, 165, 0, 0.2), rgba(26, 26, 46, 0.9)) !important;
    }
    
    .stInfo {
        border-left-color: #00D4FF !important;
        background: linear-gradient(90deg, rgba(0, 212, 255, 0.2), rgba(26, 26, 46, 0.9)) !important;
    }
    
    .stError {
        border-left-color: #FF4444 !important;
        background: linear-gradient(90deg, rgba(255, 68, 68, 0.2), rgba(26, 26, 46, 0.9)) !important;
    }
    
    .stSuccess {
        border-left-color: #00FF88 !important;
        background: linear-gradient(90deg, rgba(0, 255, 136, 0.2), rgba(26, 26, 46, 0.9)) !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .main-header {
            padding: 2.5rem 1rem;
        }
        
        .main-header h1 {
            font-size: 2.2rem;
        }
        
        .main-header .subtitle {
            font-size: 1rem;
        }
        
        .product-card {
            margin-bottom: 1rem;
        }
        
        .stats-card {
            padding: 1.2rem;
            margin-bottom: 1rem;
        }
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom Scrollbar - High Contrast */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(26, 26, 46, 0.6);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(255, 215, 0, 0.3);
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #FFFFFF, #FFD700);
        box-shadow: 0 0 15px rgba(255, 215, 0, 0.6);
    }
    
    /* Text & Labels - High Contrast */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.5);
    }
    
    label {
        color: #E0E0E0 !important;
        font-weight: 600 !important;
    }
    
    p, span, div {
        color: #E0E0E0;
    }
    
    /* Markdown text improvements */
    .stMarkdown {
        color: #E0E0E0;
    }

    </style>
""", unsafe_allow_html=True)


# ============================================
# INITIALIZE SESSION STATE
# ============================================

if 'engine' not in st.session_state:
    st.session_state.engine = RecommendationEngine()
    try:
        st.session_state.engine.load_products()
    except:
        st.warning("⚠️ Product data not found. Please run the data generation pipeline first.")

if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None

if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {}


# ============================================
# HELPER FUNCTIONS
# ============================================

def format_currency(amount):
    """Format amount as Indian currency"""
    return f"₹{amount:,.0f}"


def get_risk_badge_html(risk_level):
    """Generate HTML for risk badge"""
    emoji_map = {
        'Low': '✅',
        'Medium': '⚠️',
        'High': '❌'
    }
    class_map = {
        'Low': 'risk-low',
        'Medium': 'risk-medium',
        'High': 'risk-high'
    }
    
    emoji = emoji_map.get(risk_level, '❓')
    css_class = class_map.get(risk_level, '')
    
    return f'<span class="risk-badge {css_class}">{emoji} {risk_level}</span>'


def create_affordability_gauge(score):
    """Create affordability gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score * 100,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Affordability Score", 'font': {'size': 22, 'color': '#1F2937', 'family': 'Arial, sans-serif'}},
        delta={'reference': 70, 'increasing': {'color': "#10B981"}, 'decreasing': {'color': '#EF4444'}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 2, 'tickcolor': "#6B7280"},
            'bar': {'color': "#6366F1"},
            'bgcolor': "#F3F4F6",
            'borderwidth': 2,
            'bordercolor': "#E5E7EB",
            'steps': [
                {'range': [0, 40], 'color': '#FEE2E2'},
                {'range': [40, 70], 'color': '#FEF3C7'},
                {'range': [70, 100], 'color': '#DCFCE7'}
            ],
            'threshold': {
                'line': {'color': "#6366F1", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(
        height=350,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor='white',
        font={'family': 'Arial, sans-serif', 'color': '#1F2937'}
    )
    
    return fig


# ============================================
# MAIN APPLICATION
# ============================================

def main():
    # Enhanced Header
    st.markdown("""
    <div class="main-header">
        <div style="font-size: 4rem; margin-bottom: 0.8rem;">💳</div>
        <h1>FinSmart</h1>
        <p class="subtitle">AI-Powered Smart Product Discovery</p>
        <p class="tagline">✨ Find Affordable Products Tailored to Your Budget ✨</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar - User Input
    with st.sidebar:
        st.markdown("""
        <div style="padding: 1rem 0; margin-bottom: 2rem;">
            <h2 class="sidebar-title">📋 Your Profile</h2>
            <p class="sidebar-subtitle">Complete your financial details</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form(key="financial_profile_form"):
            # Income Details
            st.markdown("""
            <div style="padding: 1rem 0;">
                <h3 style="color: #6366F1; font-size: 1rem; margin: 0 0 1rem 0; font-weight: 700;">💰 Income Details</h3>
            </div>
            """, unsafe_allow_html=True)
            
            monthly_income = st.number_input(
                "Monthly Income (₹)",
                min_value=10000,
                max_value=1000000,
                value=50000,
                step=5000,
                help="Your monthly take-home income"
            )
            
            existing_emi = st.number_input(
                "Existing EMI Obligations (₹)",
                min_value=0,
                max_value=int(monthly_income * 0.7) if monthly_income > 0 else 1,
                value=0,
                step=1000,
                help="Total monthly EMI already being paid"
            )
            
            credit_score = st.slider(
                "Credit Score",
                min_value=300,
                max_value=850,
                value=700,
                step=10,
                help="Your CIBIL/Credit score (higher is better)"
            )
            
            st.markdown("---")
            
            # EMI Preferences
            st.markdown("""
            <div style="padding: 1rem 0;">
                <h3 style="color: #6366F1; font-size: 1rem; margin: 0 0 1rem 0; font-weight: 700;">🎯 EMI Preferences</h3>
            </div>
            """, unsafe_allow_html=True)
            
            max_emi = st.number_input(
                "Maximum Affordable EMI (₹/month)",
                min_value=1000,
                max_value=int(monthly_income) if monthly_income > 0 else 100000,
                value=min(10000, int(monthly_income * 0.3)) if monthly_income > 0 else 10000,
                step=500,
                help="Maximum EMI you can comfortably afford"
            )
            
            duration = st.selectbox(
                "Preferred EMI Duration (months)",
                options=EMI_DURATIONS,
                index=3,
                help="How long you want to spread the payment"
            )
            
            st.markdown("---")
            
            # Product Preferences
            st.markdown("""
            <div style="padding: 1rem 0;">
                <h3 style="color: #6366F1; font-size: 1rem; margin: 0 0 1rem 0; font-weight: 700;">🛍️ Preferences</h3>
            </div>
            """, unsafe_allow_html=True)
            
            preferred_category = st.selectbox(
                "Product Category",
                options=['Any'] + PRODUCT_CATEGORIES,
                index=0,
                help="Select a specific category or 'Any' to see all products"
            )
            
            top_n = st.slider(
                "Number of Recommendations",
                min_value=5,
                max_value=20,
                value=12,
                step=1,
                help="How many products you want to see"
            )
            
            filter_affordable = st.checkbox(
                "Show only affordable products",
                value=True,
                help="Filter to show only products within your budget"
            )
            
            st.markdown("---")
            
            # Search Button
            search_btn = st.form_submit_button(
                "🔍 Find My Affordable Products",
                use_container_width=True,
                help="Click to analyze and get personalized recommendations"
            )
    
    # Main Content Area
    if search_btn:
        # Create user profile
        user_profile = {
            'max_emi': max_emi,
            'duration': duration,
            'category': None if preferred_category == 'Any' else preferred_category,
            'credit_score': credit_score,
            'monthly_income': monthly_income,
            'existing_emi': existing_emi
        }
        
        st.session_state.user_profile = user_profile
        
        # Get recommendations
        with st.spinner("🤖 AI is analyzing thousands of products for you..."):
            try:
                recommendations = st.session_state.engine.get_recommendations(
                    user_profile,
                    top_n=top_n,
                    filter_affordable=filter_affordable
                )
                st.session_state.recommendations = recommendations
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.info("💡 Please run: `python run_pipeline.py` to generate data first.")
                return
    
    # Display Results
    if st.session_state.recommendations is not None and len(st.session_state.recommendations) > 0:
        recommendations = st.session_state.recommendations
        user_profile = st.session_state.user_profile
        
        # Success message
        st.success(f"✨ Found **{len(recommendations)}** perfect products for you!")
        
        # Affordability Overview
        st.markdown("### 📊 Your Affordability Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="stats-card">
                    <div class="stats-label">📊 Max Affordable EMI</div>
                    <div class="stats-value">{format_currency(user_profile['max_emi'])}</div>
                    <div class="stats-subtext">per month</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            avg_interest = np.mean(list(INTEREST_RATES.values()))
            max_price = EMICalculator.calculate_max_affordable_price(
                user_profile['max_emi'],
                user_profile['duration'],
                avg_interest
            )
            st.markdown(f"""
                <div class="stats-card" style="border-top-color: #10B981;">
                    <div class="stats-label">💰 Max Budget</div>
                    <div class="stats-value" style="color: #10B981;">{format_currency(max_price)}</div>
                    <div class="stats-subtext">at {avg_interest*100:.1f}% interest</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            available_income = user_profile['monthly_income'] - user_profile['existing_emi']
            st.markdown(f"""
                <div class="stats-card" style="border-top-color: #F59E0B;">
                    <div class="stats-label">💵 Available Income</div>
                    <div class="stats-value" style="color: #F59E0B;">{format_currency(available_income)}</div>
                    <div class="stats-subtext">after existing EMI</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            credit_category = "Excellent" if user_profile['credit_score'] >= 750 else \
                            "Good" if user_profile['credit_score'] >= 650 else \
                            "Fair" if user_profile['credit_score'] >= 550 else "Poor"
            color_map = {"Excellent": "#10B981", "Good": "#6366F1", "Fair": "#F59E0B", "Poor": "#EF4444"}
            st.markdown(f"""
                <div class="stats-card" style="border-top-color: {color_map[credit_category]};">
                    <div class="stats-label">⭐ Credit Rating</div>
                    <div class="stats-value" style="color: {color_map[credit_category]};">{user_profile['credit_score']}</div>
                    <div class="stats-subtext">{credit_category}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Affordability Gauge & Charts
        col_gauge1, col_gauge2 = st.columns([1, 1])
        
        with col_gauge1:
            st.markdown("#### 📈 Affordability Score")
            avg_score = recommendations['affordability_score'].mean()
            fig_gauge = create_affordability_gauge(avg_score)
            st.plotly_chart(fig_gauge, use_container_width=True, key='affordability_gauge')
        
        with col_gauge2:
            st.markdown("#### 💹 Budget Distribution")
            fig_dist = px.histogram(
                recommendations,
                x='final_price',
                nbins=15,
                labels={'final_price': 'Price (₹)', 'count': 'Products'},
                color_discrete_sequence=['#6366F1']
            )
            fig_dist.update_layout(
                showlegend=False,
                height=380,
                margin=dict(l=50, r=20, t=40, b=40),
                paper_bgcolor='white',
                plot_bgcolor='rgba(243, 244, 246, 0.5)',
                font={'color': '#1F2937', 'family': 'Arial, sans-serif'},
                xaxis_title="Price (₹)",
                yaxis_title="Number of Products"
            )
            st.plotly_chart(fig_dist, use_container_width=True, key='price_dist')
        
        st.markdown("---")
        
        # Product Recommendations Grid
        st.markdown("### 🎁 Recommended Products")
        
        # Sort options
        col_sort1, col_sort2, col_sort3 = st.columns([1, 1, 2])
        with col_sort1:
            sort_by = st.selectbox("Sort by", ["Affordability (High)", "Price (Low)", "Rating (High)", "Discount (High)"])
        
        if sort_by == "Affordability (High)":
            recommendations = recommendations.sort_values('affordability_score', ascending=False)
        elif sort_by == "Price (Low)":
            recommendations = recommendations.sort_values('final_price', ascending=True)
        elif sort_by == "Rating (High)":
            recommendations = recommendations.sort_values('rating', ascending=False)
        elif sort_by == "Discount (High)":
            recommendations = recommendations.sort_values('discount_percent', ascending=False)
        
        # Display products in grid
        products_per_row = 3
        for idx in range(0, len(recommendations), products_per_row):
            cols = st.columns(products_per_row)
            for col_idx, col in enumerate(cols):
                if idx + col_idx < len(recommendations):
                    product = recommendations.iloc[idx + col_idx]
                    
                    with col:
                        # Calculate risk level
                        risk_level = EMICalculator.classify_risk(product['affordability_score'])
                        risk_colors = {'Low': '#10B981', 'Medium': '#F59E0B', 'High': '#EF4444'}
                        risk_emojis = {'Low': '✅', 'Medium': '⚠️', 'High': '❌'}
                        
                        # Calculate stars
                        full_stars = int(product['rating'])
                        stars = '⭐' * full_stars
                        if (product['rating'] - full_stars) >= 0.5:
                            stars += '✨'
                        
                        st.markdown(f"""
                        <div class="product-card">
                            <div class="product-header">
                                <div>
                                    <div class="product-title">{product['product_name']}</div>
                                </div>
                                <span class="product-category">{product['category']}</span>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Product image
                        st.image(product['image_url'], use_container_width=True)
                        
                        st.markdown("""
                            <div class="product-content">
                        """, unsafe_allow_html=True)
                        
                        # Rating
                        st.markdown(f"""
                        <div class="rating-section">
                            <span class="rating-stars">{stars}</span>
                            <span class="rating-count">({int(product['num_reviews'])} reviews)</span>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Price
                        discount_html = ''
                        if product['discount_percent'] > 0:
                            discount_html = f'<span class="discount-badge">{int(product["discount_percent"])}% OFF</span>'
                        
                        st.markdown(f"""
                        <div class="price-section">
                            <span class="price-original">{format_currency(product['original_price'])}</span>
                            <span class="price-final">{format_currency(product['final_price'])}</span>
                            {discount_html}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # EMI Info
                        st.markdown(f"""
                        <div class="emi-info">
                            <div class="emi-label">Monthly EMI</div>
                            <div class="emi-amount">{format_currency(product['monthly_emi'])}</div>
                            <div class="emi-duration">for {user_profile['duration']} months</div>
                            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(99,102,241,0.2);">
                                <span class="risk-badge risk-{risk_level.lower()}">{risk_emojis[risk_level]} {risk_level}</span>
                                <div style="margin-top: 0.5rem; font-size: 0.8rem; color: #6B7280; font-weight: 600;">
                                    Score: {product['affordability_score']:.2f}/10
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Buy Button
                        st.link_button(
                            "🛒 Buy Now",
                            product['product_url'],
                            use_container_width=True
                        )
                        
                        st.markdown("</div>", unsafe_allow_html=True)
        
        # Summary Statistics
        st.markdown("---")
        st.markdown("### 📋 Summary Statistics")
        
        sum_col1, sum_col2, sum_col3, sum_col4 = st.columns(4)
        
        with sum_col1:
            avg_price = recommendations['final_price'].mean()
            st.metric("Average Price", format_currency(avg_price), delta=f"{len(recommendations)} products")
        
        with sum_col2:
            avg_emi = recommendations['monthly_emi'].mean()
            st.metric("Average EMI", format_currency(avg_emi), delta="per month")
        
        with sum_col3:
            avg_rating = recommendations['rating'].mean()
            st.metric("Average Rating", f"{avg_rating:.2f}⭐", delta="out of 5")
        
        with sum_col4:
            avg_discount = recommendations['discount_percent'].mean()
            st.metric("Average Discount", f"{avg_discount:.1f}%", delta="savings")
    
    else:
        # Welcome message
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #6B7280;">
            <h2 style="color: #1F2937; font-size: 1.8rem; margin-bottom: 1rem;">👋 Welcome to FinSmart!</h2>
            <p style="font-size: 1.1rem; line-height: 1.6;">
                Start by filling in your financial details in the sidebar to discover products that match your budget.
            </p>
            <p style="font-size: 0.95rem; color: #9CA3AF; margin-top: 2rem;">
                🔒 Your data is safe and used only for this session<br>
                💡 Our AI analyzes affordability based on your income and credit score
            </p>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
