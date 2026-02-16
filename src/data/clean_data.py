"""
Data cleaning and preprocessing for Brent oil analysis.
"""
import pandas as pd
import numpy as np
from datetime import datetime
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class BrentDataCleaner:
    """
    Cleans and prepares Brent oil data for analysis.
    """
    
    def __init__(self, df: pd.DataFrame):
        self.raw_df = df.copy()
        self.clean_df: Optional[pd.DataFrame] = None
        
    def parse_dates(self, date_format: str = '%d-%b-%y') -> 'BrentDataCleaner':
        """
        Parse date strings to datetime objects.
        
        Args:
            date_format: Format string for pd.to_datetime
        """
        logger.info("Parsing dates...")
        self.raw_df['Date'] = pd.to_datetime(
            self.raw_df['Date'], 
            format=date_format,
            errors='coerce'  # Convert errors to NaT
        )
        
        # Drop rows with unparseable dates
        invalid_dates = self.raw_df['Date'].isnull().sum()
        if invalid_dates > 0:
            logger.warning(f"Dropping {invalid_dates} rows with invalid dates")
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
    
    def remove_outliers(self, method: str = 'none', threshold: float = 3.0) -> 'BrentDataCleaner':
        """
        Handle extreme outliers (optional).
        
        Args:
            method: 'none', 'iqr', or 'zscore'
            threshold: Z-score threshold if method='zscore'
        """
        if method == 'none':
            return self
            
        logger.info(f"Removing outliers using {method}")
        
        if method == 'iqr':
            Q1 = self.raw_df['Price'].quantile(0.25)
            Q3 = self.raw_df['Price'].quantile(0.75)
            IQR = Q3 - Q1
            mask = (self.raw_df['Price'] >= Q1 - 1.5*IQR) & (self.raw_df['Price'] <= Q3 + 1.5*IQR)
            removed = (~mask).sum()
            self.raw_df = self.raw_df[mask]
            logger.info(f"Removed {removed} outliers")
            
        elif method == 'zscore':
            z_scores = np.abs((self.raw_df['Price'] - self.raw_df['Price'].mean()) / self.raw_df['Price'].std())
            mask = z_scores < threshold
            removed = (~mask).sum()
            self.raw_df = self.raw_df[mask]
            logger.info(f"Removed {removed} outliers")
            
        return self
    
    def clean(self) -> pd.DataFrame:
        """Execute cleaning pipeline and return clean data."""
        self.clean_df = self.raw_df.copy()
        if self.clean_df is None:
             raise ValueError("Failed to create clean dataframe")
        logger.info(f"Cleaning complete: {len(self.clean_df)} rows")
        return self.clean_df


def clean_brent_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Quick clean function with default settings.
    
    Args:
        df: Raw DataFrame with Date and Price columns
        
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
    # Test cleaning
    from load_data import load_brent_data
    
    raw_df = load_brent_data("../../data/raw/BrentOilPrices.csv")
    clean_df = clean_brent_data(raw_df)
    
    print("\nClean data sample:")
    print(clean_df.head())
    print(f"\nDate range: {clean_df['Date'].min()} to {clean_df['Date'].max()}")