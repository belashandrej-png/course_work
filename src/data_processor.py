"""
Data Processor Module

Handles data cleaning, transformation, and calculation of financial metrics.
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Any


class DataProcessor:
    """Class for processing financial data."""
    
    def __init__(self, data: Dict[str, Any]):
        """
        Initialize DataProcessor.
        
        Args:
            data: Raw data from API
        """
        self.raw_data = data
        self.df = None
    
    def process_annual_reports(self) -> pd.DataFrame:
        """
        Process annual reports from raw data.
        
        Returns:
            DataFrame with annual reports
        """
        if "annualReports" not in self.raw_data:
            raise ValueError("No annual reports found in data")
        
        self.df = pd.DataFrame(self.raw_data["annualReports"])
        return self.df
    
    def select_columns(self, columns: List[str]) -> pd.DataFrame:
        """
        Select specific columns from DataFrame.
        
        Args:
            columns: List of column names to select
        
        Returns:
            DataFrame with selected columns
        """
        if self.df is None:
            raise ValueError("No data loaded. Call process_annual_reports() first.")
        
        return self.df[columns].copy()
    
    def convert_to_numeric(self, columns: List[str]) -> pd.DataFrame:
        """
        Convert specified columns to numeric type.
        
        Args:
            columns: List of column names to convert
        
        Returns:
            DataFrame with converted columns
        """
        if self.df is None:
            raise ValueError("No data loaded")
        
        for col in columns:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(
                    self.df[col].replace("None", np.nan),
                    errors="coerce"
                ).fillna(0)
        
        return self.df
    
    def calculate_free_cashflow(self) -> pd.DataFrame:
        """
        Calculate Free Cash Flow (FCF).
        
        FCF = Operating Cash Flow - Capital Expenditures
        
        Returns:
            DataFrame with FCF column added
        """
        if self.df is None:
            raise ValueError("No data loaded")
        
        if "operatingCashflow" in self.df.columns and "capitalExpenditures" in self.df.columns:
            self.df["freeCashflow"] = (
                self.df["operatingCashflow"].astype(float) - 
                self.df["capitalExpenditures"].astype(float)
            )
        
        return self.df
    
    def calculate_rolling_average(self, column: str, window: int = 2) -> pd.DataFrame:
        """
        Calculate rolling average for specified column.
        
        Args:
            column: Column name to calculate rolling average
            window: Window size for rolling average
        
        Returns:
            DataFrame with rolling average column added
        """
        if self.df is None:
            raise ValueError("No data loaded")
        
        col_name = f"{column}_rolling_{window}y"
        self.df[col_name] = self.df[column].astype(float).rolling(window=window).mean()
        
        return self.df
    
    def sort_by_date(self, ascending: bool = True) -> pd.DataFrame:
        """
        Sort DataFrame by fiscal date ending.
        
        Args:
            ascending: Sort order (default: True)
        
        Returns:
            Sorted DataFrame
        """
        if self.df is None:
            raise ValueError("No data loaded")
        
        self.df = self.df.sort_values(
            "fiscalDateEnding",
            ascending=ascending
        ).reset_index(drop=True)
        
        return self.df
    
    def rename_columns(self, mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Rename columns according to mapping.
        
        Args:
            mapping: Dictionary of old_name: new_name
        
        Returns:
            DataFrame with renamed columns
        """
        if self.df is None:
            raise ValueError("No data loaded")
        
        self.df = self.df.rename(columns=mapping)
        return self.df
