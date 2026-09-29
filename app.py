import streamlit as st     #streamlit run app.py
import pandas as pd
import sqlite3
from anthropic import Anthropic
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Load environment
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key)

# Connect to database
conn = sqlite3.connect("retail.db")

# Page config
st.set_page_config(page_title="AI Business Assistant", layout="wide")

# Custom CSS for better styling
st.markdown("""
    <style>
    :root {
        --primary: #6366f1;
        --primary-dark: #4f46e5;
        --secondary: #8b5cf6;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --dark: #0f172a;
        --darker: #020617;
        --light: #f8fafc;
        --border: #e2e8f0;
    }
    
    * {
        margin: 0;
        padding: 0;
    }
    
    html, body, .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #f1f5f9;
    }
    
    /* Headers */
    h1 {
        font-size: 2.5em !important;
        font-weight: 800 !important;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        margin-bottom: 0.5em !important;
        letter-spacing: -0.02em;
    }
    
    h2 {
        font-size: 1.8em !important;
        font-weight: 700 !important;
        color: #f1f5f9 !important;
        margin-top: 1.5em !important;
        margin-bottom: 0.8em !important;
    }
    
    h3 {
        font-size: 1.3em !important;
        font-weight: 600 !important;
        color: #cbd5e1 !important;
    }
    
    h4 {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1a1f35 100%) !important;
    }
    
    .stSidebar {
        background: linear-gradient(180deg, #0f172a 0%, #1a1f35 100%) !important;
    }
    
    .stSidebar h2, .stSidebar h3 {
        color: #f1f5f9 !important;
    }
    
    .stSidebar [data-testid="stMarkdownContainer"] {
        color: #f1f5f9 !important;
    }
    
        /* NAVIGATION RADIO BUTTONS - BOLD PURPLE */
    .stSidebar .stRadio > label {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.1) 100%) !important;
        border: 2px solid rgba(99, 102, 241, 0.4) !important;
        color: #e0e7ff !important;
        font-weight: 700 !important;
        padding: 12px 16px !important;
        border-radius: 12px !important;
        margin: 8px 0 !important;
        cursor: pointer;
        transition: all 0.3s ease !important;
    }
    
    .stSidebar .stRadio > label:hover {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.25) 0%, rgba(139, 92, 246, 0.2) 100%) !important;
        border-color: rgba(139, 92, 246, 0.8) !important;
        color: #a5b4fc !important;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.2) !important;
    }
    
    /* Active selected radio button */
    .stSidebar .stRadio [data-testid="stCheckbox"] > label {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        border: 2px solid #6366f1 !important;
        color: #ffffff !important;
        box-shadow: 0 0 25px rgba(99, 102, 241, 0.4) !important;
    }
    
    .stSidebar .stRadio > div {
        background-color: transparent !important;
    }
    
    .stRadio > div {
        background-color: transparent !important;
    }
    
    /* Selectbox */
    .stSelectbox [data-baseweb="select"] > div {
        background-color: rgba(30, 41, 59, 0.9) !important;
        border: 1px solid rgba(99, 102, 241, 0.4) !important;
        border-radius: 10px !important;
        color: #f1f5f9 !important;
    }
    
    .stSidebar .stSelectbox [data-baseweb="select"] > div {
        background-color: rgba(30, 41, 59, 0.9) !important;
        border: 1px solid rgba(99, 102, 241, 0.4) !important;
    }
    
    /* Slider */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
    }
    
    /* Cards and containers */
    .metric-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 24px !important;
        border-radius: 16px !important;
        margin: 12px 0 !important;
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: rgba(99, 102, 241, 0.6);
        box-shadow: 0 12px 48px rgba(99, 102, 241, 0.15);
        transform: translateY(-2px);
    }
    
    .insight-box {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(99, 102, 241, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.4);
        padding: 20px !important;
        border-left: 4px solid #6366f1 !important;
        border-radius: 12px !important;
        margin: 16px 0 !important;
        backdrop-filter: blur(10px);
    }
    
    .anomaly-alert {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(99, 102, 241, 0.05) 100%);
        border: 1px solid rgba(245, 158, 11, 0.4);
        border-left: 4px solid #f59e0b !important;
        padding: 16px !important;
        border-radius: 12px !important;
        margin: 12px 0 !important;
        backdrop-filter: blur(10px);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
        border-bottom: 2px solid rgba(99, 102, 241, 0.2);
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8;
        padding: 0.5em 1em;
        font-weight: 600;
        border-radius: 8px 8px 0 0;
    }
    
    .stTabs [aria-selected="true"] [data-baseweb="tab"] {
        color: #6366f1 !important;
        border-bottom: 3px solid #6366f1;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Dataframe */
    .stDataFrame {
        background-color: rgba(15, 23, 42, 0.5) !important;
        border: 1px solid rgba(99, 102, 241, 0.2) !important;
        border-radius: 12px !important;
    }
    
    /* Text colors */
    p, span, div, label {
        color: #e2e8f0;
    }
    
    /* Info/Alert boxes */
    .stInfo {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(99, 102, 241, 0.05) 100%) !important;
        border: 1px solid rgba(99, 102, 241, 0.4) !important;
        border-radius: 12px !important;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%) !important;
        border: 1px solid rgba(245, 158, 11, 0.4) !important;
        border-radius: 12px !important;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.1) 0%, rgba(239, 68, 68, 0.05) 100%) !important;
        border: 1px solid rgba(239, 68, 68, 0.4) !important;
        border-radius: 12px !important;
    }
    
    /* Dividers */
    hr {
        border: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.3), transparent);
        margin: 2em 0;
    }
    
    /* Metrics */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    
    /* Toolbar & Settings */
    .stToolbar {
        background: transparent !important;
    }
    
    [data-testid="stToolbar"] {
        background: transparent !important;
    }
    
    .stToolbar button {
        background-color: rgba(99, 102, 241, 0.2) !important;
        border: 1px solid rgba(99, 102, 241, 0.4) !important;
        border-radius: 8px !important;
        color: #6366f1 !important;
    }
    
    .stToolbar button:hover {
        background-color: rgba(99, 102, 241, 0.3) !important;
        color: #8b5cf6 !important;
    }
    
    /* Settings popup */
    [data-baseweb="popover"] {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
        border: 1px solid rgba(99, 102, 241, 0.4) !important;
        border-radius: 12px !important;
    }
    
    [data-baseweb="popover"] > div {
        background: transparent !important;
    }
    
    /* Settings menu items */
    [role="menuitem"], [role="option"] {
        color: #f1f5f9 !important;
    }
    
    [role="menuitem"]:hover, [role="option"]:hover {
        background-color: rgba(99, 102, 241, 0.2) !important;
        color: #6366f1 !important;
    }
    
    /* Theme selector */
    [role="radio"] {
        color: #cbd5e1 !important;
    }
    
    [role="radio"]:hover {
        color: #6366f1 !important;
    }
    
    [role="radio"][aria-checked="true"] {
        color: #6366f1 !important;
    }
    
    /* Markdown */
    .markdown-text-container {
        color: #f1f5f9;
    }

        /* Remove black line and borders */
    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(99, 102, 241, 0.3) !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
    }
    
    /* Remove any black edges */
    .stApp > div {
        background: transparent !important;
    }
    
    .stApp > div > div {
        background: transparent !important;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
    }
    
    /* Remove all black borders */
    .stApp [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%) !important;
    }
    
    /* Purple edge only */
    [data-testid="stSidebar"]::after {
        content: '';
        position: absolute;
        right: 0;
        top: 0;
        height: 100%;
        width: 1px;
        background: linear-gradient(180deg, rgba(99, 102, 241, 0.5) 0%, rgba(139, 92, 246, 0.3) 100%);
    }

        /* Top toolbar - PURPLE */
    [data-testid="stToolbar"] {
        background: linear-gradient(90deg, #1e1b4b 0%, #312e81 100%) !important;
        border-bottom: 1px solid rgba(99, 102, 241, 0.3) !important;
    }
    
    .stToolbar {
        background: linear-gradient(90deg, #1e1b4b 0%, #312e81 100%) !important;
    }
    
    /* Deploy button */
    [data-testid="stToolbar"] button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
        border: 1px solid rgba(99, 102, 241, 0.5) !important;
        color: #ffffff !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    
    [data-testid="stToolbar"] button:hover {
        background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%) !important;
        box-shadow: 0 0 20px rgba(99, 102, 241, 0.3) !important;
    }
    
    /* Toolbar icons */
    [data-testid="stToolbar"] svg {
        color: #6366f1 !important;
    }
    
    [data-testid="stToolbar"] [role="button"] {
        color: #6366f1 !important;
    }
    
    [data-testid="stToolbar"] [role="button"]:hover {
        color: #8b5cf6 !important;
    }
    
    /* Settings menu - 3 dots */
    [data-testid="stToolbar"] [role="menuitem"] {
        color: #f1f5f9 !important;
    }
    
    [data-testid="stToolbar"] [role="menuitem"]:hover {
        background-color: rgba(99, 102, 241, 0.2) !important;
        color: #6366f1 !important;
    }

    
    </style>
""", unsafe_allow_html=True)

