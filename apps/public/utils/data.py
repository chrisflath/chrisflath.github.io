import os
import numpy as np
import pandas as pd
from typing import Dict


class DataSimulator:
    """Simulates weekly demand data with realistic trend, pronounced seasonality,
    holiday effects, and heteroskedastic noise. Generates data from start_date to end_date.
    """

    def __init__(self, start_date: str, end_date: str, seed: int = 42):
        """
        Args:
            start_date (str): Simulation start date in ISO format (e.g., '2020-01-01').
            end_date (str): Simulation end date in ISO format (e.g., '2025-01-01').
            seed (int): Random seed for reproducibility.
        """
        self.start_date = pd.to_datetime(start_date)
        self.end_date = pd.to_datetime(end_date)
        self.periods = (
            (self.end_date - self.start_date).days // 7
        ) + 1  # weeks inclusive
        np.random.seed(seed)

    def simulate(self) -> pd.DataFrame:
        # 1. Create weekly date index
        dates = pd.date_range(start=self.start_date, periods=self.periods, freq="W")
        t = np.arange(self.periods)

        # 2. Realistic trend: logistic growth with saturation
        K = 150  # theoretical maximum demand in tens of units
        r = 0.003  # growth rate
        trend = K / (1 + np.exp(-r * (t - self.periods / 2))) - (K / 2)

        # 3. Seasonal component: sinusoidal pattern with peak in winter
        weeks_per_year = 52
        seasonal = 10 * np.sin(2 * np.pi * t / weeks_per_year + np.pi / 6)

        # 4. Holiday effects
        week_of_year = dates.isocalendar().week
        holiday_effect = np.where((week_of_year >= 51) | (week_of_year <= 1), 15, 0)
        summer_dip = np.where((week_of_year >= 28) & (week_of_year <= 32), -10, 0)

        # 5. Heteroskedastic noise
        base_level = 50 + trend + seasonal + holiday_effect + summer_dip
        noise_scale = 0.05 * np.maximum(base_level, 1)
        noise = np.random.normal(scale=noise_scale, size=self.periods)

        # 6. Combine components
        demand = base_level + noise
        demand = np.maximum(demand * 10, 0).round().astype(int)

        # 7. Assemble DataFrame
        df = pd.DataFrame({"date": dates, "demand": demand})
        df["unique_id"] = "Demand Amoxicillin Fürth"
        return df[["unique_id", "date", "demand"]]


class DataLoader:
    """Loads and prepares data for forecasting."""

    def __init__(
        self,
        file_path: str,
        start_date: str = "2020-01-01",
        end_date: str = "2025-08-01",
        seed: int = 42,
    ) -> None:
        """
        Args:
            file_path (str): Path to CSV file for data storage.
            start_date (str): Simulation start date in ISO format.
            end_date (str): Simulation end date in ISO format. Defaults to today if None.
            seed (int): Random seed for simulation reproducibility.
        """
        self.file_path = file_path
        self.start_date = start_date
        # If no end_date provided, use today
        self.end_date = end_date or pd.Timestamp.today().strftime("%demand-%m-%d")
        self.seed = seed

    def load(self) -> pd.DataFrame:
        """
        Load data from a CSV file; if file does not exist, simulate data and save.

        Returns
        -------
        pd.DataFrame
            A DataFrame with columns ['unique_id', 'date', 'demand'].
        """
        if os.path.exists(self.file_path):
            df = pd.read_csv(self.file_path)
            df["date"] = pd.to_datetime(df["date"])
            df["unique_id"] = "Demand Amoxicillin Fürth"
        else:
            # Simulate data
            simulator = DataSimulator(
                start_date=self.start_date, end_date=self.end_date, seed=self.seed
            )
            df = simulator.simulate()
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            # Save to CSV
            df.to_csv(self.file_path, index=False)
        return df[["unique_id", "date", "demand"]]


class DataSplitter:
    """Splits data into training and testing sets based on a given cutoff date."""

    def __init__(self, cutoff_date: str):
        self.cutoff_date = pd.to_datetime(cutoff_date)

    def split(self, df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
        """
        Split data into training and testing sets.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame with columns ['unique_id', 'date', 'demand'].

        Returns
        -------
        Dict[str, pd.DataFrame]
            A dictionary with keys 'train' and 'test'.
        """
        train = df[df["date"] < self.cutoff_date].copy()
        test = df[df["date"] >= self.cutoff_date].copy()
        return train, test
