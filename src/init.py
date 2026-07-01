"""
Netflix Cash Flow Analysis Package

This package provides tools for analyzing Netflix's cash flow statements
using data from Alpha Vantage API.
"""

__version__ = "1.0.0"
__author__ = "Andrei Belash"

from src.data_loader import DataLoader
from src.data_processor import DataProcessor
from src.visualizer import Visualizer

__all__ = ["DataLoader", "DataProcessor", "Visualizer"]
