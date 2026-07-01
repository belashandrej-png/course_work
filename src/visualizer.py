"""
Visualizer Module

Creates visualizations for financial data analysis.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from typing import Optional, List
from pathlib import Path


class Visualizer:
    """Class for creating financial data visualizations."""
    
    def __init__(self, df: pd.DataFrame, output_dir: str = "output"):
        """
        Initialize Visualizer.
        
        Args:
            df: DataFrame with financial data
            output_dir: Directory for saving plots
        """
        self.df = df.copy()
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Set style
        plt.style.use("seaborn-v0_8-whitegrid")
        self.font_params = {
            "family": "serif",
            "serif": ["Times New Roman"],
            "size": 12
        }
        plt.rcParams.update(self.font_params)
    
    def plot_dividend_payout(
        self,
        date_col: str = "fiscalDateEnding",
        value_col: str = "dividendPayout",
        save: bool = True
    ) -> plt.Figure:
        """
        Plot dividend payout over time.
        
        Args:
            date_col: Name of date column
            value_col: Name of value column
            save: Whether to save the plot
        
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(15, 5))
        
        # Convert dates
        dates = pd.to_datetime(self.df[date_col])
        values = self.df[value_col].astype(float)
        
        bars = ax.bar(
            dates,
            values,
            color="green",
            alpha=0.7,
            edgecolor="black",
            linewidth=1
        )
        
        # Add value labels
        for bar in bars:
            height = bar.get_height()
            if height != 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2.,
                    height + 0.1,
                    f"${height:,.0f}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    rotation=45
                )
        
        ax.set_title(
            "Dividend Payout - Netflix",
            fontsize=16,
            fontweight="bold",
            pad=20
        )
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("Value ($)", fontsize=12)
        ax.tick_params(axis="x", rotation=45)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax.xaxis.set_major_locator(mdates.YearLocator())
        
        ax.legend(["Dividend Payout"], loc="best", fontsize=12)
        ax.grid(True, linestyle="--", alpha=0.7, axis="y")
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / "dividend_payout.png"
            plt.savefig(filepath, dpi=300, bbox_inches="tight")
            print(f"Plot saved to {filepath}")
        
        return fig
    
    def plot_operating_cashflow_and_capex(
        self,
        date_col: str = "fiscalDateEnding",
        ocf_col: str = "operatingCashflow",
        capex_col: str = "capitalExpenditures",
        save: bool = True
    ) -> plt.Figure:
        """
        Plot operating cash flow and capital expenditures.
        
        Args:
            date_col: Name of date column
            ocf_col: Name of operating cash flow column
            capex_col: Name of capital expenditures column
            save: Whether to save the plot
        
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(15, 5))
        
        dates = pd.to_datetime(self.df[date_col])
        ocf = self.df[ocf_col].astype(float)
        capex = self.df[capex_col].astype(float)
        
        ax.plot(
            dates, ocf,
            marker="o",
            linestyle="-",
            linewidth=2,
            markersize=8,
            color="blue",
            label="Operating Cash Flow"
        )
        
        ax.plot(
            dates, capex,
            marker="s",
            linestyle="--",
            linewidth=2,
            markersize=8,
            color="red",
            label="Capital Expenditures"
        )
        
        ax.set_title(
            "Operating Cash Flow and Capital Expenditures - Netflix",
            fontsize=16,
            fontweight="bold",
            pad=20
        )
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("Value ($)", fontsize=12)
        ax.tick_params(axis="x", rotation=45)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax.xaxis.set_major_locator(mdates.YearLocator())
        
        ax.legend(loc="best", fontsize=12)
        ax.grid(True, linestyle="--", alpha=0.7)
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / "ocf_capex_comparison.png"
            plt.savefig(filepath, dpi=300, bbox_inches="tight")
            print(f"Plot saved to {filepath}")
        
        return fig
    
    def plot_free_cashflow(
        self,
        date_col: str = "fiscalDateEnding",
        fcf_col: str = "freeCashflow",
        save: bool = True
    ) -> plt.Figure:
        """
        Plot free cash flow over time.
        
        Args:
            date_col: Name of date column
            fcf_col: Name of free cash flow column
            save: Whether to save the plot
        
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(15, 7))
        
        dates = pd.to_datetime(self.df[date_col])
        fcf = self.df[fcf_col].astype(float)
        
        colors = ["purple" if v >= 0 else "orange" for v in fcf]
        
        bars = ax.bar(dates, fcf, color=colors, alpha=0.8, edgecolor="black")
        
        # Add value labels with formatting
        for i, (bar, v) in enumerate(zip(bars, fcf)):
            if abs(v) >= 1e9:
                label = f"${v/1e9:.1f}B"
            elif abs(v) >= 1e6:
                label = f"${v/1e6:.1f}M"
            else:
                label = f"${v:,.0f}"
            
            ax.text(
                i,
                v + (0.05 * max(abs(fcf))),
                label,
                ha="center",
                va="bottom" if v >= 0 else "top",
                fontsize=10,
                rotation=90
            )
        
        ax.set_title(
            "Free Cash Flow - Netflix",
            fontsize=16,
            fontweight="bold",
            pad=20
        )
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("Dollars ($)", fontsize=12)
        ax.tick_params(axis="x", rotation=45)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax.xaxis.set_major_locator(mdates.YearLocator())
        
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        
        # Add horizontal line at zero
        ax.axhline(y=0, color="black", linestyle="-", linewidth=1)
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / "free_cashflow.png"
            plt.savefig(filepath, dpi=300, bbox_inches="tight")
            print(f"Plot saved to {filepath}")
        
        return fig
    
    def plot_rolling_average(
        self,
        date_col: str = "fiscalDateEnding",
        value_col: str = "operatingCashflow",
        window: int = 2,
        save: bool = True
    ) -> plt.Figure:
        """
        Plot rolling average of specified column.
        
        Args:
            date_col: Name of date column
            value_col: Name of value column
            window: Rolling window size
            save: Whether to save the plot
        
        Returns:
            Matplotlib figure
        """
        fig, ax = plt.subplots(figsize=(15, 5))
        
        dates = pd.to_datetime(self.df[date_col])
        values = self.df[value_col].astype(float)
        rolling = values.rolling(window=window).mean()
        
        ax.plot(
            dates, values,
            marker="o",
            linestyle="-",
            linewidth=2,
            markersize=6,
            color="blue",
            alpha=0.6,
            label=f"{value_col}"
        )
        
        ax.plot(
            dates, rolling,
            marker="s",
            linestyle="--",
            linewidth=3,
            markersize=8,
            color="red",
            label=f"{window}-Year Rolling Average"
        )
        
        ax.set_title(
            f"{value_col} with {window}-Year Rolling Average - Netflix",
            fontsize=16,
            fontweight="bold",
            pad=20
        )
        ax.set_xlabel("Year", fontsize=12)
        ax.set_ylabel("Value ($)", fontsize=12)
        ax.tick_params(axis="x", rotation=45)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
        ax.xaxis.set_major_locator(mdates.YearLocator())
        
        ax.legend(loc="best", fontsize=12)
        ax.grid(True, linestyle="--", alpha=0.7)
        
        plt.tight_layout()
        
        if save:
            filepath = self.output_dir / f"rolling_avg_{window}y.png"
            plt.savefig(filepath, dpi=300, bbox_inches="tight")
            print(f"Plot saved to {filepath}")
        
        return fig
    
    def show_all_plots(self) -> None:
        """Generate and save all standard plots."""
        print("Generating visualizations...")
        
        if "dividendPayout" in self.df.columns:
            self.plot_dividend_payout()
        
        if "freeCashflow" in self.df.columns:
            self.plot_free_cashflow()
        elif "operatingCashflow" in self.df.columns and "capitalExpenditures" in self.df.columns:
            self.plot_operating_cashflow_and_capex()
        
        if "operatingCashflow" in self.df.columns:
            self.plot_rolling_average(window=2)
            self.plot_rolling_average(window=3)
        
        print("All visualizations generated successfully!")
