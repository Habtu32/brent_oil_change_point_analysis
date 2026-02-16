"""
Unit tests for feature engineering module.
"""

import pytest
import pandas as pd
import numpy as np

from src.data.features import BrentFeatureEngineer, engineer_features


class TestBrentFeatureEngineer:
    """Test suite for BrentFeatureEngineer class."""
    
    def test_engineer_initialization(self, sample_clean_data: pd.DataFrame) -> None:
        """Test engineer initializes correctly."""
        engineer = BrentFeatureEngineer(sample_clean_data)
        assert len(engineer.df) == len(sample_clean_data)
        assert len(engineer.feature_list) == 0
    
    def test_add_returns(self, sample_clean_data: pd.DataFrame) -> None:
        """Test return calculations."""
        engineer = BrentFeatureEngineer(sample_clean_data)
        engineer.add_returns()
        
        assert 'Log_Price' in engineer.df.columns
        assert 'Log_Return' in engineer.df.columns
        assert 'Simple_Return' in engineer.df.columns
        assert 'Log_Return' in engineer.feature_list
    
    def test_add_volatility(self, sample_clean_data: pd.DataFrame) -> None:
        """Test volatility calculations."""
        engineer = BrentFeatureEngineer(sample_clean_data)
        engineer.add_returns()  # Required for volatility
        engineer.add_volatility(windows=[7, 30])
        
        assert 'Volatility_7d' in engineer.df.columns
        assert 'Volatility_30d' in engineer.df.columns
    
    def test_add_time_features(self, sample_clean_data: pd.DataFrame) -> None:
        """Test time feature extraction."""
        engineer = BrentFeatureEngineer(sample_clean_data)
        engineer.add_time_features()
        
        assert 'Year' in engineer.df.columns
        assert 'Month' in engineer.df.columns
        assert 'Quarter' in engineer.df.columns
        assert engineer.df['Year'].iloc[0] == 2020
    
    def test_add_moving_averages(self, sample_clean_data: pd.DataFrame) -> None:
        """Test moving average calculations."""
        engineer = BrentFeatureEngineer(sample_clean_data)
        engineer.add_moving_averages(windows=[10, 30])
        
        assert 'MA_10' in engineer.df.columns
        assert 'MA_30' in engineer.df.columns
        assert 'Price_to_MA_10' in engineer.df.columns
    
    def test_engineer_full_pipeline(self, sample_clean_data: pd.DataFrame) -> None:
        """Test complete feature engineering pipeline."""
        result_df = engineer_features(sample_clean_data)
        
        expected_features = [
            'Log_Price', 'Log_Return', 'Simple_Return',
            'Volatility_7d', 'Volatility_30d', 'Volatility_90d',
            'Year', 'Month', 'Quarter', 'DayOfYear', 'DayOfWeek',
            'MA_10', 'MA_30', 'MA_100', 'MA_200'
        ]
        
        for feature in expected_features:
            assert feature in result_df.columns, f"Missing feature: {feature}"


class TestEngineerFeatures:
    """Test suite for engineer_features function."""
    
    def test_function_returns_dataframe(self, sample_clean_data: pd.DataFrame) -> None:
        """Test function returns DataFrame."""
        result = engineer_features(sample_clean_data)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == len(sample_clean_data)