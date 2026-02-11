"""
Flask backend for Brent Oil Change Point Dashboard
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from pathlib import Path
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Load data
DATA_DIR = Path(__file__).parent.parent.parent / 'data'

# Load processed data
df = pd.read_csv(DATA_DIR / 'processed' / 'features_engineered.csv', parse_dates=['Date'])
change_points = pd.read_csv(DATA_DIR / 'processed' / 'change_point_results.csv', parse_dates=['date'])
events = pd.read_csv(DATA_DIR / 'external' / 'geopolitical_events.csv', parse_dates=['Date'])

print(f"✅ Loaded {len(df)} price records")
print(f"✅ Loaded {len(change_points)} change points")
print(f"✅ Loaded {len(events)} events")

# ═══════════════════════════════════════════════════════════
# API ENDPOINTS
# ═══════════════════════════════════════════════════════════

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'data_loaded': {
            'prices': len(df),
            'change_points': len(change_points),
            'events': len(events)
        }
    })

@app.route('/api/prices', methods=['GET'])
def get_prices():
    """Get historical price data with optional date filtering"""
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    
    data = df.copy()
    
    if start_date:
        data = data[data['Date'] >= start_date]
    if end_date:
        data = data[data['Date'] <= end_date]
    
    # Return as list of dicts for JSON serialization
    return jsonify({
        'data': data[['Date', 'Price', 'Log_Return', 'Volatility_30d']].to_dict('records'),
        'count': len(data),
        'date_range': {
            'start': data['Date'].min().strftime('%Y-%m-%d') if len(data) > 0 else None,
            'end': data['Date'].max().strftime('%Y-%m-%d') if len(data) > 0 else None
        }
    })

@app.route('/api/change-points', methods=['GET'])
def get_change_points():
    """Get detected change points with statistics"""
    return jsonify({
        'change_points': change_points.to_dict('records'),
        'count': len(change_points),
        'summary': {
            'avg_volatility_ratio': float(change_points['vol_ratio'].mean()),
            'max_impact': float(change_points['daily_impact'].min()),  # Most negative
            'events_covered': change_points['event_name'].tolist()
        }
    })

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get geopolitical events with optional category filtering"""
    category = request.args.get('category')
    
    data = events.copy()
    if category:
        data = data[data['Category'] == category]
    
    return jsonify({
        'events': data.to_dict('records'),
        'count': len(data),
        'categories': events['Category'].unique().tolist()
    })

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get summary statistics for dashboard"""
    return jsonify({
        'price_stats': {
            'mean': float(df['Price'].mean()),
            'median': float(df['Price'].median()),
            'min': float(df['Price'].min()),
            'max': float(df['Price'].max()),
            'std': float(df['Price'].std())
        },
        'return_stats': {
            'mean_daily': float(df['Log_Return'].mean()),
            'volatility_annual': float(df['Log_Return'].std() * np.sqrt(252)),
            'sharpe_ratio': float(df['Log_Return'].mean() / df['Log_Return'].std() * np.sqrt(252))
        },
        'regimes': [
            {
                'name': cp['event_name'],
                'date': cp['date'].strftime('%Y-%m-%d'),
                'volatility_ratio': float(cp['vol_ratio']),
                'daily_impact': float(cp['daily_impact'])
            }
            for _, cp in change_points.iterrows()
        ]
    })

@app.route('/api/analysis/<event_name>', methods=['GET'])
def get_event_analysis(event_name):
    """Get detailed analysis for specific event"""
    # Find change point
    cp = change_points[change_points['event_name'] == event_name]
    
    if len(cp) == 0:
        return jsonify({'error': 'Event not found'}), 404
    
    cp = cp.iloc[0]
    
    # Get window around event
    event_date = pd.Timestamp(cp['date'])
    window_start = event_date - pd.Timedelta(days=180)
    window_end = event_date + pd.Timedelta(days=180)
    
    window_data = df[(df['Date'] >= window_start) & (df['Date'] <= window_end)]
    
    return jsonify({
        'event': cp.to_dict(),
        'window': {
            'start': window_start.strftime('%Y-%m-%d'),
            'end': window_end.strftime('%Y-%m-%d'),
            'data': window_data[['Date', 'Price', 'Log_Return']].to_dict('records')
        }
    })

# ═══════════════════════════════════════════════════════════
# RUN SERVER
# ═══════════════════════════════════════════════════════════

if __name__ == '__main__':
    print("\n🚀 Starting Flask server...")
    print("📊 Dashboard API available at: http://localhost:5000")
    print("\nEndpoints:")
    print("  GET /api/health")
    print("  GET /api/prices?start=YYYY-MM-DD&end=YYYY-MM-DD")
    print("  GET /api/change-points")
    print("  GET /api/events?category=Conflict")
    print("  GET /api/statistics")
    print("  GET /api/analysis/<event_name>")
    print("\nPress Ctrl+C to stop\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)