# Create a more modern header
col1, col2 = st.columns([0.8, 0.2], gap="large")
with col1:
    st.title("🤖 AI Business Assistant")
    st.markdown("### Intelligent Sales Analytics Powered by AI & Advanced Analytics")
with col2:
    st.markdown(f"""
    """, unsafe_allow_html=True)

st.markdown("---")

# Helper functions
def analyze_month(year_month):
    """Get category and region breakdown for a month"""
    query_cat = f"""
    SELECT Category, ROUND(SUM(Sales), 2) as Total_Sales
    FROM sales
    WHERE strftime('%Y-%m', "Order Date") = '{year_month}'
    GROUP BY Category
    ORDER BY Total_Sales DESC
    """
    cat_df = pd.read_sql(query_cat, conn)

    query_reg = f"""
    SELECT Region, ROUND(SUM(Sales), 2) as Total_Sales
    FROM sales
    WHERE strftime('%Y-%m', "Order Date") = '{year_month}'
    GROUP BY Region
    ORDER BY Total_Sales DESC
    """
    reg_df = pd.read_sql(query_reg, conn)

    return cat_df, reg_df

def get_monthly_trend():
    """Get all monthly data for anomaly detection"""
    query = """
    SELECT strftime('%Y-%m', "Order Date") as Month, ROUND(SUM(Sales), 2) as Total_Sales
    FROM sales
    GROUP BY Month
    ORDER BY Month
    """
    return pd.read_sql(query, conn)

