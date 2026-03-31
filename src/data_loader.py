"""
Data Loader Module
Handles loading expense data from various sources.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Union


class DataLoader:
    """Class to handle loading expense data from different sources."""

    def __init__(self, data_path: Optional[Union[str, Path]] = None):
        """
        Initialize DataLoader.

        Args:
            data_path: Path to the data file. If None, uses default path.
        """
        if data_path is None:
            self.data_path = Path(__file__).parent.parent / "data" / "expenses.csv"
        else:
            self.data_path = Path(data_path)

    def load_data(self, file_path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
        """
        Load expense data from CSV file.

        Args:
            file_path: Path to the CSV file. If None, uses default path.

        Returns:
            DataFrame containing expense data.

        Raises:
            FileNotFoundError: If the data file doesn't exist.
            ValueError: If the file format is invalid.
        """
        if file_path is not None:
            self.data_path = Path(file_path)

        if not self.data_path.exists():
            raise FileNotFoundError(f"Data file not found: {self.data_path}")

        try:
            df = pd.read_csv(self.data_path)
            return df
        except Exception as e:
            raise ValueError(f"Error loading data: {e}")

    def load_from_dict(self, data: dict) -> pd.DataFrame:
        """
        Load expense data from a dictionary.

        Args:
            data: Dictionary containing expense data.

        Returns:
            DataFrame containing expense data.
        """
        return pd.DataFrame(data)

    def save_data(self, df: pd.DataFrame, file_path: Optional[Union[str, Path]] = None) -> None:
        """
        Save expense data to CSV file.

        Args:
            df: DataFrame to save.
            file_path: Path to save the file. If None, uses default path.
        """
        if file_path is not None:
            save_path = Path(file_path)
        else:
            save_path = self.data_path

        save_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(save_path, index=False)


def load_data(file_path: Optional[Union[str, Path]] = None) -> pd.DataFrame:
    """
    Convenience function to load expense data.

    Args:
        file_path: Path to the CSV file.

    Returns:
        DataFrame containing expense data.
    """
    loader = DataLoader(file_path)
    return loader.load_data()
