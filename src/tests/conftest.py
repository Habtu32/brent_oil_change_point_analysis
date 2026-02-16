"""
Pytest configuration and fixtures.
"""
import sys
import os
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to Python path for proper imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

@pytest.fixture
def sample_raw_data() -> pd.DataFrame:
    """Create sample raw data for testing."""
    dates = pd.date_range(start='2020-01-01', periods=100, freq='D')
    prices = 50 + np.random.randn(100).cumsum() * 2
    return pd.DataFrame({
        'Date': dates.strftime('%d-%b-%y'),
        'Price': prices
    })

@pytest.fixture
def sample_clean_data() -> pd.DataFrame:
    """Create sample clean data for testing."""
    dates = pd.date_range(start='2020-01-01', periods=100, freq='D')
    prices = 50 + np.random.randn(100).cumsum() * 2
    return pd.DataFrame({
        'Date': dates,
        'Price': prices
    })

@pytest.fixture
def temp_csv_file(tmp_path: Path) -> Path:
    """Create temporary CSV file for testing."""
    csv_path = tmp_path / "test_data.csv"
    dates = pd.date_range(start='2020-01-01', periods=10, freq='D')
    prices = [50.0] * 10
    df = pd.DataFrame({
        'Date': dates.strftime('%d-%b-%y'),
        'Price': prices
    })
    df.to_csv(csv_path, index=False)
    return csv_path
