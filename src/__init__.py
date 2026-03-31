"""
Personal Expense Tracker & Analyzer - Source Package
"""

__version__ = "1.0.0"
__author__ = "Expense Tracker Team"

from .data_loader import DataLoader, load_data
from .preprocessing import DataPreprocessor, preprocess_data
from .categorization import ExpenseCategorizer, categorize_expenses
from .analysis import ExpenseAnalyzer, analyze_expenses
from .visualization import ExpenseVisualizer, plot_expense_distribution

__all__ = [
    "DataLoader",
    "load_data",
    "DataPreprocessor",
    "preprocess_data",
    "ExpenseCategorizer",
    "categorize_expenses",
    "ExpenseAnalyzer",
    "analyze_expenses",
    "ExpenseVisualizer",
    "plot_expense_distribution",
]
