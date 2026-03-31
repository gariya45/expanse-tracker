"""
Categorization Module
Handles expense categorization and category management.
"""

import pandas as pd
from typing import Dict, List, Optional
from collections import Counter


class ExpenseCategorizer:
    """Class to handle expense categorization."""

    # Default categories with descriptions
    DEFAULT_CATEGORIES = {
        "Food": "Groceries, restaurants, coffee, snacks",
        "Transport": "Bus, train, taxi, fuel, rideshare",
        "Entertainment": "Movies, concerts, games, streaming",
        "Shopping": "Clothing, electronics, books",
        "Utilities": "Electricity, water, internet, phone",
        "Health": "Medical, pharmacy, doctor visits",
        "Rent": "Housing, rent payments",
        "Education": "Tuition, courses, books",
        "Other": "Miscellaneous expenses",
    }

    # Keywords for automatic categorization
    CATEGORY_KEYWORDS = {
        "Food": [
            "grocery", "groceries", "restaurant", "lunch", "dinner",
            "breakfast", "coffee", "snack", "food", "meal", "eat",
            "cafe", "bakery", "pizza", "burger", "sushi"
        ],
        "Transport": [
            "bus", "train", "taxi", "uber", "lyft", "fuel", "gas",
            "transport", "transportation", "ride", "metro", "subway",
            "parking", "ticket"
        ],
        "Entertainment": [
            "movie", "concert", "game", "gaming", "streaming",
            "subscription", "netflix", "spotify", "entertainment",
            "theater", "cinema", "music", "show"
        ],
        "Shopping": [
            "clothing", "clothes", "fashion", "shoes", "electronics",
            "shopping", "store", "amazon", "book", "gift"
        ],
        "Utilities": [
            "electricity", "electric", "water", "internet", "phone",
            "mobile", "utility", "bill", "wifi", "gas bill"
        ],
        "Health": [
            "medical", "doctor", "pharmacy", "medicine", "health",
            "dental", "hospital", "clinic", "prescription", "vitamin"
        ],
        "Rent": [
            "rent", "housing", "apartment", "lease", "mortgage"
        ],
        "Education": [
            "education", "tuition", "course", "class", "school",
            "university", "college", "training", "workshop"
        ],
    }

    def __init__(self, custom_categories: Optional[Dict[str, str]] = None):
        """
        Initialize ExpenseCategorizer.

        Args:
            custom_categories: Custom categories to add/override defaults.
        """
        self.categories = self.DEFAULT_CATEGORIES.copy()
        if custom_categories:
            self.categories.update(custom_categories)

    def categorize_expense(self, description: str, amount: float = 0) -> str:
        """
        Automatically categorize an expense based on description.

        Args:
            description: Expense description.
            amount: Expense amount (can be used for additional logic).

        Returns:
            Predicted category.
        """
        if pd.isna(description):
            return "Other"

        description_lower = str(description).lower()

        # Check for keyword matches
        for category, keywords in self.CATEGORY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in description_lower:
                    return category

        return "Other"

    def categorize_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add predicted categories to a DataFrame.

        Args:
            df: DataFrame with expense data.

        Returns:
            DataFrame with added 'predicted_category' column.
        """
        df = df.copy()

        if "description" in df.columns:
            df["predicted_category"] = df["description"].apply(
                lambda x: self.categorize_expense(x)
            )
        else:
            df["predicted_category"] = "Other"

        return df

    def get_category_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Get summary statistics by category.

        Args:
            df: Preprocessed expense DataFrame.

        Returns:
            DataFrame with category summary.
        """
        summary = df.groupby("category").agg({
            "amount": ["sum", "mean", "count", "std"]
        }).round(2)

        summary.columns = ["Total", "Average", "Count", "Std Dev"]
        summary = summary.sort_values("Total", ascending=False)

        return summary

    def get_top_categories(self, df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
        """
        Get top spending categories.

        Args:
            df: Preprocessed expense DataFrame.
            n: Number of top categories to return.

        Returns:
            DataFrame with top categories.
        """
        category_totals = df.groupby("category")["amount"].sum().sort_values(ascending=False)
        return category_totals.head(n).to_frame(name="Total")

    def identify_unnecessary_spending(
        self,
        df: pd.DataFrame,
        threshold: float = 100.0,
        categories: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Identify potentially unnecessary expenses.

        Args:
            df: Preprocessed expense DataFrame.
            threshold: Amount threshold for flagging expenses.
            categories: Categories to check. If None, checks all.

        Returns:
            DataFrame with flagged expenses.
        """
        df = df.copy()

        if categories:
            df = df[df["category"].isin(categories)]

        # Flag expenses above threshold in discretionary categories
        discretionary_categories = ["Entertainment", "Shopping", "Food"]
        flagged = df[
            (df["category"].isin(discretionary_categories)) &
            (df["amount"] > threshold)
        ].copy()

        flagged["flag_reason"] = f"High amount (>${threshold}) in discretionary category"

        return flagged

    def get_category_distribution(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        Get percentage distribution of spending by category.

        Args:
            df: Preprocessed expense DataFrame.

        Returns:
            Dictionary with category percentages.
        """
        total = df["amount"].sum()
        category_totals = df.groupby("category")["amount"].sum()

        distribution = {
            category: (amount / total * 100).round(2)
            for category, amount in category_totals.items()
        }

        return dict(sorted(distribution.items(), key=lambda x: x[1], reverse=True))

    def add_custom_category(self, name: str, description: str, keywords: List[str]) -> None:
        """
        Add a custom category.

        Args:
            name: Category name.
            description: Category description.
            keywords: Keywords for auto-categorization.
        """
        self.categories[name] = description
        self.CATEGORY_KEYWORDS[name] = keywords


def categorize_expenses(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convenience function to categorize expenses.

    Args:
        df: Preprocessed expense DataFrame.

    Returns:
        DataFrame with category summary.
    """
    categorizer = ExpenseCategorizer()
    return categorizer.get_category_summary(df)
