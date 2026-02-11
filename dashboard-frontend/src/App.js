import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from 'recharts';
import axios from 'axios';
import './App.css';

const API_BASE = 'http://localhost:5000';

// Safe date formatting
const formatDate = (dateString) => {
  if (!dateString) return 'Unknown';
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return 'Invalid';
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
  } catch (e) {
    return 'Invalid';
  }
};

// Format for x-axis (shorter)
const formatAxisDate = (dateString) => {
  if (!dateString) return '';
  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return '';
    return date.getFullYear().toString(); // Just show year
  } catch (e) {
    return '';
  }
};

function App() {
  const [prices, setPrices] = useState([]);
  const [changePoints, setChangePoints] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [dateRange, setDateRange] = useState({ start: '', end: '' });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Fetch ALL data (no date filter to start)
      const params = {};
      if (dateRange.start) params.start = dateRange.start;
      if (dateRange.end) params.end = dateRange.end;
      
      console.log('Fetching with params:', params);
      
      const [pricesRes, cpRes, statsRes] = await Promise.all([
        axios.get(`${API_BASE}/api/prices`, { params, timeout: 15000 }),
        axios.get(`${API_BASE}/api/change-points`),
        axios.get(`${API_BASE}/api/statistics`)
      ]);
      
      const priceData = pricesRes.data.data || [];
      const cpData = cpRes.data.change_points || [];
      
      console.log(`Loaded ${priceData.length} prices from ${pricesRes.data.date_range?.start} to ${pricesRes.data.date_range?.end}`);
      
      setPrices(priceData);
      setChangePoints(cpData);
      setStats(statsRes.data);
      
      // Update date range inputs if we got data
      if (pricesRes.data.date_range) {
        setDateRange({
          start: pricesRes.data.date_range.start || '',
          end: pricesRes.data.date_range.end || ''
        });
      }
      
    } catch (err) {
      console.error('Error:', err);
      setError(`Failed to load: ${err.message}`);
    }
    
    setLoading(false);
  };

  // Format for chart - use every 50th point to avoid overcrowding
  const chartData = prices
    .filter((d, i) => i % 10 === 0) // Sample every 10th point for performance
    .map((d, i) => {
      try {
        const price = parseFloat(d.Price);
        return {
          index: i,
          price: isNaN(price) ? null : price,
          fullDate: d.Date,
          year: formatAxisDate(d.Date),
          displayDate: formatDate(d.Date)
        };
      } catch (e) {
        return null;
      }
    })
    .filter(d => d && d.price !== null && d.price > 0);

  // Find change point positions in chart data
  const changePointLines = changePoints.map((cp, idx) => {
    const cpDate = new Date(cp.date);
    // Find closest point in chart data
    const closestPoint = chartData.find(d => {
      const dDate = new Date(d.fullDate);
      return Math.abs(dDate - cpDate) < 1000 * 60 * 60 * 24 * 30; // Within 30 days
    });
    
    return {
      ...cp,
      x: closestPoint?.index || null,
      year: cpDate.getFullYear()
    };
  }).filter(cp => cp.x !== null);

  if (loading) return <div className="loading">Loading...</div>;
  
  if (error) return (
    <div className="error">
      <h2>Error</h2>
      <p>{error}</p>
      <button onClick={fetchData}>Retry</button>
    </div>
  );

  const actualDateRange = prices.length > 0 ? {
    start: formatDate(prices[0].Date),
    end: formatDate(prices[prices.length - 1].Date)
  } : null;

  return (
    <div className="App">
      <header className="App-header">
        <h1>🛢️ Brent Oil Change Point Dashboard</h1>
        <p>Interactive analysis of structural breaks (1987-2022)</p>
        {actualDateRange && (
          <p className="date-range">Showing: {actualDateRange.start} — {actualDateRange.end}</p>
        )}
      </header>

      {/* Controls */}
      <div className="controls">
        <label>
          Start:
          <input 
            type="date" 
            value={dateRange.start}
            onChange={(e) => setDateRange({...dateRange, start: e.target.value})}
          />
        </label>
        <label>
          End:
          <input 
            type="date" 
            value={dateRange.end}
            onChange={(e) => setDateRange({...dateRange, end: e.target.value})}
          />
        </label>
        <button onClick={fetchData}>Update Range</button>
        <button onClick={() => {setDateRange({start: '', end: ''}); fetchData();}}>Show All</button>
      </div>

      {/* Stats */}
      {stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Data Points</h3>
            <p>{prices.length.toLocaleString()}</p>
            <small>{chartData.length} displayed</small>
          </div>
          <div className="stat-card">
            <h3>Price Range</h3>
            <p>${stats.price_stats?.min?.toFixed(0)} - ${stats.price_stats?.max?.toFixed(0)}</p>
          </div>
          <div className="stat-card">
            <h3>Average</h3>
            <p>${stats.price_stats?.mean?.toFixed(2)}</p>
          </div>
          <div className="stat-card">
            <h3>Change Points</h3>
            <p>{changePoints.length}</p>
          </div>
        </div>
      )}

      {/* Main Chart */}
      <div className="chart-container">
        <h2>Brent Oil Price History ({prices.length.toLocaleString()} records)</h2>
        {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={450}>
            <LineChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
              <XAxis 
                dataKey="year"
                type="category"
                interval={0}
                angle={-45}
                textAnchor="end"
                height={80}
                tick={{ fontSize: 12 }}
              />
              <YAxis 
                domain={[0, 150]} 
                label={{ value: 'Price ($/barrel)', angle: -90, position: 'insideLeft' }}
              />
              <Tooltip 
                formatter={(value) => [`$${value.toFixed(2)}`, 'Brent Price']}
                labelFormatter={(item) => {
                  const point = chartData[item];
                  return point ? point.displayDate : '';
                }}
              />
              <Legend verticalAlign="top" height={36}/>
              <Line 
                type="monotone" 
                dataKey="price" 
                name="Brent Crude Price" 
                stroke="#2563eb" 
                strokeWidth={2}
                dot={false}
                activeDot={{ r: 6, fill: '#2563eb' }}
              />
              {changePointLines.map((cp, idx) => (
                <ReferenceLine
                  key={idx}
                  x={cp.x}
                  stroke={['#dc2626', '#ea580c', '#9333ea', '#16a34a'][idx % 4]}
                  strokeDasharray="5 5"
                  strokeWidth={2}
                  label={{ 
                    value: `${cp.year}: ${cp.event_name.split('_').slice(0,2).join(' ')}`, 
                    position: 'top',
                    fill: ['#dc2626', '#ea580c', '#9333ea', '#16a34a'][idx % 4],
                    fontSize: 11,
                    fontWeight: 'bold'
                  }}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <p>No data available</p>
        )}
      </div>

      {/* Change Point Cards */}
      <div className="change-points-section">
        <h2>Structural Break Analysis</h2>
        <div className="cp-grid">
          {changePoints.map((cp, idx) => (
            <div 
              key={idx} 
              className="cp-card"
              style={{ 
                borderTop: `4px solid ${['#dc2626', '#ea580c', '#9333ea', '#16a34a'][idx % 4]}`,
                background: 'white',
                padding: '20px',
                borderRadius: '8px',
                boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
              }}
            >
              <h3 style={{ margin: '0 0 10px 0', color: '#333' }}>
                {cp.event_name?.replace(/_/g, ' ')}
              </h3>
              <p style={{ color: '#666', margin: '0 0 15px 0' }}>
                {formatDate(cp.date)}
              </p>
              <div style={{ display: 'flex', gap: '15px', marginBottom: '10px' }}>
                <div style={{ background: '#fee2e2', padding: '5px 10px', borderRadius: '4px' }}>
                  <strong>{cp.daily_impact ? (cp.daily_impact * 100).toFixed(2) : 'N/A'}%</strong>
                  <br/><small>daily return</small>
                </div>
                <div style={{ background: '#dbeafe', padding: '5px 10px', borderRadius: '4px' }}>
                  <strong>{cp.vol_ratio ? cp.vol_ratio.toFixed(1) : 'N/A'}x</strong>
                  <br/><small>volatility</small>
                </div>
              </div>
              <div style={{ fontSize: '12px', color: '#059669', fontFamily: 'monospace' }}>
                ✅ MCMC: R-hat={cp.r_hat?.toFixed(3)}, ESS={cp.ess?.toFixed(0)}
              </div>
            </div>
          ))}
        </div>
      </div>

      <footer style={{ textAlign: 'center', padding: '30px', color: '#666', marginTop: '30px' }}>
        <p>Brent Oil Change Point Analysis | 10 Academy Week 11 | February 2026</p>
        <p>Bayesian structural break detection with PyMC</p>
      </footer>
    </div>
  );
}

export default App;