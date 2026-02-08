"""
Feature engineering for Brent oil time series analysis.
"""
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)

class BrentFeatureEngineer:
    """
    Creates features for change point analysis and modeling.
    """
    
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.feature_list = []
        
    def add_returns(self) -> 'BrentFeatureEngineer':
        """Calculate log and simple returns."""
        logger.info("Calculating returns...")
        
        # Log returns: more stable, time-additive
        self.df['Log_Price'] = np.log(self.df['Price'])
        self.df['Log_Return'] = self.df['Log_Price'].diff()
        
        # Simple returns: intuitive percentage change
        self.df['Simple_Return'] = self.df['Price'].pct_change()
        
        self.feature_list.extend(['Log_Price', 'Log_Return', 'Simple_Return'])
        return self
    
    def add_volatility(self, windows: list = [7, 30, 90]) -> 'BrentFeatureEngineer':
        """
        Calculate rolling volatility (annualized).
        
        Args:
            windows: List of day windows for rolling std
        """
        logger.info(f"Calculating volatility for windows: {windows}")
        
        for window in windows:
            col_name = f'Volatility_{window}d'
            # Annualized volatility: std * sqrt(252 trading days)
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
        self.df['IsMonthEnd'] = self.df['Date'].dt.is_month_end
        
        self.feature_list.extend(['Year', 'Month', 'Quarter', 'DayOfYear', 'DayOfWeek', 'IsMonthEnd'])
        return self
    
    def add_moving_averages(self, windows: list = [10, 30, 100, 200]) -> 'BrentFeatureEngineer':
        """Add moving averages and ratios."""
        logger.info(f"Adding moving averages: {windows}")
        
        for window in windows:
            ma_col = f'MA_{window}'
            ratio_col = f'Price_to_MA_{window}'
            
            self.df[ma_col] = self.df['Price'].rolling(window=window, min_periods=1).mean()
            self.df[ratio_col] = self.df['Price'] / self.df[ma_col]
            
            self.feature_list.extend([ma_col, ratio_col])
            
        return self
    
    def add_trend_features(self) -> 'BrentFeatureEngineer':
        """Add trend and momentum indicators."""
        logger.info("Adding trend features...")
        
        # Price momentum (change over past n days)
        for lag in [1, 5, 10, 30]:
            self.df[f'Momentum_{lag}d'] = self.df['Price'].diff(lag)
            self.feature_list.append(f'Momentum_{lag}d')
        
        # Cumulative return from start of series
        self.df['Cumulative_Return'] = (1 + self.df['Simple_Return'].fillna(0)).cumprod() - 1
        self.feature_list.append('Cumulative_Return')
        
        return self
    
    def engineer(self) -> pd.DataFrame:
        """Execute full feature engineering pipeline."""
        (self.add_returns()
             .add_volatility()
             .add_time_features()
             .add_moving_averages()
             .add_trend_features())
        
        logger.info(f"Created {len(self.feature_list)} features")
        return self.df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Quick feature engineering function.
    
    Args:
        df: Clean DataFrame with Date and Price columns
        
    Returns:
        DataFrame with engineered features
    """
    engineer = BrentFeatureEngineer(df)
    return engineer.engineer()


if __name__ == "__main__":
    # Test feature engineering
    import sys
    sys.path.append('..')
    from data.load_data import load_brent_data
    from data.clean_data import clean_brent_data
    
    # Load and clean
    raw = load_brent_data("../../data/raw/BrentOilPrices.csv")
    clean = clean_brent_data(raw)
    
    # Engineer features
    featured = engineer_features(clean)
    
    print("\nEngineered features:")
    print(featured[['Date', 'Price', 'Log_Return', 'Volatility_30d', 'MA_30', 'Momentum_30d']].head())
    print(f"\nTotal columns: {len(featured.columns)}")
    print(f"Feature columns: {len([c for c in featured.columns if c not in ['Date', 'Price']])}")