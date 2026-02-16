"""
Data cleaning and preprocessing for Brent oil analysis.
"""

import logging
from typing import Optional

import numpy as np
import pandas as pd

from config.settings import DATA_CONFIG

logger = logging.getLogger(__name__)


class BrentDataCleaner:
    """
    Cleans and prepares Brent oil data for analysis.
    
    Attributes:
        raw_df: Input DataFrame
        clean_df: Processed DataFrame
    """
    
    def __init__(self, df: pd.DataFrame) -> None:
        """
        Initialize cleaner with raw data.
        
        Args:
            df: Raw DataFrame with Date and Price columns
        """
        self.raw_df = df.copy()
        self.clean_df: Optional[pd.DataFrame] = None
        
    def parse_dates(self, date_format: Optional[str] = None) -> 'BrentDataCleaner':
        """
        Parse date strings to datetime objects.
        
        Args:
            date_format: Optional format string, defaults to config
            
        Returns:
            Self for method chaining
        """
        fmt = date_format or DATA_CONFIG.date_format
        logger.info(f"Parsing dates with format: {fmt}")
        
        self.raw_df['Date'] = pd.to_datetime(
            self.raw_df['Date'], 
            format=fmt,
            errors='coerce'
        )
        
        # Drop invalid dates
        invalid = self.raw_df['Date'].isnull().sum()
        if invalid > 0:
            logger.warning(f"Dropping {invalid} rows with invalid dates")
            self.raw_df = self.raw_df.dropna(subset=['Date'])
        
        return self
    
    def sort_and_index(self) -> 'BrentDataCleaner':
        """Sort by date and reset index."""
        logger.info("Sorting by date...")
        self.raw_df = self.raw_df.sort_values('Date').reset_index(drop=True)
        return self
    
    def handle_missing_prices(self, method: str = 'interpolate') -> 'BrentDataCleaner':
        """
        Handle missing price values.
        
        Args:
            method: 'interpolate', 'forward_fill', 'drop', or 'mean'
            
        Returns:
            Self for method chaining
        """
        missing = self.raw_df['Price'].isnull().sum()
        if missing == 0:
            return self
            
        logger.info(f"Handling {missing} missing prices using {method}")
        
        if method == 'interpolate':
            self.raw_df['Price'] = self.raw_df['Price'].interpolate(method='linear')
        elif method == 'forward_fill':
            self.raw_df['Price'] = self.raw_df['Price'].fillna(method='ffill')
        elif method == 'drop':
            self.raw_df = self.raw_df.dropna(subset=['Price'])
        elif method == 'mean':
            self.raw_df['Price'] = self.raw_df['Price'].fillna(self.raw_df['Price'].mean())
            
        return self
    
    def clean(self) -> pd.DataFrame:
        """
        Execute cleaning pipeline and return clean data.
        
        Returns:
            Cleaned DataFrame
        """
        self.clean_df = self.raw_df.copy()
        logger.info(f"Cleaning complete: {len(self.clean_df)} rows")
        return self.clean_df


def clean_brent_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Quick clean function with default settings.
    
    Args:
        df: Raw DataFrame
        
    Returns:
        Cleaned DataFrame
    """
    cleaner = BrentDataCleaner(df)
    return (cleaner
            .parse_dates()
            .sort_and_index()
            .handle_missing_prices(method='interpolate')
            .clean())


if __name__ == "__main__":
    # Test
    from src.data.loader import load_brent_data
    
    df, _ = load_brent_data()
    clean_df = clean_brent_data(df)
    print(f"\nClean data: {len(clean_df)} rows")
    print(clean_df.head())