def detect_anomalies(month_data, threshold=1.5):
    """Detect anomalies using standard deviation"""
    mean = month_data['Total_Sales'].mean()
    std = month_data['Total_Sales'].std()
    
    anomalies = []
    for idx, row in month_data.iterrows():
        z_score = abs((row['Total_Sales'] - mean) / std)
        if z_score > threshold:
            pct_diff = ((row['Total_Sales'] - mean) / mean) * 100
            anomalies.append({
                'month': row['Month'],
                'sales': row['Total_Sales'],
                'deviation': pct_diff,
                'z_score': z_score
            })
    
    return anomalies

def generate_explanation(month):
    """Generate AI explanation using Claude"""
    cat_df, reg_df = analyze_month(month)
    
    if cat_df.empty or reg_df.empty:
        return "No data available for this month."
    
    category_text = "\n".join([f"  - {row['Category']}: ${row['Total_Sales']:,.2f}" 
                               for _, row in cat_df.iterrows()])
    region_text = "\n".join([f"  - {row['Region']}: ${row['Total_Sales']:,.2f}" 
                             for _, row in reg_df.iterrows()])
    
    prompt = f"""
You are a business analyst. Here is sales data for {month}:

By Category:
{category_text}

By Region:
{region_text}

Provide a concise, plain-English analysis of this month's performance. 
Identify the key drivers and patterns. Keep it to 2-3 sentences.
"""
    
    try:
        message = client.messages.create(
            model="claude-opus-5",
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}]
        )
        
        for block in message.content:
            if hasattr(block, 'text'):
                return block.text
    except Exception as e:
        return f"Error generating explanation: {str(e)}"
    
    return "No response"

def compare_months(month1, month2):
    """Compare two months and show differences"""
    cat1, reg1 = analyze_month(month1)
    cat2, reg2 = analyze_month(month2)
    
    sales1 = cat1['Total_Sales'].sum()
    sales2 = cat2['Total_Sales'].sum()
    pct_change = ((sales2 - sales1) / sales1) * 100
    
    comparison = {
        'month1': month1,
        'month2': month2,
        'sales1': sales1,
        'sales2': sales2,
        'change': sales2 - sales1,
        'pct_change': pct_change
    }
    
    return comparison, cat1, cat2, reg1, reg2

# Sidebar navigation
st.sidebar.header("📊 Navigation")
page = st.sidebar.radio(
    "Navigation",
    ["Single Month Analysis", "Anomaly Detection", "Compare Months", 
     "KPI Dashboard","Sales Forecast", "Ask Claude", "PDF Report Export"]
)

