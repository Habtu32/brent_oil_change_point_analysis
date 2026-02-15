"""
Feature engineering for Brent oil time series analysis.
"""

import logging
from typing import List, Optional

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


class BrentFeatureEngineer:
    """
    Creates features for change point analysis and modeling.
    
    Attributes:
        df: Input DataFrame
        feature_list: List of created feature names
    """
    
    def __init__(self, df: pd.DataFrame) -> None:
        """
        Initialize engineer with clean data.
        
        Args:
            df: Cleaned DataFrame with Date and Price columns
        """
        self.df = df.copy()
        self.feature_list: List[str] = []
        
    def add_returns(self) -> 'BrentFeatureEngineer':
        """Calculate log and simple returns."""
        logger.info("Calculating returns...")
        
        # Log returns: time-additive, stabilize variance
        self.df['Log_Price'] = np.log(self.df['Price'])
        self.df['Log_Return'] = self.df['Log_Price'].diff()
        
        # Simple returns: intuitive percentage
        self.df['Simple_Return'] = self.df['Price'].pct_change()
        
        self.feature_list.extend(['Log_Price', 'Log_Return', 'Simple_Return'])
        return self
    
    def add_volatility(self, windows: Optional[List[int]] = None) -> 'BrentFeatureEngineer':
        """
        Calculate rolling volatility (annualized).
        
        Args:
            windows: List of day windows, defaults to [7, 30, 90]
            
        Returns:
            Self for method chaining
        """
        windows = windows or [7, 30, 90]
        logger.info(f"Calculating volatility for windows: {windows}")
        
        for window in windows:
            col_name = f'Volatility_{window}d'
            # Annualized: std * sqrt(252 trading days)
            self.df[col_name] = (
                self.df['Log_Return']
                .rolling(window=window, min_periods=window//2)
                .std() * np.sqrt(252)
            )
            self.feature_list.append(col_name)
            
        return self
    
    def add_time_features(self) -> 'BrentFeatureEngineer':
        """Extract time-based features."""
        logger.info("Adding time features...")
        
        self.df['Year'] = self.df['Date'].dt.year
        self.df['Month'] = self.df['Date'].dt.month
        self.df['Quarter'] = self.df['Date'].dt.quarter
        self.df['DayOfYear'] = self.df['Date'].dt.dayofyear
        self.df['DayOfWeek'] = self.df['Date'].dt.dayofweek
        
        self.feature_list.extend(['Year', 'Month', 'Quarter', 'DayOfYear', 'DayOfWeek'])
        return self
    
    def add_moving_averages(self, windows: Optional[List[int]] = None) -> 'BrentFeatureEngineer':
        """Add moving averages and price ratios."""
        windows = windows or [10, 30, 100, 200]
        logger.info(f"Adding moving averages: {windows}")
        
        for window in windows:
            ma_col = f'MA_{window}'
            ratio_col = f'Price_to_MA_{window}'
            
            self.df[ma_col] = self.df['Price'].rolling(window=window, min_periods=1).mean()
            self.df[ratio_col] = self.df['Price'] / self.df[ma_col]
            
            self.feature_list.extend([ma_col, ratio_col])
            
        return self
    
    def engineer(self) -> pd.DataFrame:
        """Execute full feature engineering pipeline."""
        (self.add_returns()
             .add_volatility()
             .add_time_features()
             .add_moving_averages())
        
        logger.info(f"Created {len(self.feature_list)} features")
        return self.df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Quick feature engineering function.
    
    Args:
        df: Clean DataFrame
        
    Returns:
        DataFrame with engineered features
    """
    engineer = BrentFeatureEngineer(df)
    return engineer.engineer()


if __name__ == "__main__":
    # Test
    from src.data.loader import load_brent_data
    from src.data.cleaner import clean_brent_data
    
    raw_df, _ = load_brent_data()
    clean_df = clean_brent_data(raw_df)
    featured_df = engineer_features(clean_df)
    
    print(f"\nFeatures created: {len([c for c in featured_df.columns if c not in ['Date', 'Price']])}")
    print(featured_df[['Date', 'Price', 'Log_Return', 'Volatility_30d']].head())
