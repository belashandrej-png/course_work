"""
Main Module

Main entry point for Netflix cash flow analysis.
"""

import os
from dotenv import load_dotenv
from src.data_loader import DataLoader
from src.data_processor import DataProcessor
from src.visualizer import Visualizer


def main():
    """Main function to run the analysis."""
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        raise ValueError(
            "API key not found. Please set ALPHA_VANTAGE_API_KEY in .env file"
        )
    
    # Initialize components
    loader = DataLoader(api_key=api_key)
    
    # Load data
    print("Loading data from Alpha Vantage API...")
    data = loader.get_cash_flow_data(symbol="NFLX")
    
    # Save raw data
    loader.save_to_json(data, "data/netflix_cashflow_raw.json")
    print("Raw data saved to data/netflix_cashflow_raw.json")
    
    # Process data
    print("Processing data...")
    processor = DataProcessor(data)
    df = processor.process_annual_reports()
    
    # Convert to numeric
    numeric_cols = [
        "operatingCashflow",
        "capitalExpenditures",
        "dividendPayout"
    ]
    df = processor.convert_to_numeric(numeric_cols)
    
    # Calculate free cash flow
    df = processor.calculate_free_cashflow()
    
    # Calculate rolling averages
    df = processor.calculate_rolling_average("operatingCashflow", window=2)
    df = processor.calculate_rolling_average("operatingCashflow", window=3)
    
    # Sort by date
    df = processor.sort_by_date(ascending=False)
    
    # Rename columns for display
    column_mapping = {
        "fiscalDateEnding": "Report Date",
        "operatingCashflow": "Operating Cash Flow",
        "capitalExpenditures": "Capital Expenditures",
        "dividendPayout": "Dividend Payout",
        "freeCashflow": "Free Cash Flow"
    }
    df_display = processor.rename_columns(column_mapping)
    
    # Display summary
    print("\n" + "="*80)
    print("NETFLIX CASH FLOW ANALYSIS SUMMARY")
    print("="*80)
    print(f"\nTotal years of data: {len(df)}")
    print(f"Date range: {df['Report Date'].min()} to {df['Report Date'].max()}")
    
    print("\nKey Metrics (Latest Year):")
    print("-" * 40)
    latest = df_display.iloc[0]
    for col in ["Operating Cash Flow", "Capital Expenditures", "Free Cash Flow"]:
        if col in latest:
            value = latest[col]
            if abs(value) >= 1e9:
                print(f"{col:30s}: ${value/1e9:,.2f}B")
            else:
                print(f"{col:30s}: ${value/1e6:,.2f}M")
    
    # Visualize
    print("\nGenerating visualizations...")
    viz = Visualizer(df, output_dir="output")
    viz.show_all_plots()
    
    print("\nAnalysis complete! Check the 'output' folder for visualizations.")


if __name__ == "__main__":
    main()
