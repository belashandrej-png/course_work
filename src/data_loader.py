"""
Data Loader Module

Handles downloading and loading financial data from Alpha Vantage API.
"""

import requests
import json
from typing import Dict, Any, Optional
from pathlib import Path


class DataLoader:
    """Class for loading financial data from Alpha Vantage API."""
    
    BASE_URL = "https://www.alphavantage.co/query"
    
    def __init__(self, api_key: str):
        """
        Initialize DataLoader.
        
        Args:
            api_key: Alpha Vantage API key
        """
        self.api_key = api_key
        self.session = requests.Session()
    
    def get_cash_flow_data(self, symbol: str = "NFLX") -> Dict[str, Any]:
        """
        Get cash flow statement data for a given symbol.
        
        Args:
            symbol: Stock ticker symbol (default: NFLX)
        
        Returns:
            Dictionary containing cash flow data
        
        Raises:
            requests.RequestException: If API request fails
        """
        params = {
            "function": "CASH_FLOW",
            "symbol": symbol,
            "apikey": self.api_key
        }
        
        response = self.session.get(self.BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if "Error Message" in data:
            raise ValueError(f"API Error: {data['Error Message']}")
        
        return data
    
    def save_to_json(self, data: Dict[str, Any], filepath: str) -> None:
        """
        Save data to JSON file.
        
        Args:
            data: Data to save
            filepath: Path to output file
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    
    def load_from_json(self, filepath: str) -> Dict[str, Any]:
        """
        Load data from JSON file.
        
        Args:
            filepath: Path to JSON file
        
        Returns:
            Loaded data as dictionary
        """
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
