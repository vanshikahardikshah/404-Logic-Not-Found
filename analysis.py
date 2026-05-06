from database import get_all_transactions
from collections import defaultdict
from datetime import datetime
import os

os.environ.setdefault(
    "MPLCONFIGDIR",
    os.path.join(os.path.dirname(__file__), "static", ".matplotlib"),
)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


def calculate_summary():
    """Calculate income, expenses, and net balance summary"""
    transactions = get_all_transactions()
    
    summary = {
        'total_income': 0,
        'total_expenses': 0,
        'net_balance': 0,
        'net_savings': 0,
        'transaction_count': len(transactions),
        'highest_expense_category': 'N/A',
        'by_category': defaultdict(lambda: {'income': 0, 'expense': 0})
    }
    
    for transaction in transactions:
        amount = transaction['amount']
        category = transaction['category']
        trans_type = transaction['transaction_type']
        
        if trans_type == 'income':
            summary['total_income'] += amount
            summary['by_category'][category]['income'] += amount
        else:
            summary['total_expenses'] += amount
            summary['by_category'][category]['expense'] += amount
    
    summary['net_balance'] = summary['total_income'] - summary['total_expenses']
    summary['net_savings'] = summary['net_balance']
    
    # Find highest expense category
    highest_expense = 0
    highest_category = 'N/A'
    for category, values in summary['by_category'].items():
        if values['expense'] > highest_expense:
            highest_expense = values['expense']
            highest_category = category
    summary['highest_expense_category'] = highest_category
    
    return summary


def generate_charts():
    """Generate chart data for visualization"""
    transactions = get_all_transactions()
    
    # Category breakdown
    category_data = defaultdict(lambda: {'income': 0, 'expense': 0})
    
    # Monthly breakdown
    monthly_data = defaultdict(lambda: {'income': 0, 'expense': 0})
    total_expenses = 0
    
    for transaction in transactions:
        amount = transaction['amount']
        category = transaction['category']
        trans_type = transaction['transaction_type']
        date = transaction['date']
        
        # Parse date (YYYY-MM-DD format)
        month = date[:7]  # YYYY-MM
        
        if trans_type == 'income':
            category_data[category]['income'] += amount
            monthly_data[month]['income'] += amount
        else:
            category_data[category]['expense'] += amount
            monthly_data[month]['expense'] += amount
            total_expenses += amount

    top_expense_categories = []
    for category, values in category_data.items():
        expense_amount = values['expense']
        if expense_amount > 0:
            top_expense_categories.append({
                'category': category,
                'amount': expense_amount,
                'percent': (expense_amount / total_expenses * 100) if total_expenses else 0,
            })

    top_expense_categories = sorted(
        top_expense_categories,
        key=lambda category: category['amount'],
        reverse=True,
    )[:5]

    monthly_summary = []
    for month, values in sorted(monthly_data.items()):
        monthly_summary.append({
            'month': month,
            'income': values['income'],
            'expense': values['expense'],
            'net': values['income'] - values['expense'],
        })
    
    return {
        'category_data': dict(category_data),
        'monthly_data': dict(sorted(monthly_data.items())),
        'top_expense_categories': top_expense_categories,
        'monthly_summary': monthly_summary,
    }


def generate_chart_images():
    """Generate PNG chart images and save to static/charts/"""
    transactions = get_all_transactions()
    
    # Ensure charts directory exists
    charts_dir = os.path.join(os.path.dirname(__file__), 'static', 'charts')
    os.makedirs(charts_dir, exist_ok=True)
    
    # Prepare data structures
    category_expenses = defaultdict(float)
    category_counts = defaultdict(int)
    monthly_income = defaultdict(float)
    monthly_expenses = defaultdict(float)
    total_income = 0
    total_expenses = 0
    
    for transaction in transactions:
        amount = transaction['amount']
        category = transaction['category']
        trans_type = transaction['transaction_type']
        date = transaction['date']
        month = date[:7]  # YYYY-MM format
        category_counts[category] += 1
        
        if trans_type == 'income':
            total_income += amount
            monthly_income[month] += amount
        else:
            total_expenses += amount
            category_expenses[category] += amount
            monthly_expenses[month] += amount
    
    # 1. Category Spending Bar Chart
    if category_expenses:
        plt.figure(figsize=(10, 6))
        categories = list(category_expenses.keys())
        amounts = list(category_expenses.values())
        plt.bar(categories, amounts, color='#e74c3c')
        plt.xlabel('Category')
        plt.ylabel('Amount ($)')
        plt.title('Total Expenses by Category')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(charts_dir, 'category_spending.png'), dpi=100)
        plt.close()
    
    # 2. Monthly Spending Line Chart
    if monthly_expenses:
        plt.figure(figsize=(10, 6))
        months = sorted(monthly_expenses.keys())
        amounts = [monthly_expenses[m] for m in months]
        plt.plot(months, amounts, marker='o', linewidth=2, color='#3498db')
        plt.xlabel('Month')
        plt.ylabel('Total Expenses ($)')
        plt.title('Monthly Expenses Trend')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(charts_dir, 'monthly_spending.png'), dpi=100)
        plt.close()
    
    # 3. Income vs Expenses Bar Chart
    plt.figure(figsize=(8, 6))
    plt.bar(['Income', 'Expenses'], [total_income, total_expenses], color=['#2ecc71', '#e74c3c'])
    plt.xlabel('Type')
    plt.ylabel('Amount ($)')
    plt.title('Income vs Expenses')
    for i, v in enumerate([total_income, total_expenses]):
        plt.text(i, v + max(total_income, total_expenses) * 0.02, f'${v:,.2f}', ha='center')
    plt.tight_layout()
    plt.savefig(os.path.join(charts_dir, 'income_vs_expenses.png'), dpi=100)
    plt.close()
    
    # 4. Expense Pie Chart
    if category_expenses:
        plt.figure(figsize=(10, 8))
        categories = list(category_expenses.keys())
        amounts = list(category_expenses.values())
        colors = plt.cm.Set3(range(len(categories)))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', colors=colors, startangle=90)
        plt.title('Expense Distribution by Category')
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(os.path.join(charts_dir, 'expense_pie_chart.png'), dpi=100)
        plt.close()

    # 5. Monthly Net Savings Line Chart
    months = sorted(set(monthly_income.keys()) | set(monthly_expenses.keys()))
    if months:
        plt.figure(figsize=(10, 6))
        savings = [monthly_income[m] - monthly_expenses[m] for m in months]
        plt.plot(months, savings, marker='o', linewidth=2, color='#8e44ad')
        plt.axhline(0, color='#555555', linewidth=1, linestyle='--')
        plt.xlabel('Month')
        plt.ylabel('Net Savings ($)')
        plt.title('Monthly Net Savings')
        plt.xticks(rotation=45, ha='right')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(os.path.join(charts_dir, 'monthly_net_savings.png'), dpi=100)
        plt.close()

    # 6. Transaction Count by Category Bar Chart
    if category_counts:
        plt.figure(figsize=(10, 6))
        categories = list(category_counts.keys())
        counts = list(category_counts.values())
        plt.bar(categories, counts, color='#f39c12')
        plt.xlabel('Category')
        plt.ylabel('Number of Transactions')
        plt.title('Transactions by Category')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(os.path.join(charts_dir, 'transaction_count_by_category.png'), dpi=100)
        plt.close()
    
    return True
