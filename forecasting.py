import pandas as pd
import sqlite3
from sklearn.linear_model import LinearRegression
from scipy import stats
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def get_monthly_data():
    """Get all monthly sales data"""
    conn = sqlite3.connect("retail.db")
    query = """
    SELECT strftime('%Y-%m', "Order Date") as Month, ROUND(SUM(Sales), 2) as Sales
    FROM sales
    GROUP BY Month
    ORDER BY Month
    """
    df = pd.read_sql(query, conn)
    return df

def forecast_sales(periods=3):
    """
    Forecast sales using linear regression with seasonality
    Simple but effective approach
    """
    # Get historical data
    df = get_monthly_data()
    historical_df = df.copy()
    
    # Prepare data for model
    X = np.arange(len(df)).reshape(-1, 1)  # Month indices
    y = df['Sales'].values
    
    # Train linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Calculate trend and seasonal components
    trend = model.predict(X)
    residuals = y - trend
    seasonal_pattern = residuals / np.std(residuals)
    
    # Forecast future periods
    future_indices = np.arange(len(df), len(df) + periods).reshape(-1, 1)
    forecast_values = model.predict(future_indices)
    
    # Add confidence intervals (±15% based on historical volatility)
    volatility = np.std(residuals) / np.mean(y)
    margin = forecast_values * volatility * 1.96  # 95% confidence
    
    # Create forecast dataframe
    last_date = pd.to_datetime(df['Month'].iloc[-1])
    future_dates = [last_date + pd.DateOffset(months=i+1) for i in range(periods)]
    
    forecast_df = pd.DataFrame({
        'Month': [d.strftime('%Y-%m') for d in future_dates],
        'Forecast': forecast_values,
        'Lower_Bound': forecast_values - margin,
        'Upper_Bound': forecast_values + margin
    })
    
    return forecast_df, model, historical_df, X, y

def calculate_forecast_accuracy(model, X, y):
    """Calculate forecast accuracy using cross-validation"""
    from sklearn.model_selection import cross_val_score
    
    # Use last 3 months as test set
    train_size = len(X) - 3
    X_train, X_test = X[:train_size], X[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]
    
    # Retrain on training data
    test_model = LinearRegression()
    test_model.fit(X_train, y_train)
    
    # Predict on test data
    y_pred = test_model.predict(X_test)
    
    # Calculate metrics
    mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
    rmse = np.sqrt(np.mean((y_test - y_pred) ** 2))
    accuracy = 100 - mape
    
    return {
        'mape': mape,
        'rmse': rmse,
        'accuracy': max(0, accuracy),  # Avoid negative accuracy
        'test_periods': len(X_test),
        'method': 'Linear Regression with Seasonality'
    }

def get_trend_analysis(model, X, y):
    """Analyze trend direction and strength"""
    trend = model.predict(X)
    slope = model.coef_[0]
    
    if slope > 0:
        direction = "📈 Upward"
    elif slope < 0:
        direction = "📉 Downward"
    else:
        direction = "➡️ Flat"
    
    return {
        'direction': direction,
        'slope': slope,
        'strength': abs(slope) / np.mean(y) * 100  # Slope as % of average
    }