# PAGE 1: Single Month Analysis
if page == "Single Month Analysis":
    st.sidebar.header("Select Month")
    
    # Get available months
    monthly_df = get_monthly_trend()
    available_months = monthly_df['Month'].tolist()
    
    selected_month = st.sidebar.selectbox(
        "Choose a month to analyze:",
        options=available_months,
        index=0
    )
    
    if selected_month:
        st.header(f"📈 Analysis for {selected_month}")
        
        with st.spinner("Analyzing data..."):
            cat_df, reg_df = analyze_month(selected_month)
            explanation = generate_explanation(selected_month)
        
        # AI Insight
        st.subheader("🤖 AI Insight")
        st.markdown(f"""
        <div class="insight-box">
        {explanation}
        </div>
        """, unsafe_allow_html=True)
        
        # Key Metrics
        st.markdown("### 📊 Key Metrics")
        col1, col2, col3, col4 = st.columns(4, gap="large")
        
        total_sales = cat_df['Total_Sales'].sum()
        top_category = cat_df.iloc[0]['Category'] if not cat_df.empty else "N/A"
        top_region = reg_df.iloc[0]['Region'] if not reg_df.empty else "N/A"
        
        with col1:
            st.metric("Total Sales", f"${total_sales:,.0f}")
        with col2:
            st.metric("Top Category", top_category)
        with col3:
            st.metric("Top Region", top_region)
        with col4:
            st.metric("# Categories", len(cat_df))
        
        # Charts
        st.subheader("📊 Breakdown")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Revenue by Category**")
            fig, ax = plt.subplots(figsize=(8, 4))
            colors = plt.cm.Blues(np.linspace(0.4, 0.8, len(cat_df)))
            ax.barh(cat_df['Category'], cat_df['Total_Sales'], color=colors)
            ax.set_xlabel('Sales ($)')
            ax.set_title(f"{selected_month}")
            plt.tight_layout()
            st.pyplot(fig)
        
        with col2:
            st.write("**Revenue by Region**")
            fig, ax = plt.subplots(figsize=(8, 4))
            colors = plt.cm.Oranges(np.linspace(0.4, 0.8, len(reg_df)))
            ax.barh(reg_df['Region'], reg_df['Total_Sales'], color=colors)
            ax.set_xlabel('Sales ($)')
            ax.set_title(f"{selected_month}")
            plt.tight_layout()
            st.pyplot(fig)

