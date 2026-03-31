# 💰 Personal Expense Tracker & Analyzer

A comprehensive Python-based system for tracking, analyzing, and visualizing personal expenses with Docker support for production-ready deployment.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Supported-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)

## 🎯 Features

- **Track Expenses**: Log daily and monthly expenses with categories
- **Auto-Categorization**: Automatically categorize expenses based on descriptions
- **Data Analysis**: 
  - Total monthly expenses
  - Category-wise spending breakdown
  - Daily/weekly/monthly trends
  - Savings calculation
  - Identify highest spending categories
  - Detect unnecessary spending patterns
- **Visual Reports**:
  - Pie chart (category distribution)
  - Bar chart (monthly expenses)
  - Line chart (trend over time)
  - Savings vs expenses graph
  - Heatmap of daily spending
- **Interactive Dashboard**: Streamlit-based UI for easy interaction
- **CLI Support**: Command-line interface for quick insights
- **Docker Ready**: Fully containerized for easy deployment

## 🧰 Tech Stack

- **Python 3.10+**
- **pandas** - Data manipulation
- **numpy** - Numerical computing
- **matplotlib** - Plotting
- **seaborn** - Statistical visualization
- **Streamlit** - Web UI framework
- **Docker** - Containerization

## 📁 Project Structure

```
expense-tracker/
│
├── data/
│   └── expenses.csv              # Sample expense data
│
├── src/
│   ├── data_loader.py            # Data loading utilities
│   ├── preprocessing.py          # Data cleaning & preprocessing
│   ├── analysis.py               # Expense analysis functions
│   ├── categorization.py         # Category management
│   └── visualization.py          # Plotting & charts
│
├── app/
│   └── streamlit_app.py          # Streamlit web application
│
├── notebooks/
│   └── EDA.ipynb                 # Exploratory Data Analysis
│
├── main.py                       # CLI entry point
├── requirements.txt              # Python dependencies
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
└── README.md                    # This file
```

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd expense-tracker
   ```

2. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

3. **Access the application**
   Open your browser and navigate to: `http://localhost:8501`

### Using Docker Commands

1. **Build the Docker image**
   ```bash
   docker build -t expense-tracker .
   ```

2. **Run the container**
   ```bash
   docker run -p 8501:8501 -v $(pwd)/data:/app/data expense-tracker
   ```

3. **Access the application**
   Open your browser at: `http://localhost:8501`

### Local Development

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Streamlit app**
   ```bash
   streamlit run app/streamlit_app.py
   ```

3. **Access the application**
   Open your browser at: `http://localhost:8501`

## 📊 Data Format

The expense data should be in CSV format with the following columns:

| Column      | Type    | Description                     |
|-------------|---------|---------------------------------|
| date        | string  | Date in YYYY-MM-DD format       |
| category    | string  | Expense category                |
| amount      | float   | Expense amount                  |
| description | string  | Description of the expense      |

### Sample Data

```csv
date,category,amount,description
2024-01-01,Food,45.50,Grocery shopping
2024-01-02,Transport,12.00,Bus ticket
2024-01-03,Food,25.00,Lunch at restaurant
```

## 🌐 Streamlit UI Features

### Dashboard
- Key metrics (total expenses, average daily/monthly spending)
- Category breakdown with pie chart
- Recent transactions

### Add Expense
- Form to add new expenses
- Date picker, category selector, amount input
- Description field

### Analytics
- **Trends**: Daily/weekly/monthly spending trends
- **Savings**: Calculate savings based on income
- **Insights**: Spending insights and patterns
- **Unnecessary**: Flag potentially wasteful expenses

### Data View
- Filter by date range
- Filter by category
- Filter by amount range
- Download data as CSV

## ⚡ CLI Usage

### Show All Insights
```bash
python main.py
```

### Show Summary Only
```bash
python main.py --summary
```

### Show Category Breakdown
```bash
python main.py --categories
```

### Show Monthly Trends
```bash
python main.py --trends
```

### Calculate Savings
```bash
python main.py --savings 5000
```

### Show Unnecessary Spending
```bash
python main.py --unnecessary 100
```

### Show Recent Transactions
```bash
python main.py --recent 20
```

### Use Custom Data File
```bash
python main.py --data custom_expenses.csv
```

### CLI Help
```bash
python main.py --help
```

## 📈 Example Outputs

### CLI Summary Output
```
============================================================
  EXPENSE TRACKER - SUMMARY INSIGHTS
============================================================

📊 Total Expenses:           $4,523.29
📅 Date Range:               2024-01-01 to 2024-03-31
📈 Average Daily Spending:   $49.16
📈 Average Monthly Spending: $1,507.76
🔢 Total Transactions:       92
💵 Avg per Transaction:      $49.16
```

### Category Breakdown
```
────────────────────────────────────────────────────────────
  TOP 5 SPENDING CATEGORIES
────────────────────────────────────────────────────────────

Category             Amount        
-----------------------------------
Food                 $1,234.50
Utilities             $915.00
Shopping              $814.99
Transport             $438.00
Entertainment         $425.00
```

## 🐳 Docker Commands Reference

### Build Image
```bash
docker build -t expense-tracker .
```

### Run Container
```bash
docker run -p 8501:8501 -v $(pwd)/data:/app/data expense-tracker
```

### Run with Docker Compose
```bash
docker-compose up --build
```

### Stop Container
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

### Execute Commands in Container
```bash
docker-compose exec expense-tracker python main.py --summary
```

## 📊 Supported Categories

- **Food**: Groceries, restaurants, coffee, snacks
- **Transport**: Bus, train, taxi, fuel, rideshare
- **Entertainment**: Movies, concerts, games, streaming
- **Shopping**: Clothing, electronics, books
- **Utilities**: Electricity, water, internet, phone
- **Health**: Medical, pharmacy, doctor visits
- **Rent**: Housing, rent payments
- **Education**: Tuition, courses, books
- **Other**: Miscellaneous expenses

## 🔧 Configuration

### Environment Variables

| Variable                    | Default  | Description                      |
|-----------------------------|----------|----------------------------------|
| STREAMLIT_SERVER_PORT       | 8501     | Streamlit server port           |
| STREAMLIT_SERVER_ADDRESS    | 0.0.0.0  | Streamlit server address        |

## 📝 Development

### Running Tests
```bash
# Add test framework and run tests
pytest tests/
```

### Code Style
The project follows PEP8 guidelines. Use `black` for formatting:
```bash
black src/ app/ main.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Data visualization with [Matplotlib](https://matplotlib.org/) and [Seaborn](https://seaborn.pydata.org/)
- Containerized with [Docker](https://www.docker.com/)

## 📧 Support

For issues, questions, or contributions, please open an issue on the repository.

---

**Happy Tracking! 💰📊**
