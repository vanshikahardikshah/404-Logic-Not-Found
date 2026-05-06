import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "finance.db"

SAMPLE_TRANSACTIONS = [
    ("2026-04-01", 1200, "Job", "Part-time paycheck", "income"),
    ("2026-04-02", 45.99, "Groceries", "Safeway groceries", "expense"),
    ("2026-04-03", 15.50, "Transportation", "Gas", "expense"),
    ("2026-04-04", 12.99, "Entertainment", "Netflix", "expense"),
    ("2026-04-05", 80.00, "Dining", "Restaurant with friends", "expense"),
    ("2026-04-06", 500.00, "Rent", "Monthly rent payment", "expense"),
    ("2026-04-07", 35.00, "Shopping", "Clothes", "expense"),
    ("2026-04-08", 200.00, "Freelance", "Freelance project", "income"),
    ("2026-04-09", 25.75, "Groceries", "Trader Joe's", "expense"),
    ("2026-04-10", 18.00, "School", "Notebook and supplies", "expense"),
    ("2026-05-01", 1200, "Job", "Part-time paycheck", "income"),
    ("2026-05-02", 55.20, "Groceries", "Costco groceries", "expense"),
    ("2026-05-03", 22.00, "Transportation", "Uber ride", "expense"),
    ("2026-05-04", 16.99, "Entertainment", "Movie ticket", "expense"),
    ("2026-05-05", 95.00, "Dining", "Dinner", "expense"),
]


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_database():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            transaction_type TEXT NOT NULL CHECK(transaction_type IN ('income', 'expense'))
        )
        """
    )

    conn.commit()
    conn.close()


def add_transaction(date, amount, category, description, transaction_type):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO transactions (date, amount, category, description, transaction_type)
        VALUES (?, ?, ?, ?, ?)
        """,
        (date, amount, category, description, transaction_type),
    )

    conn.commit()
    conn.close()


def get_all_transactions():
    conn = get_db_connection()

    transactions = conn.execute(
        """
        SELECT * FROM transactions
        ORDER BY date DESC
        """
    ).fetchall()

    conn.close()
    return transactions


def search_transactions(category="", transaction_type="", month=""):
    query = "SELECT * FROM transactions WHERE 1=1"
    params = []

    if category:
        query += " AND category LIKE ?"
        params.append(f"%{category}%")

    if transaction_type:
        query += " AND transaction_type = ?"
        params.append(transaction_type)

    if month:
        query += " AND strftime('%Y-%m', date) = ?"
        params.append(month)

    query += " ORDER BY date DESC"

    conn = get_db_connection()
    transactions = conn.execute(query, params).fetchall()
    conn.close()

    return transactions


def delete_transaction(transaction_id):
    conn = get_db_connection()

    conn.execute(
        """
        DELETE FROM transactions
        WHERE id = ?
        """,
        (transaction_id,),
    )

    conn.commit()
    conn.close()


def add_sample_data():
    conn = get_db_connection()
    cursor = conn.cursor()

    inserted_count = 0
    duplicate_count = 0

    for transaction in SAMPLE_TRANSACTIONS:
        date, amount, category, description, transaction_type = transaction

        existing_rows = cursor.execute(
            """
            SELECT id FROM transactions
            WHERE date = ?
              AND amount = ?
              AND category = ?
              AND description = ?
              AND transaction_type = ?
            ORDER BY id
            """,
            transaction,
        ).fetchall()

        if not existing_rows:
            cursor.execute(
                """
                INSERT INTO transactions (date, amount, category, description, transaction_type)
                VALUES (?, ?, ?, ?, ?)
                """,
                (date, amount, category, description, transaction_type),
            )
            inserted_count += 1
            continue

        duplicate_ids = [(row["id"],) for row in existing_rows[1:]]
        if duplicate_ids:
            cursor.executemany(
                """
                DELETE FROM transactions
                WHERE id = ?
                """,
                duplicate_ids,
            )
            duplicate_count += len(duplicate_ids)

    conn.commit()
    conn.close()

    return inserted_count, duplicate_count
