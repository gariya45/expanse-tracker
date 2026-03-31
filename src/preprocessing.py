"""
Preprocessing Module
Handles data cleaning and preprocessing for expense data.
"""

import pandas as pd
import numpy as np
from typing import Optional, List
from datetime import datetime


class DataPreprocessor:
    """Class to handle preprocessing of expense data."""

    # Standard category names
    STANDARD_CATEGORIES = {
        "food": "Food",
        "grocery": "Food",
        "groceries": "Food",
        "restaurant": "Food",
        "lunch": "Food",
        "dinner": "Food",
        "breakfast": "Food",
        "coffee": "Food",
        "snacks": "Food",
        "transport": "Transport",
        "transportation": "Transport",
        "bus": "Transport",
        "train": "Transport",
        "taxi": "Transport",
        "uber": "Transport",
        "lyft": "Transport",
        "fuel": "Transport",
        "gas": "Transport",
        "entertainment": "Entertainment",
        "movie": "Entertainment",
        "movies": "Entertainment",
        "concert": "Entertainment",
        "games": "Entertainment",
        "gaming": "Entertainment",
        "streaming": "Entertainment",
        "subscription": "Entertainment",
        "shopping": "Shopping",
        "clothing": "Shopping",
        "clothes": "Shopping",
        "electronics": "Shopping",
        "books": "Shopping",
        "utilities": "Utilities",
        "electricity": "Utilities",
        "water": "Utilities",
        "internet": "Utilities",
        "phone": "Utilities",
        "mobile": "Utilities",
        "health": "Health",
        "medical": "Health",
        "doctor": "Health",
        "pharmacy": "Health",
        "medicine": "Health",
        "dental": "Health",
        "rent": "Rent",
        "housing": "Rent",
        "education": "Education",
        "tuition": "Education",
        "course": "Education",
        "other": "Other",
        "misc": "Other",
    }

    def __init__(self):
        """Initialize DataPreprocessor."""
        pass

    def preprocess_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Preprocess expense data.

        Args:
            df: Raw expense DataFrame.

        Returns:
            Cleaned and preprocessed DataFrame.
        """
        df = df.copy()

        # Standardize column names
        df.columns = df.columns.str.lower().str.strip()

        # Ensure required columns exist
        required_columns = ["date", "category", "amount"]
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")

        # Convert date to datetime
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

        # Remove rows with invalid dates
        df = df.dropna(subset=["date"])

        # Clean amount column
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df = df.dropna(subset=["amount"])

        # Remove negative amounts (unless they represent refunds)
        df = df[df["amount"] > 0]

        # Normalize category names
        df["category"] = df["category"].apply(self._normalize_category)

        # Clean description
        if "description" in df.columns:
            df["description"] = df["description"].str.strip()
            df["description"] = df["description"].fillna("")

        # Sort by date
        df = df.sort_values("date").reset_index(drop=True)

        return df

    def _normalize_category(self, category: str) -> str:
        """
        Normalize category name to standard format.

        Args:
            category: Raw category name.

        Returns:
            Normalized category name.
        """
        if pd.isna(category):
            return "Other"

        category_lower = str(category).lower().strip()

        # Check for exact match first
        if category_lower in self.STANDARD_CATEGORIES:
            return self.STANDARD_CATEGORIES[category_lower]

        # Check for partial match
        for key, value in self.STANDARD_CATEGORIES.items():
            if key in category_lower:
                return value

        # Capitalize first letter if no match found
        return category.title()

    def add_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add time-based features to the DataFrame.

        Args:
            df: Preprocessed DataFrame.

        Returns:
            DataFrame with additional time features.
        """
        df = df.copy()

        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month
        df["month_name"] = df["date"].dt.month_name()
        df["day"] = df["date"].dt.day
        df["day_of_week"] = df["date"].dt.dayofweek
        df["day_name"] = df["date"].dt.day_name()
        df["week"] = df["date"].dt.isocalendar().week
        df["quarter"] = df["date"].dt.quarter

        return df

    def filter_by_date_range(
        self,
        df: pd.DataFrame,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> pd.DataFrame:
        """
        Filter DataFrame by date range.

        Args:
            df: Preprocessed DataFrame.
            start_date: Start date for filtering.
            end_date: End date for filtering.

        Returns:
            Filtered DataFrame.
        """
        df = df.copy()

        if start_date is not None:
            df = df[df["date"] >= start_date]

        if end_date is not None:
            df = df[df["date"] <= end_date]

        return df

    def filter_by_category(self, df: pd.DataFrame, categories: List[str]) -> pd.DataFrame:
        """
        Filter DataFrame by categories.

        Args:
            df: Preprocessed DataFrame.
            categories: List of categories to filter by.

        Returns:
            Filtered DataFrame.
        """
        df = df.copy()
        return df[df["category"].isin(categories)]


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convenience function to preprocess expense data.

    Args:
        df: Raw expense DataFrame.

    Returns:
        Cleaned and preprocessed DataFrame.
    """
    preprocessor = DataPreprocessor()
    return preprocessor.preprocess_data(df)
