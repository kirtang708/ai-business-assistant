# AI Business Assistant

An intelligent sales analytics platform that combines SQL-based data analysis with Claude AI to provide automated business insights.

## Features

- **Single Month Analysis**: View sales breakdowns by category and region with AI-generated insights
- **Anomaly Detection**: Automatically identify unusual sales patterns using statistical analysis
- **Comparative Analysis**: Compare two months side-by-side to understand trends and changes

## Why It's Different

- **Real Data Analysis**: Uses actual SQL queries (not just dummy data)
- **AI Explanations**: Claude explains pre-computed numbers (avoids hallucination)
- **Statistical Rigor**: Anomaly detection uses z-score method, not arbitrary thresholds
- **Production-Grade**: Error handling, proper architecture, clean code

## Architecture


## Tech Stack

- **Frontend**: Streamlit (Python web framework)
- **Database**: SQLite with Pandas SQL queries
- **AI**: Claude API (Anthropic)
- **Data Processing**: Pandas, NumPy
- **Visualization**: Matplotlib

## Installation

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Install dependencies:
```bash
pip install streamlit pandas sqlite3 anthropic python-dotenv matplotlib numpy
```

3. Create `.env` file with your API key:



4. Run the app:
```bash
streamlit run app.py
```

## Dataset

- **Source**: Superstore Sales Dataset (Kaggle)
- **Size**: 9,800 transactions across 3 categories, 4 regions
- **Date Range**: 2016-2017
- **Database**: `retail.db` (SQLite)

## Key Findings

- Technology is the highest revenue category ($827K+)
- West region leads in sales ($710K+)
- Seasonal patterns detected with anomalies in off-peak months
- AI explanations identify key drivers without hallucination

## Features Implemented

### 1. Single Month Analysis
- Breakdown by category and region
- AI-generated business insight
- Visual charts (matplotlib)
- Key metrics display

### 2. Anomaly Detection
- Detects unusual months using standard deviation
- Visual trend chart highlighting anomalies
- Severity scoring (z-score)

### 3. Comparative Analysis
- Side-by-side month comparison
- Percentage change calculation
- Category and region breakdowns

## Files

- `app.py` - Main Streamlit application
- `analysis.ipynb` - Jupyter notebook with analysis code
- `retail.db` - SQLite database with sales data
- `.env` - Environment variables (API key)
- `train.csv` - Original dataset
- `README.md` - This file

## Results

- Successfully identifies revenue drivers
- Detects seasonal patterns
- Generates human-readable insights
- Zero hallucinations (AI only explains real data)

## Time Investment

- Data preparation: 1 hour
- Backend analysis: 1 hour
- API integration: 1 hour
- UI/Streamlit app: 2 hours
- **Total: ~5 hours**

## What I Learned

1. How to build end-to-end data pipeline
2. LLM integration best practices (grounding in real data)
3. Anomaly detection techniques
4. Streamlit for rapid UI development
5. Balancing technical depth with usability

## Next Steps (If Extended)

- Add forecasting (predict next month sales)
- User authentication and multi-user support
- Export reports to PDF
- Real-time data ingestion
- More sophisticated anomaly detection (Isolation Forest)

### 4. Sales Forecasting
- Time series prediction using linear regression
- Confidence intervals for forecast uncertainty
- Model accuracy metrics (MAPE, RMSE)

### 5. Advanced Anomaly Detection
- Compares 3 statistical methods (Z-Score, IQR, Isolation Forest)
- Consensus-based anomaly identification
- Method explanation and recommendation

---

**Author**: Kirtan Gandhi 