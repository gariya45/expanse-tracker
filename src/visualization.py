"""
Visualization Module
Handles expense data visualization using matplotlib and seaborn.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Optional, List, Dict
import numpy as np


# Set style
sns.set_style("whitegrid")
plt.rcParams["figure.figsize"] = (12, 6)


class ExpenseVisualizer:
    """Class to visualize expense data."""

    def __init__(self, df: pd.DataFrame):
        """
        Initialize ExpenseVisualizer.

        Args:
            df: Preprocessed expense DataFrame.
        """
        self.df = df.copy()

    def plot_expense_distribution(self, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a pie chart of expense distribution by category.

        Args:
            save_path: Path to save the figure.

        Returns:
            Matplotlib Figure object.
        """
        category_totals = self.df.groupby("category")["amount"].sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(10, 8))

        colors = sns.color_palette("husl", len(category_totals))
        wedges, texts, autotexts = ax.pie(
            category_totals.values,
            labels=category_totals.index,
            autopct="%1.1f%%",
            colors=colors,
            startangle=90,
            textprops={"fontsize": 10}
        )

        # Enhance text
        for autotext in autotexts:
            autotext.set_color("white")
            autotext.set_fontweight("bold")

        ax.set_title("Expense Distribution by Category", fontsize=14, fontweight="bold", pad=20)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")

        return fig

    def plot_monthly_expenses(self, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a bar chart of monthly expenses.

        Args:
            save_path: Path to save the figure.

        Returns:
            Matplotlib Figure object.
        """
        monthly = self.df.groupby(["year", "month", "month_name"])["amount"].sum().reset_index()
        monthly["period"] = monthly["month_name"] + " " + monthly["year"].astype(str)
        monthly = monthly.sort_values(["year", "month"])

        fig, ax = plt.subplots(figsize=(12, 6))

        bars = ax.bar(monthly["period"], monthly["amount"], color=sns.color_palette("viridis", len(monthly)))

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.,
                height,
                f"${height:.0f}",
                ha="center",
                va="bottom",
                fontsize=9
            )

        ax.set_xlabel("Month", fontsize=12)
        ax.set_ylabel("Amount ($)", fontsize=12)
        ax.set_title("Monthly Expenses", fontsize=14, fontweight="bold")
        ax.tick_params(axis="x", rotation=45)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")

        return fig

    def plot_spending_trend(self, period: str = "daily", save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a line chart of spending trend over time.

        Args:
            period: Time period ('daily', 'weekly', 'monthly').
            save_path: Path to save the figure.

        Returns:
            Matplotlib Figure object.
        """
        if period == "daily":
            trend = self.df.groupby("date")["amount"].sum().reset_index()
            x_label = "Date"
        elif period == "weekly":
            trend = self.df.groupby(["year", "week"])["amount"].sum().reset_index()
            trend["period"] = "Week " + trend["week"].astype(str) + " " + trend["year"].astype(str)
            trend = trend[["period", "amount"]]
            x_label = "Week"
        elif period == "monthly":
            trend = self.df.groupby(["year", "month", "month_name"])["amount"].sum().reset_index()
            trend["period"] = trend["month_name"] + " " + trend["year"].astype(str)
            trend = trend[["period", "amount"]]
            x_label = "Month"
        else:
            raise ValueError(f"Invalid period: {period}")

        fig, ax = plt.subplots(figsize=(12, 6))

        ax.plot(
            range(len(trend)),
            trend["amount"],
            marker="o",
            linewidth=2,
            markersize=6,
            color=sns.color_palette("deep")[0]
        )

        ax.fill_between(
            range(len(trend)),
            trend["amount"],
            alpha=0.3,
            color=sns.color_palette("deep")[0]
        )

        ax.set_xlabel(x_label, fontsize=12)
        ax.set_ylabel("Amount ($)", fontsize=12)
        ax.set_title(f"Spending Trend ({period.capitalize()})", fontsize=14, fontweight="bold")

        if period != "daily":
            ax.set_xticks(range(len(trend)))
            ax.set_xticklabels(trend["period"], rotation=45, ha="right")

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")

        return fig

    def plot_category_comparison(self, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a horizontal bar chart comparing categories.

        Args:
            save_path: Path to save the figure.

        Returns:
            Matplotlib Figure object.
        """
        category_totals = self.df.groupby("category")["amount"].sum().sort_values(ascending=True)

        fig, ax = plt.subplots(figsize=(10, 8))

        bars = ax.barh(
            category_totals.index,
            category_totals.values,
            color=sns.color_palette("rocket", len(category_totals))
        )

        # Add value labels
        for i, (bar, value) in enumerate(zip(bars, category_totals.values)):
            ax.text(
                value + max(category_totals.values) * 0.01,
                i,
                f"${value:.0f}",
                va="center",
                fontsize=10
            )

        ax.set_xlabel("Amount ($)", fontsize=12)
        ax.set_ylabel("Category", fontsize=12)
        ax.set_title("Spending by Category", fontsize=14, fontweight="bold")

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")

        return fig

    def plot_savings_vs_expenses(
        self,
        income: float,
        period: str = "monthly",
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """
        Create a bar chart comparing savings and expenses.

        Args:
            income: Total income for the period.
            period: Period for calculation ('monthly' or 'total').
            save_path: Path to save the figure.

        Returns:
            Matplotlib Figure object.
        """
        if period == "monthly":
            expenses = self.df.groupby(["year", "month"])["amount"].sum().mean()
        else:
            expenses = self.df["amount"].sum()

        savings = income - expenses

        fig, ax = plt.subplots(figsize=(8, 6))

        categories = ["Income", "Expenses", "Savings"]
        values = [income, expenses, savings]
        colors = ["#2ecc71", "#e74c3c", "#3498db"]

        bars = ax.bar(categories, values, color=colors, alpha=0.8)

        # Add value labels
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.,
                height,
                f"${value:.0f}",
                ha="center",
                va="bottom",
                fontsize=12,
                fontweight="bold"
            )

        ax.set_ylabel("Amount ($)", fontsize=12)
        ax.set_title(f"Income vs Expenses vs Savings ({period.capitalize()})", fontsize=14, fontweight="bold")

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")

        return fig

    def plot_daily_spending_heatmap(self, save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a heatmap of daily spending by day of week and week number.

        Args:
            save_path: Path to save the figure.

        Returns:
            Matplotlib Figure object.
        """
        df = self.df.copy()
        df["day_of_week"] = df["date"].dt.day_name()
        df["week"] = df["date"].dt.isocalendar().week

        # Create pivot table
        pivot = df.pivot_table(
            values="amount",
            index="day_of_week",
            columns="week",
            aggfunc="sum",
            fill_value=0
        )

        # Reorder days
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        pivot = pivot.reindex(day_order)

        fig, ax = plt.subplots(figsize=(14, 6))

        sns.heatmap(
            pivot,
            annot=True,
            fmt=".0f",
            cmap="YlOrRd",
            cbar_kws={"label": "Amount ($)"},
            linewidths=0.5,
            ax=ax
        )

        ax.set_title("Daily Spending Heatmap", fontsize=14, fontweight="bold")
        ax.set_xlabel("Week Number", fontsize=12)
        ax.set_ylabel("Day of Week", fontsize=12)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")

        return fig

    def generate_dashboard(self, save_path: Optional[str] = None) -> plt.Figure:
        """
        Generate a comprehensive dashboard with multiple plots.

        Args:
            save_path: Path to save the figure.

        Returns:
            Matplotlib Figure object.
        """
        fig = plt.figure(figsize=(16, 12))

        # Create subplots
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

        # 1. Expense distribution pie chart
        ax1 = fig.add_subplot(gs[0, 0])
        category_totals = self.df.groupby("category")["amount"].sum().sort_values(ascending=False)
        colors = sns.color_palette("husl", len(category_totals))
        ax1.pie(
            category_totals.values,
            labels=category_totals.index,
            autopct="%1.1f%%",
            colors=colors,
            startangle=90,
            textprops={"fontsize": 9}
        )
        ax1.set_title("Expense Distribution", fontweight="bold")

        # 2. Monthly expenses bar chart
        ax2 = fig.add_subplot(gs[0, 1])
        monthly = self.df.groupby(["year", "month", "month_name"])["amount"].sum().reset_index()
        monthly["period"] = monthly["month_name"] + " " + monthly["year"].astype(str)
        monthly = monthly.sort_values(["year", "month"])
        ax2.bar(monthly["period"], monthly["amount"], color=sns.color_palette("viridis", len(monthly)))
        ax2.set_title("Monthly Expenses", fontweight="bold")
        ax2.tick_params(axis="x", rotation=45)

        # 3. Spending trend line chart
        ax3 = fig.add_subplot(gs[1, 0])
        daily = self.df.groupby("date")["amount"].sum().reset_index()
        ax3.plot(daily["date"], daily["amount"], marker="o", linewidth=1.5, markersize=4)
        ax3.fill_between(daily["date"], daily["amount"], alpha=0.3)
        ax3.set_title("Spending Trend", fontweight="bold")
        ax3.tick_params(axis="x", rotation=45)

        # 4. Category comparison
        ax4 = fig.add_subplot(gs[1, 1])
        category_totals_sorted = self.df.groupby("category")["amount"].sum().sort_values(ascending=True)
        ax4.barh(
            category_totals_sorted.index,
            category_totals_sorted.values,
            color=sns.color_palette("rocket", len(category_totals_sorted))
        )
        ax4.set_title("Spending by Category", fontweight="bold")

        fig.suptitle("Expense Analysis Dashboard", fontsize=16, fontweight="bold", y=0.995)

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches="tight")

        return fig


def plot_expense_distribution(df: pd.DataFrame, save_path: Optional[str] = None) -> plt.Figure:
    """
    Convenience function to plot expense distribution.

    Args:
        df: Preprocessed expense DataFrame.
        save_path: Path to save the figure.

    Returns:
        Matplotlib Figure object.
    """
    visualizer = ExpenseVisualizer(df)
    return visualizer.plot_expense_distribution(save_path)
