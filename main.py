"""
CLI Entry Point for Personal Expense Tracker & Analyzer
Command-line interface for expense tracking and analysis.
"""

import argparse
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.data_loader import DataLoader
from src.preprocessing import DataPreprocessor
from src.categorization import ExpenseCategorizer
from src.analysis import ExpenseAnalyzer
from src.visualization import ExpenseVisualizer


def print_header(title: str) -> None:
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}\n")


def load_and_preprocess_data(file_path: str = None):
    """Load and preprocess expense data."""
    loader = DataLoader(file_path)
    df = loader.load_data()

    preprocessor = DataPreprocessor()
    df = preprocessor.preprocess_data(df)
    df = preprocessor.add_time_features(df)

    return df


def display_summary(df):
    """Display summary insights."""
    print_header("EXPENSE TRACKER - SUMMARY INSIGHTS")

    analyzer = ExpenseAnalyzer(df)
    insights = analyzer.get_insights()

    print(f"📊 Total Expenses:           ${insights['total_expenses']:,.2f}")
    print(f"📅 Date Range:               {insights['date_range']['start']} to {insights['date_range']['end']}")
    print(f"📈 Average Daily Spending:   ${insights['average_daily']:,.2f}")
    print(f"📈 Average Monthly Spending: ${insights['average_monthly']:,.2f}")
    print(f"🔢 Total Transactions:       {insights['total_transactions']:,}")
    print(f"💵 Avg per Transaction:      ${insights['total_expenses'] / insights['total_transactions']:.2f}")


def display_top_categories(df, n: int = 5):
    """Display top spending categories."""
    print_section(f"TOP {n} SPENDING CATEGORIES")

    categorizer = ExpenseCategorizer()
    top_categories = categorizer.get_top_categories(df, n)

    print(f"{'Category':<20} {'Amount':>15}")
    print("-" * 35)
    for category, amount in top_categories.itertuples():
        print(f"{category:<20} ${amount:>13,.2f}")


def display_category_breakdown(df):
    """Display detailed category breakdown."""
    print_section("CATEGORY BREAKDOWN")

    categorizer = ExpenseCategorizer()
    category_df = categorizer.get_category_summary(df)

    print(f"{'Category':<20} {'Total':>12} {'Avg':>12} {'Count':>8} {'%':>8}")
    print("-" * 62)
    for idx, row in category_df.iterrows():
        total = row["Total"]
        avg = row["Average"]
        count = int(row["Count"])
        pct = (total / df["amount"].sum() * 100)
        print(f"{idx:<20} ${total:>10,.2f} ${avg:>10,.2f} {count:>8} {pct:>6.1f}%")


def display_monthly_trends(df):
    """Display monthly expense trends."""
    print_section("MONTHLY EXPENSE TRENDS")

    analyzer = ExpenseAnalyzer(df)
    monthly = analyzer.get_monthly_expenses()

    print(f"{'Month':<20} {'Amount':>15}")
    print("-" * 35)
    for _, row in monthly.iterrows():
        print(f"{row['period']:<20} ${row['amount']:>13,.2f}")


def display_savings_info(df, income: float = None):
    """Display savings information."""
    print_section("SAVINGS CALCULATION")

    if income is None:
        income = float(input("Enter your monthly income ($): "))

    analyzer = ExpenseAnalyzer(df)
    savings_info = analyzer.calculate_savings(income, "monthly")

    print(f"💰 Monthly Income:    ${savings_info['income']:>12,.2f}")
    print(f"💸 Monthly Expenses:  ${savings_info['expenses']:>12,.2f}")
    print(f"💵 Monthly Savings:   ${savings_info['savings']:>12,.2f}")
    print(f"📊 Savings Rate:      {savings_info['savings_rate']:>12.1f}%")

    if savings_info["savings"] < 0:
        print("\n⚠️  Warning: You are spending more than you earn!")
    elif savings_info["savings_rate"] < 20:
        print("\n💡 Tip: Consider aiming for at least 20% savings rate.")
    else:
        print("\n✅ Great job! You're maintaining a healthy savings rate.")


