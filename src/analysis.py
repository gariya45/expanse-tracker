"""
Analysis Module
Handles expense analysis and insights generation.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class ExpenseAnalyzer:
    """Class to analyze expense data and generate insights."""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize ExpenseAnalyzer.

        Args:
            df: Preprocessed expense DataFrame.
        """
        self.df = df.copy()

    def get_total_expenses(self) -> float:
        """
        Calculate total expenses.

        Returns:
            Total amount spent.
        """
        return round(self.df["amount"].sum(), 2)

    def get_monthly_expenses(self) -> pd.DataFrame:
        """
        Calculate monthly expenses.

        Returns:
            DataFrame with monthly expense totals.
        """
        monthly = self.df.groupby(["year", "month", "month_name"])["amount"].sum().reset_index()
        monthly["period"] = monthly["month_name"] + " " + monthly["year"].astype(str)
        monthly = monthly[["period", "amount"]].sort_values("year").reset_index(drop=True)
        return monthly

    def get_daily_expenses(self) -> pd.DataFrame:
        """
        Calculate daily expenses.

        Returns:
            DataFrame with daily expense totals.
        """
        daily = self.df.groupby("date")["amount"].sum().reset_index()
        daily = daily.sort_values("date").reset_index(drop=True)
        return daily

    def get_weekly_expenses(self) -> pd.DataFrame:
        """
        Calculate weekly expenses.

        Returns:
            DataFrame with weekly expense totals.
        """
        weekly = self.df.groupby(["year", "week"])["amount"].sum().reset_index()
        weekly["period"] = "Week " + weekly["week"].astype(str) + " " + weekly["year"].astype(str)
        weekly = weekly[["period", "amount"]].sort_values(["year", "week"]).reset_index(drop=True)
        return weekly

    def get_category_breakdown(self) -> pd.DataFrame:
        """
        Get category-wise spending breakdown.

        Returns:
            DataFrame with category totals and percentages.
        """
        total = self.df["amount"].sum()
        category_df = self.df.groupby("category")["amount"].sum().reset_index()
        category_df["percentage"] = (category_df["amount"] / total * 100).round(2)
        category_df = category_df.sort_values("amount", ascending=False).reset_index(drop=True)
        return category_df

    def get_average_daily_spending(self) -> float:
        """
        Calculate average daily spending.

        Returns:
            Average amount spent per day.
        """
        date_range = (self.df["date"].max() - self.df["date"].min()).days + 1
        return round(self.get_total_expenses() / date_range, 2)

    def get_average_monthly_spending(self) -> float:
        """
        Calculate average monthly spending.

        Returns:
            Average amount spent per month.
        """
        months = self.df[["year", "month"]].drop_duplicates().shape[0]
        return round(self.get_total_expenses() / months, 2)

    def get_highest_spending_day(self) -> Tuple[pd.Timestamp, float]:
        """
        Find the day with highest spending.

        Returns:
            Tuple of (date, amount).
        """
        daily = self.get_daily_expenses()
        idx = daily["amount"].idxmax()
        return daily.loc[idx, "date"], daily.loc[idx, "amount"]

    def get_spending_trend(self, period: str = "daily") -> pd.DataFrame:
        """
        Get spending trend over time.

        Args:
            period: Time period for trend ('daily', 'weekly', 'monthly').

        Returns:
            DataFrame with spending trend.
        """
        if period == "daily":
            return self.get_daily_expenses()
        elif period == "weekly":
            return self.get_weekly_expenses()
        elif period == "monthly":
            return self.get_monthly_expenses()
        else:
            raise ValueError(f"Invalid period: {period}. Use 'daily', 'weekly', or 'monthly'.")

    def calculate_savings(
        self,
        income: float,
        period: str = "monthly"
    ) -> Dict[str, float]:
        """
        Calculate savings based on income and expenses.

        Args:
            income: Total income for the period.
            period: Period for calculation ('monthly' or 'total').

        Returns:
            Dictionary with savings information.
        """
        if period == "monthly":
            expenses = self.get_average_monthly_spending()
        else:
            expenses = self.get_total_expenses()

        savings = income - expenses
        savings_rate = (savings / income * 100) if income > 0 else 0

        return {
            "income": round(income, 2),
            "expenses": round(expenses, 2),
            "savings": round(savings, 2),
            "savings_rate": round(savings_rate, 2)
        }

    def get_insights(self) -> Dict[str, any]:
        """
        Generate comprehensive insights about spending.

        Returns:
            Dictionary with various insights.
        """
        total = self.get_total_expenses()
        category_breakdown = self.get_category_breakdown()
        top_category = category_breakdown.iloc[0]["category"]
        top_category_amount = category_breakdown.iloc[0]["amount"]
        top_category_pct = category_breakdown.iloc[0]["percentage"]

        highest_day, highest_amount = self.get_highest_spending_day()

        insights = {
            "total_expenses": total,
            "average_daily": self.get_average_daily_spending(),
            "average_monthly": self.get_average_monthly_spending(),
            "top_category": top_category,
            "top_category_amount": top_category_amount,
            "top_category_percentage": top_category_pct,
            "highest_spending_day": highest_day.strftime("%Y-%m-%d"),
            "highest_spending_amount": highest_amount,
            "total_transactions": len(self.df),
            "date_range": {
                "start": self.df["date"].min().strftime("%Y-%m-%d"),
                "end": self.df["date"].max().strftime("%Y-%m-%d")
            },
            "category_breakdown": category_breakdown.to_dict("records")
        }

        return insights

    def compare_periods(
        self,
        period1_start: datetime,
        period1_end: datetime,
        period2_start: datetime,
        period2_end: datetime
    ) -> Dict[str, any]:
        """
        Compare spending between two time periods.

        Args:
            period1_start: Start date of period 1.
            period1_end: End date of period 1.
            period2_start: Start date of period 2.
            period2_end: End date of period 2.

        Returns:
            Dictionary with comparison results.
        """
        period1_df = self.df[
            (self.df["date"] >= period1_start) &
            (self.df["date"] <= period1_end)
        ]

        period2_df = self.df[
            (self.df["date"] >= period2_start) &
            (self.df["date"] <= period2_end)
        ]

        period1_total = period1_df["amount"].sum()
        period2_total = period2_df["amount"].sum()

        change = period2_total - period1_total
        change_pct = (change / period1_total * 100) if period1_total > 0 else 0

        return {
            "period1": {
                "start": period1_start.strftime("%Y-%m-%d"),
                "end": period1_end.strftime("%Y-%m-%d"),
                "total": round(period1_total, 2)
            },
            "period2": {
                "start": period2_start.strftime("%Y-%m-%d"),
                "end": period2_end.strftime("%Y-%m-%d"),
                "total": round(period2_total, 2)
            },
            "change": round(change, 2),
            "change_percentage": round(change_pct, 2)
        }

    def detect_anomalies(self, threshold: float = 2.0) -> pd.DataFrame:
        """
        Detect spending anomalies using z-score.

        Args:
            threshold: Z-score threshold for anomaly detection.

        Returns:
            DataFrame with anomalous expenses.
        """
        df = self.df.copy()
        category_stats = df.groupby("category")["amount"].agg(["mean", "std"])

        anomalies = []

        for _, row in df.iterrows():
            category = row["category"]
            amount = row["amount"]

            if category in category_stats.index:
                mean = category_stats.loc[category, "mean"]
                std = category_stats.loc[category, "std"]

                if std > 0:
                    z_score = (amount - mean) / std
                    if abs(z_score) > threshold:
                        anomalies.append({
                            "date": row["date"],
                            "category": category,
                            "amount": amount,
                            "description": row.get("description", ""),
                            "z_score": round(z_score, 2)
                        })

        return pd.DataFrame(anomalies)


def analyze_expenses(df: pd.DataFrame) -> Dict[str, any]:
    """
    Convenience function to analyze expenses.

    Args:
        df: Preprocessed expense DataFrame.

    Returns:
        Dictionary with analysis insights.
    """
    analyzer = ExpenseAnalyzer(df)
    return analyzer.get_insights()
