# 💰 Personal Finance & Spending Analyzer

A modern, responsive web application to track your income and expenses with beautiful visualizations and insightful analytics.

## ✨ Features

- **📊 Dashboard** - View comprehensive financial summary with real-time data
- **➕ Add Transactions** - Easy-to-use form to record income and expenses
- **📋 Transaction List** - View all transactions with filtering options
- **🔍 Advanced Search** - Filter transactions by category, type, and date range
- **💳 Analytics** - Track your spending patterns and financial insights
- **📈 Chart Images** - Generate bar, line, and pie charts from stored transactions
- **📱 Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices
- **🎨 Modern UI** - Beautiful gradient design with intuitive navigation

## 🚀 Getting Started

### Prerequisites

- Python 3.7+
- Flask
- SQLite3
- matplotlib

### Installation

1. Navigate to the project directory:
```bash
cd personal-finance-analyzer
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and visit:
```
http://127.0.0.1:5000
```

## 📁 Project Structure

```
personal-finance-analyzer/
├── app.py                 # Main Flask application
├── database.py            # Database operations and functions
├── analysis.py            # Financial analysis functions
├── requirements.txt       # Python dependencies
├── finance.db             # SQLite database (auto-generated, not committed)
├── templates/             # HTML templates
│   ├── index.html         # Homepage
│   ├── add_transaction.html
│   ├── transactions.html
│   ├── search.html
│   └── dashboard.html
└── static/                # Generated chart images and static files
```

Note: `finance.db` and generated chart PNG files are created locally when the app runs. They are intentionally not committed to GitHub.

## 💻 How to Use

### 1. Adding a Transaction
1. Click "Add Transaction" button on the homepage
2. Fill in the following details:
   - **Date** - The date of the transaction
   - **Amount** - The transaction amount
   - **Category** - Category of expense/income (e.g., Groceries, Rent, Salary)
   - **Description** - Optional notes about the transaction
   - **Type** - Select either "Income" or "Expense"
3. Click "Add Transaction" to save

### 2. Viewing Transactions
1. Go to the "Transactions" page
2. View all your recorded transactions in a table format
3. Use filters to narrow down by:
   - Category
   - Transaction Type (Income/Expense)
   - Month

### 3. Searching Transactions
1. Visit the "Search" page
2. Use the search form to find specific transactions
3. Filter by category, type, or date range

### 4. Dashboard
1. View your financial overview with:
   - Total Income
   - Total Expenses
   - Net Balance
   - Transaction Count
2. See detailed analytics including:
   - Top spending categories
   - Monthly income, expenses, and net balance
   - Average transaction values
3. View generated PNG charts including spending by category, monthly trends, income vs expenses, expense distribution, net savings, and transaction counts

### 5. Loading Sample Data
- Click "Load Sample Data" on the homepage to populate the database with example transactions
- Great for testing the application functionality

## 🗄️ Database Structure

The application uses SQLite with the following transaction table:

```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    transaction_type TEXT NOT NULL CHECK(transaction_type IN ('income', 'expense'))
)
```

## 🎨 Design Features

- **Gradient Background**: Modern purple gradient theme
- **Responsive Layout**: Grid-based design that adapts to all screen sizes
- **Interactive Cards**: Hover effects and smooth transitions
- **Color Coding**: 
  - Green for Income
  - Red for Expenses
  - Blue for Balance
  - Orange for Transaction Count
- **Intuitive Navigation**: Sticky navbar with quick access to all features

## 📊 API Routes

- `GET /` - Homepage with financial summary
- `GET/POST /add` - Add new transaction
- `GET /transactions` - View all transactions with filters
- `GET /search` - Search transactions
- `GET /dashboard` - Financial dashboard and analytics
- `GET /sample-data` - Load sample data
- `POST /delete/<id>` - Delete a transaction

## 🔧 Technologies Used

- **Backend**: Flask (Python web framework)
- **Database**: SQLite3
- **Charts**: Matplotlib
- **Frontend**: HTML5, CSS3 (modern grid and flexbox)
- **Design**: Responsive design with gradient backgrounds

## 📋 Sample Data

The application includes pre-loaded sample data with:
- 15 sample transactions
- Diverse categories (Groceries, Rent, Job, Entertainment, etc.)
- Mix of income and expense entries
- Dates spanning April-May 2026

## ⚙️ Configuration

To modify the Flask configuration, edit `app.py`:

```python
app.secret_key = "personal_finance_secret_key"
app.run(debug=True)  # Set debug=False for production
```

To change the database location, modify `database.py`:

```python
DB_PATH = BASE_DIR / "finance.db"
```

## 🐛 Troubleshooting

### Port 5000 is already in use
```bash
# Kill the process using port 5000
pkill -f "python app.py"

# Or use a different port in app.py
app.run(debug=True, port=5001)
```

### Database not found
The database is created automatically when the app starts. If you have issues:
```bash
python -c "from database import create_database; create_database()"
```

### Templates not loading
Ensure the `templates/` folder exists and contains all HTML files in the correct location.

## 📝 Future Enhancements

- 🔐 User authentication and accounts
- 📧 Email reports and notifications
- 📱 Mobile app
- 🔄 Budget planning and tracking
- 🏆 Financial goals

## 📄 License

This project is open source and available for educational purposes.

## 👤 Author
Hetav Vyas,
Vanshika Hardik Shah

Personal Finance Analyzer - Created for easy financial tracking and analysis.

---

**Version**: 1.0  
**Last Updated**: May 5, 2026

Enjoy tracking your finances! 💰
