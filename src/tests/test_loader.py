"""
Unit tests for data loading module.
"""

import pytest
import pandas as pd
from pathlib import Path

from src.data.loader import BrentDataLoader, load_brent_data


class TestBrentDataLoader:
    """Test suite for BrentDataLoader class."""
    
    def test_loader_initialization(self) -> None:
        """Test loader initializes with correct defaults."""
        loader = BrentDataLoader()
        assert loader.data_path.name == "BrentOilPrices.csv"
        assert loader.df is None
        assert isinstance(loader.validation_report, dict)
    
    def test_loader_custom_path(self, temp_csv_file: Path) -> None:
        """Test loader accepts custom path."""
        loader = BrentDataLoader(data_path=temp_csv_file)
        assert loader.data_path == temp_csv_file
    
    def test_load_returns_dataframe(self, temp_csv_file: Path) -> None:
        """Test load returns valid DataFrame."""
        loader = BrentDataLoader(data_path=temp_csv_file)
        df = loader.load()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 10
        assert 'Date' in df.columns
        assert 'Price' in df.columns
    
    def test_load_missing_file(self) -> None:
        """Test load raises error for missing file."""
        loader = BrentDataLoader(data_path=Path("nonexistent.csv"))
        
        with pytest.raises(FileNotFoundError):
            loader.load()
    
    def test_validate_creates_report(self, temp_csv_file: Path) -> None:
        """Test validate creates validation report."""
        loader = BrentDataLoader(data_path=temp_csv_file)
        loader.load()
        report = loader.validate()
        
        assert isinstance(report, dict)
        assert 'total_rows' in report
        assert 'missing_dates' in report
        assert 'price_range' in report
        assert report['total_rows'] == 10
    
    def test_get_summary_returns_string(self, temp_csv_file: Path) -> None:
        """Test get_summary returns formatted string."""
        loader = BrentDataLoader(data_path=temp_csv_file)
        loader.load()
        summary = loader.get_summary()
        
        assert isinstance(summary, str)
        assert "BRENT OIL DATA SUMMARY" in summary
        assert "Total Records" in summary


class TestLoadBrentData:
    """Test suite for load_brent_data function."""
    
    def test_returns_tuple(self, temp_csv_file: Path) -> None:
        """Test function returns tuple of DataFrame and loader."""
        df, loader = load_brent_data(data_path=temp_csv_file)
        
        assert isinstance(df, pd.DataFrame)
        assert isinstance(loader, BrentDataLoader)
        assert len(df) == 10