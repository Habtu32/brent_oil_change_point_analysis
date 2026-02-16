"""
Data loading utilities for Brent oil prices.
"""
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from typing import Optional, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BrentDataLoader:
    """
    Handles loading and initial validation of Brent oil price data.
    """
    
    def __init__(self, data_path: str):
        self.data_path = Path(data_path)
        self.raw_df: Optional[pd.DataFrame] = None
        self.validation_report: Dict[str, Any] = {}
        
    def load(self) -> pd.DataFrame:
        """
        Load data from CSV with automatic format detection.
        
        Returns:
            pd.DataFrame: Raw data with columns ['Date', 'Price']
        """
        logger.info(f"Loading data from {self.data_path}")
        
        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")
        
        # Try different parsing strategies
        try:
            df = pd.read_csv(self.data_path)
        except Exception as e:
            logger.warning(f"Standard read failed, trying alternatives: {e}")
            try:
                df = pd.read_csv(self.data_path, sep='\t')
            except:
                df = pd.read_csv(self.data_path, sep=';')
        
        # Standardize column names
        df.columns = [col.strip().title() for col in df.columns]
        
        # Ensure required columns exist
        required = ['Date', 'Price']
        missing = [col for col in required if col not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}. Found: {df.columns.tolist()}")
        
        self.raw_df = df.copy()
        logger.info(f"Loaded {len(df)} rows")
        return df
    
    def validate(self) -> dict:
        """
        Run data quality checks.
        
        Returns:
            dict: Validation results
        """
        if self.raw_df is None:
            self.load()
            
        if self.raw_df is None:
            raise ValueError("Data could not be loaded")

        df = self.raw_df
        report = {
            'total_rows': len(df),
            'missing_dates': df['Date'].isnull().sum(),
            'missing_prices': df['Price'].isnull().sum(),
            'duplicate_dates': df['Date'].duplicated().sum(),
            'negative_prices': (df['Price'] < 0).sum(),
            'zero_prices': (df['Price'] == 0).sum(),
            'price_range': {
                'min': df['Price'].min(),
                'max': df['Price'].max()
            }
        }
        
        # Check date parsing
        try:
            pd.to_datetime(df['Date'])
            report['date_parseable'] = True
        except:
            report['date_parseable'] = False
            
        self.validation_report = report
        logger.info(f"Validation complete: {report}")
        return report
    
    def get_summary(self) -> str:
        """Generate human-readable summary."""
        if not self.validation_report:
            self.validate()
            
        if self.raw_df is None:
            raise ValueError("Data could not be loaded")

        r = self.validation_report
        summary = f"""
        === BRENT OIL DATA SUMMARY ===
        Total Records: {r['total_rows']:,}
        Date Range: {self.raw_df['Date'].min()} to {self.raw_df['Date'].max()}
        Price Range: ${r['price_range']['min']:.2f} - ${r['price_range']['max']:.2f}
        
        Quality Checks:
        - Missing Dates: {r['missing_dates']}
        - Missing Prices: {r['missing_prices']}
        - Duplicate Dates: {r['duplicate_dates']}
        - Negative Prices: {r['negative_prices']}
        - Zero Prices: {r['zero_prices']}
        ==============================
        """
        return summary


# Convenience function
def load_brent_data(file_path: str) -> pd.DataFrame:
    """Quick load function."""
    loader = BrentDataLoader(file_path)
    df = loader.load()
    print(loader.get_summary())
    return df


if __name__ == "__main__":
    # Test the loader
    test_path = "../../data/raw/BrentOilPrices.csv"
    df = load_brent_data(test_path)
    print(df.head())