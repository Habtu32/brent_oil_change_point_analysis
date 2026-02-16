"""
Unit tests for data cleaning module.
"""

import pytest
import pandas as pd
import numpy as np

from src.data.cleaner import BrentDataCleaner, clean_brent_data


class TestBrentDataCleaner:
    """Test suite for BrentDataCleaner class."""
    
    def test_cleaner_initialization(self, sample_raw_data: pd.DataFrame) -> None:
        """Test cleaner initializes correctly."""
        cleaner = BrentDataCleaner(sample_raw_data)
        assert len(cleaner.raw_df) == len(sample_raw_data)
        assert cleaner.clean_df is None
    
    def test_parse_dates(self, sample_raw_data: pd.DataFrame) -> None:
        """Test date parsing converts to datetime."""
        cleaner = BrentDataCleaner(sample_raw_data)
        cleaner.parse_dates()
        
        assert pd.api.types.is_datetime64_any_dtype(cleaner.raw_df['Date'])
    
    def test_parse_dates_invalid_format(self) -> None:
        """Test parse_dates handles invalid dates."""
        df = pd.DataFrame({
            'Date': ['invalid', '02-Jan-20', '03-Jan-20'],
            'Price': [50.0, 51.0, 52.0]
        })
        cleaner = BrentDataCleaner(df)
        cleaner.parse_dates()
        
        # Should drop invalid row
        assert len(cleaner.raw_df) == 2
    
    def test_sort_and_index(self, sample_raw_data: pd.DataFrame) -> None:
        """Test sorting by date."""
        # Create unsorted data
        df = sample_raw_data.sample(frac=1).reset_index(drop=True)
        cleaner = BrentDataCleaner(df)
        cleaner.parse_dates()  # Parse dates before sorting
        cleaner.sort_and_index()
        
        # Check sorted
        dates = pd.to_datetime(cleaner.raw_df['Date'])
        assert dates.is_monotonic_increasing
    
    def test_handle_missing_prices_interpolate(self) -> None:
        """Test missing price interpolation."""
        df = pd.DataFrame({
            'Date': ['01-Jan-20', '02-Jan-20', '03-Jan-20'],
            'Price': [50.0, np.nan, 52.0]
        })
        cleaner = BrentDataCleaner(df)
        cleaner.handle_missing_prices(method='interpolate')
        
        assert not cleaner.raw_df['Price'].isnull().any()
        assert cleaner.raw_df['Price'].iloc[1] == 51.0  # Interpolated
    
    def test_clean_returns_dataframe(self, sample_raw_data: pd.DataFrame) -> None:
        """Test clean returns valid DataFrame."""
        cleaner = BrentDataCleaner(sample_raw_data)
        clean_df = cleaner.clean()
        
        assert isinstance(clean_df, pd.DataFrame)
        assert len(clean_df) > 0


class TestCleanBrentData:
    """Test suite for clean_brent_data function."""
    
    def test_full_pipeline(self, sample_raw_data: pd.DataFrame) -> None:
        """Test complete cleaning pipeline."""
        clean_df = clean_brent_data(sample_raw_data)
        
        assert isinstance(clean_df, pd.DataFrame)
        assert pd.api.types.is_datetime64_any_dtype(clean_df['Date'])
        assert clean_df['Date'].is_monotonic_increasing