# PAGE 2: Anomaly Detection
elif page == "Anomaly Detection":
    st.header("🚨 Anomaly Detection")
    st.markdown("Automatically identify unusual months based on statistical analysis.")
    
    # Get monthly trend
    monthly_df = get_monthly_trend()
    
    # Detect anomalies
    anomalies = detect_anomalies(monthly_df, threshold=1.5)
    
    if anomalies:
        st.markdown(f"### Found {len(anomalies)} Anomal(ies)")
        
        for anom in anomalies:
            direction = "⬆️ **Higher**" if anom['deviation'] > 0 else "⬇️ **Lower**"
            st.markdown(f"""
            <div class="anomaly-alert">
            <strong>{anom['month']}</strong><br>
            Sales: ${anom['sales']:,.0f} ({direction} by {abs(anom['deviation']):.1f}%)<br>
            Anomaly Score: {anom['z_score']:.2f}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("✅ No significant anomalies detected in the data.")
    
    # Visualize trend
    st.subheader("📊 Monthly Trend with Anomalies")
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Plot all months
    ax.plot(monthly_df['Month'], monthly_df['Total_Sales'], marker='o', linestyle='-', linewidth=2, label='Sales')
    
    # Highlight anomalies
    if anomalies:
        anom_months = [a['month'] for a in anomalies]
        anom_sales = [monthly_df[monthly_df['Month'] == m]['Total_Sales'].values[0] for m in anom_months]
        ax.scatter(anom_months, anom_sales, color='red', s=200, zorder=5, label='Anomalies')
    
    # Add mean line
    mean_sales = monthly_df['Total_Sales'].mean()
    ax.axhline(y=mean_sales, color='gray', linestyle='--', alpha=0.7, label='Average')
    
    ax.set_xlabel('Month')
    ax.set_ylabel('Sales ($)')
    ax.set_title('Monthly Sales Trend with Anomalies')
    ax.legend()
    ax.tick_params(axis='x', rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# PAGE 3: Compare Months
elif page == "Compare Months":
    st.header("📊 Compare Two Months")
    
    monthly_df = get_monthly_trend()
    available_months = monthly_df['Month'].tolist()
    
    col1, col2 = st.columns(2)
    
    with col1:
        month1 = st.selectbox("First Month:", options=available_months, index=0)
    with col2:
        month2 = st.selectbox("Second Month:", options=available_months, index=min(1, len(available_months)-1))
    
    if month1 and month2:
        comparison, cat1, cat2, reg1, reg2 = compare_months(month1, month2)
        
        # Summary
        st.subheader("📈 Comparison Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(f"Sales ({month1})", f"${comparison['sales1']:,.0f}")
        with col2:
            st.metric(f"Sales ({month2})", f"${comparison['sales2']:,.0f}")
        with col3:
            color = "green" if comparison['pct_change'] > 0 else "red"
            st.metric("Change", f"{comparison['pct_change']:+.1f}%")
        
        # Category comparison
        st.subheader("🏷️ Category Changes")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**{month1}**")
            st.dataframe(cat1, use_container_width=True)
        
        with col2:
            st.write(f"**{month2}**")
            st.dataframe(cat2, use_container_width=True)
        
        # Region comparison
        st.subheader("🗺️ Region Changes")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**{month1}**")
            st.dataframe(reg1, use_container_width=True)
        
        with col2:
            st.write(f"**{month2}**")
            st.dataframe(reg2, use_container_width=True)



#  KPI Dashboard
elif page == "KPI Dashboard":
    st.header("📊 KPI Dashboard")
    st.markdown("Executive summary of key performance indicators")
    
    from forecasting import get_monthly_data
    
    # Get data
    monthly_df = get_monthly_data()
    
    # Calculate KPIs
    total_revenue = monthly_df['Sales'].sum()
    avg_monthly = monthly_df['Sales'].mean()
    best_month = monthly_df.loc[monthly_df['Sales'].idxmax()]
    worst_month = monthly_df.loc[monthly_df['Sales'].idxmin()]
    
    # Calculate growth
    first_6_months = monthly_df['Sales'].head(6).mean()
    last_6_months = monthly_df['Sales'].tail(6).mean()
    growth_rate = ((last_6_months - first_6_months) / first_6_months) * 100
    
    # Get category data
    conn = sqlite3.connect('retail.db')
    category_sales = pd.read_sql_query(
        "SELECT Category, SUM(Sales) as Total FROM sales GROUP BY Category ORDER BY Total DESC",
        conn
    )
    region_sales = pd.read_sql_query(
        "SELECT Region, SUM(Sales) as Total FROM sales GROUP BY Region ORDER BY Total DESC",
        conn
    )
    conn.close()
    
    top_category = category_sales.iloc[0] if len(category_sales) > 0 else None
    top_region = region_sales.iloc[0] if len(region_sales) > 0 else None
    
    # Display KPIs in 4 columns
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); 
                    padding: 20px; border-radius: 10px; text-align: center;">
            <h3 style="color: white; margin: 0;">Total Revenue</h3>
            <h2 style="color: white; margin: 10px 0 0 0;">${:,.0f}</h2>
        </div>
        """.format(total_revenue), unsafe_allow_html=True)
    
    with col2:
        color = "#10b981" if growth_rate > 0 else "#ef4444"
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {color} 0%, #059669 100%); 
                    padding: 20px; border-radius: 10px; text-align: center;">
            <h3 style="color: white; margin: 0;">Growth Rate</h3>
            <h2 style="color: white; margin: 10px 0 0 0;">{growth_rate:+.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); 
                    padding: 20px; border-radius: 10px; text-align: center;">
            <h3 style="color: white; margin: 0;">Avg Monthly</h3>
            <h2 style="color: white; margin: 10px 0 0 0;">${:,.0f}</h2>
        </div>
        """.format(avg_monthly), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ec4899 0%, #be185d 100%); 
                    padding: 20px; border-radius: 10px; text-align: center;">
            <h3 style="color: white; margin: 0;">Data Points</h3>
            <h2 style="color: white; margin: 10px 0 0 0;">{}</h2>
        </div>
        """.format(len(monthly_df)), unsafe_allow_html=True)
    
    st.divider()
    
    # Best and Worst Month
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                    padding: 20px; border-radius: 10px;">
            <h3 style="color: white; margin: 0;">🏆 Best Month</h3>
            <h2 style="color: white; margin: 10px 0 0 0;">{best_month['Month']}</h2>
            <h3 style="color: white; margin: 10px 0 0 0;">${best_month['Sales']:,.0f}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
                    padding: 20px; border-radius: 10px;">
            <h3 style="color: white; margin: 0;">📉 Worst Month</h3>
            <h2 style="color: white; margin: 10px 0 0 0;">{worst_month['Month']}</h2>
            <h3 style="color: white; margin: 10px 0 0 0;">${worst_month['Sales']:,.0f}</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    # Top Category and Region
    col1, col2 = st.columns(2)
    
    with col1:
        if top_category is not None:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); 
                        padding: 20px; border-radius: 10px;">
                <h3 style="color: white; margin: 0;">🎯 Top Category</h3>
                <h2 style="color: white; margin: 10px 0 0 0;">{top_category['Category']}</h2>
                <h3 style="color: white; margin: 10px 0 0 0;">${top_category['Total']:,.0f}</h3>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        if top_region is not None:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); 
                        padding: 20px; border-radius: 10px;">
                <h3 style="color: white; margin: 0;">🌍 Top Region</h3>
                <h2 style="color: white; margin: 10px 0 0 0;">{top_region['Region']}</h2>
                <h3 style="color: white; margin: 10px 0 0 0;">${top_region['Total']:,.0f}</h3>
            </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Category Breakdown Table
    st.subheader("📊 Category Performance")
    st.dataframe(
        category_sales.rename(columns={'Category': 'Category', 'Total': 'Revenue'})
        .style.format({'Revenue': '${:,.0f}'})
        .background_gradient(subset=['Revenue'], cmap='Purples'),
        use_container_width=True
    )
    
    # Region Breakdown Table
    st.subheader("🌏 Regional Performance")
    st.dataframe(
        region_sales.rename(columns={'Region': 'Region', 'Total': 'Revenue'})
        .style.format({'Revenue': '${:,.0f}'})
        .background_gradient(subset=['Revenue'], cmap='Blues'),
        use_container_width=True
    )



