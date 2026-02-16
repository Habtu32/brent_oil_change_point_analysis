"""
Pytest configuration file to set up proper import paths.
This file is automatically loaded by pytest to configure the test environment.
"""

import sys
import os

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)