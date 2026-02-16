"""
Configuration settings for Brent Oil Change Point Analysis.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True)
class DataConfig:
    """Data loading and processing configuration."""
    raw_data_path: Path = Path("data/raw/BrentOilPrices.csv")
    processed_data_path: Path = Path("data/processed/features_engineered.csv")
    change_points_path: Path = Path("data/processed/change_point_results.csv")
    events_path: Path = Path("data/external/geopolitical_events.csv")
    
    date_format: str = "%d-%b-%y"
    min_date: str = "1987-05-20"
    max_date: str = "2022-09-30"


@dataclass(frozen=True)
class ModelConfig:
    """Bayesian model configuration."""
    n_draws: int = 2000
    n_tune: int = 1000
    n_chains: int = 4
    target_accept: float = 0.9
    random_seed: int = 42
    
    # Convergence thresholds
    max_r_hat: float = 1.01
    min_ess: int = 400


@dataclass(frozen=True)
class DashboardConfig:
    """Dashboard configuration."""
    api_host: str = "0.0.0.0"
    api_port: int = 5000
    frontend_port: int = 3000
    
    # Data sampling for performance
    chart_sample_rate: int = 10  # Show every 10th point
    
    # Date display
    default_start_date: str = "2010-01-01"
    default_end_date: str = "2022-12-31"


# Global instances
DATA_CONFIG = DataConfig()
MODEL_CONFIG = ModelConfig()
DASHBOARD_CONFIG = DashboardConfig()
