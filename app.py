from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

from database import (
    create_database,
    add_transaction as insert_transaction,
    get_all_transactions,
    search_transactions,
    delete_transaction as remove_transaction,
    add_sample_data as insert_sample_data,
)

from analysis import calculate_summary, generate_charts, generate_chart_images


app = Flask(__name__)
app.secret_key = "personal_finance_secret_key"


# -----------------------------
# Helper Function
# -----------------------------
def is_valid_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# -----------------------------
# Routes
# -----------------------------
@app.route("/")
def index():
    summary = calculate_summary()
    return render_template("index.html", summary=summary)


@app.route("/add", methods=["GET", "POST"])
def add_transaction():
    if request.method == "POST":
        date = request.form.get("date")
        amount = request.form.get("amount")
        category = request.form.get("category")
        description = request.form.get("description")
        transaction_type = request.form.get("transaction_type")

        # Check required fields
        if not date or not amount or not category or not transaction_type:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("add_transaction"))

        # Validate date
        if not is_valid_date(date):
            flash("Date must be in YYYY-MM-DD format.", "error")
            return redirect(url_for("add_transaction"))

        # Validate amount
        try:
            amount = float(amount)

            if amount <= 0:
                flash("Amount must be greater than 0.", "error")
                return redirect(url_for("add_transaction"))

        except ValueError:
            flash("Amount must be a valid number.", "error")
            return redirect(url_for("add_transaction"))

        # Validate transaction type
        if transaction_type not in ["income", "expense"]:
            flash("Transaction type must be income or expense.", "error")
            return redirect(url_for("add_transaction"))

        # Save transaction to SQLite database
        insert_transaction(
            date=date,
            amount=amount,
            category=category,
            description=description,
            transaction_type=transaction_type,
        )

        flash("Transaction added successfully!", "success")
        return redirect(url_for("transactions"))

    return render_template("add_transaction.html")


@app.route("/transactions")
def transactions():
    transaction_data = get_all_transactions()

    return render_template(
        "transactions.html",
        transactions=transaction_data,
        category="",
        transaction_type="",
        month="",
    )


@app.route("/search")
def search():
    category = request.args.get("category", "")
    transaction_type = request.args.get("transaction_type", "")
    month = request.args.get("month", "")

    transaction_data = search_transactions(
        category=category,
        transaction_type=transaction_type,
        month=month,
    )

    return render_template(
        "search.html",
        transactions=transaction_data,
        category=category,
        transaction_type=transaction_type,
        month=month,
    )


@app.route("/delete/<int:transaction_id>", methods=["POST"])
def delete_transaction(transaction_id):
    remove_transaction(transaction_id)

    flash("Transaction deleted successfully.", "success")
    return redirect(url_for("transactions"))


@app.route("/dashboard")
def dashboard():
    # Generate chart PNG images
    generate_chart_images()
    
    summary = calculate_summary()
    charts = generate_charts()
    chart_images = [
        {
            "title": "Spending by Category",
            "filename": "charts/category_spending.png",
            "alt": "Bar chart showing spending by category",
        },
        {
            "title": "Monthly Spending Trend",
            "filename": "charts/monthly_spending.png",
            "alt": "Line chart showing monthly spending trend",
        },
        {
            "title": "Income vs Expenses",
            "filename": "charts/income_vs_expenses.png",
            "alt": "Bar chart comparing income and expenses",
        },
        {
            "title": "Expense Distribution",
            "filename": "charts/expense_pie_chart.png",
            "alt": "Pie chart showing expense distribution by category",
        },
        {
            "title": "Monthly Net Savings",
            "filename": "charts/monthly_net_savings.png",
            "alt": "Line chart showing monthly net savings",
        },
        {
            "title": "Transactions by Category",
            "filename": "charts/transaction_count_by_category.png",
            "alt": "Bar chart showing transaction count by category",
        },
    ]

    return render_template(
        "dashboard.html",
        summary=summary,
        charts=charts,
        chart_images=chart_images,
    )


@app.route("/sample-data")
def sample_data():
    inserted_count, duplicate_count = insert_sample_data()

    if inserted_count:
        flash(f"{inserted_count} sample transactions added successfully!", "success")
    elif duplicate_count:
        flash(
            f"Sample data was already loaded. Removed {duplicate_count} duplicate sample transactions.",
            "success",
        )
    else:
        flash("Sample data is already loaded. No new transactions were added.", "success")

    return redirect(url_for("transactions"))


# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    create_database()
    app.run(debug=True)
