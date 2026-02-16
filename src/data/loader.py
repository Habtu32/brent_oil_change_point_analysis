"""
Data loading utilities for Brent oil price analysis.
"""

import logging
from pathlib import Path
from typing import Optional, Tuple

import pandas as pd

from config.settings import DATA_CONFIG

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BrentDataLoader:
    """
    Handles loading and initial validation of Brent oil price data.
    
    Attributes:
        data_path: Path to the raw CSV file
        df: Loaded DataFrame
    """
    
    def __init__(self, data_path: Optional[Path] = None) -> None:
        """
        Initialize loader with data path.
        
        Args:
            data_path: Optional custom path, defaults to config
        """
        self.data_path = data_path or DATA_CONFIG.raw_data_path
        self.df: Optional[pd.DataFrame] = None
        self.validation_report: dict = {}
        
    def load(self) -> pd.DataFrame:
        """
        Load data from CSV with automatic format detection.
        
        Returns:
            DataFrame with raw data
            
        Raises:
            FileNotFoundError: If data file doesn't exist
            ValueError: If required columns missing
        """
        logger.info(f"Loading data from {self.data_path}")
        
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        
        # Try different separators
        try:
            df = pd.read_csv(self.data_path)
        except Exception:
            try:
                df = pd.read_csv(self.data_path, sep='\t')
            except Exception:
                df = pd.read_csv(self.data_path, sep=';')
        
        # Standardize column names
        df.columns = [col.strip().title() for col in df.columns]
        
        # Validate required columns
        required = ['Date', 'Price']
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}. Found: {df.columns.tolist()}")
        
        self.df = df.copy()
        logger.info(f"Loaded {len(df)} rows")
        return df
    
    def validate(self) -> dict:
        """
        Run data quality checks.
        
        Returns:
            Dictionary with validation results
        """
        if self.df is None:
            self.load()
            
        df = self.df
        report = {
            'total_rows': len(df),
            'missing_dates': int(df['Date'].isnull().sum()),
            'missing_prices': int(df['Price'].isnull().sum()),
            'duplicate_dates': int(df['Date'].duplicated().sum()),
            'negative_prices': int((df['Price'] < 0).sum()),
            'zero_prices': int((df['Price'] == 0).sum()),
            'price_range': {
                'min': float(df['Price'].min()),
                'max': float(df['Price'].max())
            }
        }
        
        # Check date parsing
        try:
            pd.to_datetime(df['Date'])
            report['date_parseable'] = True
        except Exception:
            report['date_parseable'] = False
            
        self.validation_report = report
        logger.info(f"Validation complete: {report}")
        return report
    
    def get_summary(self) -> str:
        """Generate human-readable summary."""
        if not self.validation_report:
            self.validate()
            
        r = self.validation_report
        return f"""
=== BRENT OIL DATA SUMMARY ===
Total Records: {r['total_rows']:,}
Price Range: ${r['price_range']['min']:.2f} - ${r['price_range']['max']:.2f}

Quality Checks:
- Missing Dates: {r['missing_dates']}
- Missing Prices: {r['missing_prices']}
- Duplicate Dates: {r['duplicate_dates']}
- Negative Prices: {r['negative_prices']}
==============================
"""


def load_brent_data(data_path: Optional[Path] = None) -> Tuple[pd.DataFrame, BrentDataLoader]:
    """
    Quick load function with validation.
    
    Args:
        data_path: Optional custom path
        
    Returns:
        Tuple of (DataFrame, loader instance)
    """
    loader = BrentDataLoader(data_path)
    df = loader.load()
    print(loader.get_summary())
    return df, loader


if __name__ == "__main__":
    # Test the loader
    df, loader = load_brent_data()
    print("\nFirst 5 rows:")
    print(df.head())
