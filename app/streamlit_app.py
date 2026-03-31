"""
Streamlit Application for Personal Expense Tracker & Analyzer
Interactive dashboard for tracking, analyzing, and visualizing expenses.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.data_loader import DataLoader
from src.preprocessing import DataPreprocessor
from src.categorization import ExpenseCategorizer
from src.analysis import ExpenseAnalyzer
from src.visualization import ExpenseVisualizer


# Page configuration
st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_expense_data():
    """Load and cache expense data."""
    try:
        loader = DataLoader()
        df = loader.load_data()
        preprocessor = DataPreprocessor()
        df = preprocessor.preprocess_data(df)
        df = preprocessor.add_time_features(df)
        return df
    except FileNotFoundError:
        return None


def add_new_expense(df):
    """Add a new expense entry."""
    st.subheader("Add New Expense")

    col1, col2, col3 = st.columns(3)

    with col1:
        expense_date = st.date_input("Date", value=date.today())
        category = st.selectbox(
            "Category",
            ["Food", "Transport", "Entertainment", "Shopping", "Utilities", "Health", "Rent", "Education", "Other"]
        )

    with col2:
        amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, value=10.0)

    with col3:
        description = st.text_input("Description", placeholder="e.g., Lunch at restaurant")

    if st.button("Add Expense", type="primary"):
        new_expense = pd.DataFrame({
            "date": [expense_date],
            "category": [category],
            "amount": [amount],
            "description": [description]
        })

        if df is not None:
            df = pd.concat([df, new_expense], ignore_index=True)
        else:
            df = new_expense

        # Re-preprocess
        preprocessor = DataPreprocessor()
        df = preprocessor.preprocess_data(df)
        df = preprocessor.add_time_features(df)

        st.success("Expense added successfully!")
        return df

    return df


def display_metrics(df):
    """Display key metrics."""
    analyzer = ExpenseAnalyzer(df)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Expenses",
            value=f"${analyzer.get_total_expenses():,.2f}",
            delta="All time"
        )

    with col2:
        st.metric(
            label="Avg. Daily Spending",
            value=f"${analyzer.get_average_daily_spending():,.2f}",
            delta="Per day"
        )

    with col3:
        st.metric(
            label="Avg. Monthly Spending",
            value=f"${analyzer.get_average_monthly_spending():,.2f}",
            delta="Per month"
        )

    with col4:
        st.metric(
            label="Total Transactions",
            value=f"{len(df):,}",
            delta="Count"
        )


def display_category_breakdown(df):
    """Display category-wise spending breakdown."""
    st.subheader("Category Breakdown")

    categorizer = ExpenseCategorizer()
    category_df = categorizer.get_category_summary(df)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(
            category_df,
            use_container_width=True,
            hide_index=True
        )

    with col2:
        # Create pie chart
        category_totals = df.groupby("category")["amount"].sum().sort_values(ascending=False)

        fig, ax = plt.subplots(figsize=(8, 8))
        colors = plt.cm.Set3(range(len(category_totals)))
        wedges, texts, autotexts = ax.pie(
            category_totals.values,
            labels=category_totals.index,
            autopct="%1.1f%%",
            colors=colors,
            startangle=90
        )
        ax.set_title("Expense Distribution by Category", fontweight="bold")
        st.pyplot(fig)


def display_trends(df):
    """Display spending trends."""
    st.subheader("Spending Trends")

    period = st.selectbox("Select Period", ["Daily", "Weekly", "Monthly"])

    visualizer = ExpenseVisualizer(df)

    if period == "Daily":
        fig = visualizer.plot_spending_trend("daily")
    elif period == "Weekly":
        fig = visualizer.plot_spending_trend("weekly")
    else:
        fig = visualizer.plot_spending_trend("monthly")

    st.pyplot(fig)


def display_savings_calculator(df):
    """Display savings calculator."""
    st.subheader("Savings Calculator")

    col1, col2 = st.columns([1, 2])

    with col1:
        income = st.number_input(
            "Monthly Income ($)",
            min_value=0.0,
            step=100.0,
            value=5000.0
        )

    with col2:
        if income > 0:
            analyzer = ExpenseAnalyzer(df)
            savings_info = analyzer.calculate_savings(income, "monthly")

            col_a, col_b, col_c = st.columns(3)

            with col_a:
                st.metric("Income", f"${savings_info['income']:,.2f}")

            with col_b:
                st.metric("Expenses", f"${savings_info['expenses']:,.2f}")

            with col_c:
                savings_color = "normal" if savings_info["savings"] >= 0 else "inverse"
                st.metric(
                    "Savings",
                    f"${savings_info['savings']:,.2f}",
                    f"{savings_info['savings_rate']:.1f}%"
                )

            # Savings vs Expenses chart
            visualizer = ExpenseVisualizer(df)
            fig = visualizer.plot_savings_vs_expenses(income, "monthly")
            st.pyplot(fig)


def display_insights(df):
    """Display spending insights."""
    st.subheader("Spending Insights")

    analyzer = ExpenseAnalyzer(df)
    insights = analyzer.get_insights()

    col1, col2 = st.columns(2)

    with col1:
        st.info(f"""
        **Top Spending Category:** {insights['top_category']}
        - Amount: ${insights['top_category_amount']:,.2f}
        - Percentage: {insights['top_category_percentage']:.1f}%
        """)

        st.info(f"""
        **Highest Spending Day:** {insights['highest_spending_day']}
        - Amount: ${insights['highest_spending_amount']:,.2f}
        """)

    with col2:
        st.info(f"""
        **Date Range:**
        - Start: {insights['date_range']['start']}
        - End: {insights['date_range']['end']}
        """)

        st.info(f"""
        **Transaction Summary:**
        - Total Transactions: {insights['total_transactions']:,}
        - Average per Transaction: ${insights['total_expenses'] / insights['total_transactions']:.2f}
        """)


def display_unnecessary_spending(df):
    """Display potentially unnecessary spending."""
    st.subheader("Potentially Unnecessary Spending")

    categorizer = ExpenseCategorizer()
    threshold = st.slider("Amount Threshold ($)", min_value=50, max_value=500, value=100, step=10)

    flagged = categorizer.identify_unnecessary_spending(df, threshold)

    if len(flagged) > 0:
        st.warning(f"Found {len(flagged)} expenses that may be unnecessary:")
        st.dataframe(
            flagged[["date", "category", "amount", "description", "flag_reason"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("No unnecessary spending detected based on current threshold!")


def display_filtered_data(df):
    """Display filtered expense data."""
    st.subheader("Expense Data")

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        min_date = df["date"].min().date()
        max_date = df["date"].max().date()
        date_range = st.date_input(
            "Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

    with col2:
        categories = df["category"].unique().tolist()
        selected_categories = st.multiselect(
            "Categories",
            categories,
            default=categories
        )

    with col3:
        min_amount = st.number_input("Min Amount ($)", min_value=0.0, value=0.0)
        max_amount = st.number_input("Max Amount ($)", min_value=0.0, value=df["amount"].max())

    # Apply filters
    filtered_df = df.copy()

    if len(date_range) == 2:
        filtered_df = filtered_df[
            (filtered_df["date"].dt.date >= date_range[0]) &
            (filtered_df["date"].dt.date <= date_range[1])
        ]

    if selected_categories:
        filtered_df = filtered_df[filtered_df["category"].isin(selected_categories)]

    filtered_df = filtered_df[
        (filtered_df["amount"] >= min_amount) &
        (filtered_df["amount"] <= max_amount)
    ]

    st.write(f"Showing {len(filtered_df)} of {len(df)} transactions")
    st.dataframe(
        filtered_df[["date", "category", "amount", "description"]],
        use_container_width=True,
        hide_index=True
    )


def main():
    """Main application function."""
    # Load data
    df = load_expense_data()

    # Header
    st.markdown('<h1 class="main-header">💰 Personal Expense Tracker</h1>', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Dashboard", "Add Expense", "Analytics", "Data View", "Settings"]
    )

    # File upload in sidebar
    st.sidebar.subheader("Upload Data")
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        preprocessor = DataPreprocessor()
        df = preprocessor.preprocess_data(df)
        df = preprocessor.add_time_features(df)
        st.sidebar.success("Data uploaded successfully!")

    # Check if data exists
    if df is None:
        st.error("No expense data found. Please upload a CSV file or add expenses manually.")
        return

    # Page routing
    if page == "Dashboard":
        st.header("📊 Dashboard")

        # Metrics
        display_metrics(df)

        st.divider()

        # Category breakdown
        display_category_breakdown(df)

        st.divider()

        # Recent transactions
        st.subheader("Recent Transactions")
        recent_df = df.sort_values("date", ascending=False).head(10)
        st.dataframe(
            recent_df[["date", "category", "amount", "description"]],
            use_container_width=True,
            hide_index=True
        )

    elif page == "Add Expense":
        st.header("➕ Add New Expense")
        df = add_new_expense(df)

    elif page == "Analytics":
        st.header("📈 Analytics")

        tab1, tab2, tab3, tab4 = st.tabs(["Trends", "Savings", "Insights", "Unnecessary"])

        with tab1:
            display_trends(df)

        with tab2:
            display_savings_calculator(df)

        with tab3:
            display_insights(df)

        with tab4:
            display_unnecessary_spending(df)

    elif page == "Data View":
        st.header("📋 Expense Data")
        display_filtered_data(df)

    elif page == "Settings":
        st.header("⚙️ Settings")

        st.subheader("Data Management")
        if st.button("Download Data as CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download expenses.csv",
                data=csv,
                file_name="expenses.csv",
                mime="text/csv"
            )

        st.subheader("About")
        st.info("""
        **Personal Expense Tracker & Analyzer**

        A comprehensive tool for tracking, analyzing, and visualizing personal expenses.

        Features:
        - Track daily/monthly expenses
        - Categorize spending automatically
        - Analyze spending patterns
        - Identify unnecessary expenses
        - Generate visual reports
        - Calculate savings

        Built with Python, Streamlit, and Docker.
        """)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    main()