# PAGE 4: Sales Forecast
elif page == "Sales Forecast":
    st.header("🔮 Sales Forecast")
    st.markdown("Predict future sales using time series analysis")
    
    # Import forecasting functions
    from forecasting import forecast_sales, calculate_forecast_accuracy, get_trend_analysis
    
    # Forecast parameters
    col1, col2 = st.columns([3, 1])
    with col1:
        forecast_months = st.slider("Forecast horizon (months):", min_value=1, max_value=6, value=3)
    
    with st.spinner("Training forecast model..."):
        try:
            forecast_df, model, historical_df, X, y = forecast_sales(periods=forecast_months)
            
            # Display forecast table
            st.subheader("📊 Sales Forecast Table")
            st.dataframe(forecast_df, use_container_width=True)
            
            # Visualize
            st.subheader("📈 Forecast Visualization")
            
            fig, ax = plt.subplots(figsize=(12, 6))
            
            # Historical data
            historical_monthly = historical_df.copy()
            historical_monthly['Month'] = pd.to_datetime(historical_monthly['Month'])
            ax.plot(historical_monthly['Month'], historical_monthly['Sales'], 
                   marker='o', label='Historical Sales', linewidth=2, color='blue')
            
            # Forecast data
            forecast_dates = pd.to_datetime(forecast_df['Month'])
            ax.plot(forecast_dates, forecast_df['Forecast'], 
                   marker='s', label='Forecast', linewidth=2, color='orange', linestyle='--')
            
            # Confidence interval
            ax.fill_between(forecast_dates, 
                            forecast_df['Lower_Bound'], 
                            forecast_df['Upper_Bound'],
                            alpha=0.2, color='orange', label='95% Confidence Interval')
            
            ax.set_xlabel('Month')
            ax.set_ylabel('Sales ($)')
            ax.set_title('Historical vs Forecasted Sales')
            ax.legend()
            ax.tick_params(axis='x', rotation=45)
            plt.tight_layout()
            st.pyplot(fig)
            
            # Model accuracy metrics
            st.subheader("📊 Model Accuracy")
            
            accuracy_metrics = calculate_forecast_accuracy(model, X, y)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Forecast Accuracy", f"{accuracy_metrics['accuracy']:.1f}%")
            with col2:
                st.metric("MAPE", f"{accuracy_metrics['mape']:.2f}%")
            with col3:
                st.metric("RMSE", f"${accuracy_metrics['rmse']:,.0f}")
            
            st.info(f"✅ Model: {accuracy_metrics['method']} | Test Periods: {accuracy_metrics['test_periods']}")
            
            # Trend analysis
            st.subheader("📈 Trend Analysis")
            
            trend = get_trend_analysis(model, X, y)
            st.markdown(f"""
            <div class="insight-box">
            <strong>Direction:</strong> {trend['direction']}<br>
            <strong>Trend Strength:</strong> {trend['strength']:.2f}% per month<br>
            Based on historical linear progression.
            </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Error in forecasting: {str(e)}")




elif page == "Ask Claude":
    st.header("💬 Ask Claude About Your Data")
    st.markdown("Ask any question about your sales data and get AI-powered insights.")
    
    from forecasting import get_monthly_data
    
    # Initialize session state
    if 'show_answer' not in st.session_state:
        st.session_state.show_answer = False
    if 'last_response' not in st.session_state:
        st.session_state.last_response = ""
    
    # Get all data for context
    monthly_df = get_monthly_data()
    total_revenue = monthly_df['Sales'].sum()
    avg_monthly = monthly_df['Sales'].mean()
    best_month = monthly_df.loc[monthly_df['Sales'].idxmax()]
    worst_month = monthly_df.loc[monthly_df['Sales'].idxmin()]
    
    data_context = f"""
Sales Data Summary:
- Total Revenue: ${total_revenue:,.0f}
- Average Monthly Sales: ${avg_monthly:,.0f}
- Best Month: {best_month['Month']} (${best_month['Sales']:,.0f})
- Worst Month: {worst_month['Month']} (${worst_month['Sales']:,.0f})
- Data Range: {monthly_df['Month'].min()} to {monthly_df['Month'].max()}

Monthly breakdown:
{monthly_df.to_string(index=False)}
"""
    
    # USER INPUT SECTION
    st.subheader("📝 Ask Your Question")
    user_question = st.text_area(
        "What would you like to know about your sales data?",
        placeholder="e.g., 'Which month had the highest sales?'",
        height=100
    )
    
    # QUICK EXAMPLES
    st.markdown("**Quick examples:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔝 Best Month", use_container_width=True):
            user_question = "Which month had the highest sales?"
            with st.spinner("Claude is analyzing..."):
                try:
                    prompt = f"""You are a business analyst expert. A user is asking about their sales data.

Here is their sales data:
{data_context}

User Question: {user_question}

Provide a detailed, actionable answer based on the data. Be specific with numbers and insights."""
                    
                    message = client.messages.create(
                        model="claude-sonnet-5",
                        max_tokens=500,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    response_text = ""
                    if message.content:
                        last_block = message.content[-1]
                        if hasattr(last_block, 'text'):
                            response_text = last_block.text
                    
                    st.session_state.show_answer = True
                    st.session_state.last_response = response_text
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with col2:
        if st.button("📉 Worst Month", use_container_width=True):
            user_question = "Which month had the lowest sales?"
            with st.spinner("Claude is analyzing..."):
                try:
                    prompt = f"""You are a business analyst expert. A user is asking about their sales data.

Here is their sales data:
{data_context}

User Question: {user_question}

Provide a detailed, actionable answer based on the data. Be specific with numbers and insights."""
                    
                    message = client.messages.create(
                        model="claude-sonnet-5",
                        max_tokens=500,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    response_text = ""
                    if message.content:
                        last_block = message.content[-1]
                        if hasattr(last_block, 'text'):
                            response_text = last_block.text
                    
                    st.session_state.show_answer = True
                    st.session_state.last_response = response_text
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    with col3:
        if st.button("📊 Overall Summary", use_container_width=True):
            user_question = "Give me a summary of overall sales performance"
            with st.spinner("Claude is analyzing..."):
                try:
                    prompt = f"""You are a business analyst expert. A user is asking about their sales data.

Here is their sales data:
{data_context}

User Question: {user_question}

Provide a detailed, actionable answer based on the data. Be specific with numbers and insights."""
                    
                    message = client.messages.create(
                        model="claude-sonnet-5",
                        max_tokens=500,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    response_text = ""
                    if message.content:
                        last_block = message.content[-1]
                        if hasattr(last_block, 'text'):
                            response_text = last_block.text
                    
                    st.session_state.show_answer = True
                    st.session_state.last_response = response_text
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # GET ANSWER BUTTON - FULL WIDTH
    st.markdown("")
    if st.button("🔍 Get Answer", use_container_width=True, key="main_button"):
        if user_question.strip():
            with st.spinner("Claude is analyzing your question..."):
                try:
                    question_lower = user_question.lower().strip()
                    is_greeting = len(question_lower) < 10 and any(word == question_lower for word in ['hi', 'hello', 'hey', 'howdy', 'thanks', 'thank you'])
                    business_keywords = ['sales', 'revenue', 'month', 'category', 'region', 'growth', 'trend', 'highest', 'lowest', 'decrease', 'increase', 'forecast', 'anomal', 'performance', 'customer', 'product', 'profit', 'sell', 'buy', 'market', 'business']
                    is_business_question = any(keyword in question_lower for keyword in business_keywords)
                    
                    if is_greeting:
                        prompt = f"""User said: {user_question}
Just respond with a friendly greeting back. Keep it short (1-2 sentences)."""
                    elif is_business_question:
                        prompt = f"""You are a business analyst expert. A user is asking about their sales data.

Here is their sales data:
{data_context}

User Question: {user_question}

Provide a detailed, actionable answer based on the data. Be specific with numbers and insights."""
                    else:
                        prompt = f"""User asked: {user_question}

Politely explain that you only answer questions about sales data and business analytics."""
                    
                    message = client.messages.create(
                        model="claude-sonnet-5",
                        max_tokens=500,
                        messages=[{"role": "user", "content": prompt}]
                    )
                    
                    response_text = ""
                    if message.content:
                        last_block = message.content[-1]
                        if hasattr(last_block, 'text'):
                            response_text = last_block.text
                    
                    st.session_state.show_answer = True
                    st.session_state.last_response = response_text
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        else:
            st.warning("Please enter a question!")
    
    st.caption("📌 Click examples above or type your own question")
    
    # ANSWER SECTION - FULL WIDTH
    st.divider()
    st.subheader("🤖 Claude's Answer")
    
    if st.session_state.show_answer and st.session_state.last_response:
        st.markdown(f"""
        <div class="insight-box">
        {st.session_state.last_response}
        </div>
        """, unsafe_allow_html=True)
    elif st.session_state.show_answer:
        st.info("Getting response...")


# PAGE 7: PDF Report Export
elif page == "PDF Report Export":
    st.header("📄 Generate PDF Report")
    st.markdown("Create a professional PDF report with all your sales analysis and AI insights.")
    
    from forecasting import get_monthly_data
    from pdf_report import generate_pdf_report
    from anthropic import Anthropic
    
    # Get data
    monthly_df = get_monthly_data()
    
    # Create columns for layout
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📋 Report Preview")
        st.markdown("""
        Your PDF report will include:
        - ✅ Executive Summary (key metrics)
        - ✅ Monthly Sales Trend Chart
        - ✅ Revenue by Category Chart
        - ✅ Revenue by Region Chart
        - ✅ AI-Powered Business Insights
        - ✅ Professional Formatting
        """)
    
    with col2:
        st.subheader("⚙️ Settings")
        include_summary = st.checkbox("Include Summary Stats", value=True)
        include_insights = st.checkbox("Include AI Insights", value=True)
    
    st.divider()
    
    # Generate PDF Button
    if st.button("🎯 Generate PDF Report", use_container_width=True):
        with st.spinner("Generating PDF report..."):
            try:
                # Get AI summary for the report
                total_revenue = monthly_df['Sales'].sum()
                avg_monthly = monthly_df['Sales'].mean()
                
                data_context = f"""
Sales Data:
- Total Revenue: ${total_revenue:,.0f}
- Average Monthly Sales: ${avg_monthly:,.0f}
- Monthly breakdown: {monthly_df.to_string(index=False)}
"""
                
                prompt = f"""You are a business analyst. Provide a brief 2-3 paragraph executive summary of sales performance based on this data:

{data_context}

Be specific with numbers and actionable insights."""
                
                # Get AI insights
                client = Anthropic(api_key=api_key)
                message = client.messages.create(
                    model="claude-sonnet-5",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                ai_summary = ""
                if message.content:
                    last_block = message.content[-1]
                    if hasattr(last_block, 'text'):
                        ai_summary = last_block.text
                
                # Generate PDF
                import tempfile
                pdf_filename = os.path.join(tempfile.gettempdir(), "sales_report.pdf")
                generate_pdf_report(monthly_df, ai_summary, pdf_filename)
                
                # Read PDF for download
                with open(pdf_filename, "rb") as pdf_file:
                    pdf_bytes = pdf_file.read()
                
                # Success message
                st.success("✅ PDF Report Generated Successfully!")
                
                # Download button
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_bytes,
                    file_name="Sales_Analysis_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
                
                st.info("💡 Your report is ready to download and share!")
                
            except Exception as e:
                st.error(f"Error generating report: {str(e)}")
    
    st.divider()
    
    # Info section
    st.subheader("📌 What's Included?")
    
    with st.expander("📊 Charts & Visualizations"):
        st.markdown("""
        - **Sales Trend**: Monthly sales performance over time
        - **Category Analysis**: Revenue breakdown by product category
        - **Regional Analysis**: Revenue distribution across regions
        """)
    
    with st.expander("📈 Key Metrics"):
        st.markdown(f"""
        - Total Revenue: ${monthly_df['Sales'].sum():,.0f}
        - Average Monthly Sales: ${monthly_df['Sales'].mean():,.0f}
        - Data Points: {len(monthly_df)} months
        - Time Range: {monthly_df['Month'].min()} to {monthly_df['Month'].max()}
        """)
    
    with st.expander("🤖 AI Insights"):
        st.markdown("""
        Claude analyzes your sales data and provides:
        - Performance summary
        - Trend analysis
        - Key business insights
        - Actionable recommendations
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding-top: 10px;">
    <p style="font-size: 15px; color: #e2e8f0; margin-bottom: 4px;">
        © 2026 Kirtan Gandhi. All rights reserved.
    </p>
   
</div>
""", unsafe_allow_html=True)