def display_unnecessary_spending(df, threshold: float = 100.0):
    """Display potentially unnecessary spending."""
    print_section(f"POTENTIALLY UNNECESSARY SPENDING (>${threshold:.0f})")

    categorizer = ExpenseCategorizer()
    flagged = categorizer.identify_unnecessary_spending(df, threshold)

    if len(flagged) > 0:
        print(f"Found {len(flagged)} expenses that may be unnecessary:\n")
        print(f"{'Date':<12} {'Category':<15} {'Amount':>10} {'Description':<30}")
        print("-" * 67)
        for _, row in flagged.iterrows():
            date_str = row["date"].strftime("%Y-%m-%d")
            print(f"{date_str:<12} {row['category']:<15} ${row['amount']:>8,.2f} {row['description'][:27]:<30}")

        total_flagged = flagged["amount"].sum()
        print(f"\n💸 Total Potentially Wasted: ${total_flagged:,.2f}")
    else:
        print("✅ No unnecessary spending detected based on current threshold!")


def display_recent_transactions(df, n: int = 10):
    """Display recent transactions."""
    print_section(f"RECENT {n} TRANSACTIONS")

    recent_df = df.sort_values("date", ascending=False).head(n)

    print(f"{'Date':<12} {'Category':<15} {'Amount':>10} {'Description':<30}")
    print("-" * 67)
    for _, row in recent_df.iterrows():
        date_str = row["date"].strftime("%Y-%m-%d")
        print(f"{date_str:<12} {row['category']:<15} ${row['amount']:>8,.2f} {row['description'][:27]:<30}")


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Personal Expense Tracker & Analyzer - CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                    # Show all insights
  python main.py --summary          # Show summary only
  python main.py --categories       # Show category breakdown
  python main.py --trends           # Show monthly trends
  python main.py --savings 5000     # Calculate savings with $5000 income
  python main.py --unnecessary 150  # Show expenses over $150
  python main.py --recent 20        # Show last 20 transactions
  python main.py --data custom.csv  # Use custom data file
        """
    )

    parser.add_argument(
        "--data",
        type=str,
        help="Path to custom expense CSV file"
    )

    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show summary insights only"
    )

    parser.add_argument(
        "--categories",
        action="store_true",
        help="Show category breakdown only"
    )

    parser.add_argument(
        "--trends",
        action="store_true",
        help="Show monthly trends only"
    )

    parser.add_argument(
        "--savings",
        type=float,
        metavar="INCOME",
        help="Calculate savings with given monthly income"
    )

    parser.add_argument(
        "--unnecessary",
        type=float,
        metavar="THRESHOLD",
        help="Show expenses above threshold in discretionary categories"
    )

    parser.add_argument(
        "--recent",
        type=int,
        metavar="N",
        default=10,
        help="Show N recent transactions (default: 10)"
    )

    parser.add_argument(
        "--top",
        type=int,
        metavar="N",
        default=5,
        help="Show top N spending categories (default: 5)"
    )

    args = parser.parse_args()

    # Load and preprocess data
    try:
        df = load_and_preprocess_data(args.data)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("\nPlease ensure the data file exists or provide a custom path using --data")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

    # Display requested information
    if args.summary or not any([
        args.categories, args.trends, args.savings,
        args.unnecessary, args.recent
    ]):
        display_summary(df)

    if args.categories or not any([
        args.summary, args.trends, args.savings,
        args.unnecessary, args.recent
    ]):
        display_top_categories(df, args.top)
        display_category_breakdown(df)

    if args.trends or not any([
        args.summary, args.categories, args.savings,
        args.unnecessary, args.recent
    ]):
        display_monthly_trends(df)

    if args.savings:
        display_savings_info(df, args.savings)

    if args.unnecessary:
        display_unnecessary_spending(df, args.unnecessary)

    if args.recent:
        display_recent_transactions(df, args.recent)

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
