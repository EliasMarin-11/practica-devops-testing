import sqlite3
from datetime import date

from core.expense import Expense
from core.expense_service import ExpenseRepository

"""
¡NO TOCAR! ES UN EJEMPLO.
"""


class SQLiteExpenseRepository(ExpenseRepository):
    def __init__(self, db_path: str = "expenses.db"):
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._create_table()

    def _create_table(self) -> None:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                expense_date TEXT NOT NULL
            )
            """
        )
        self._conn.commit()

    def save(self, expense: Expense) -> None:
        cursor = self._conn.cursor()
        cursor.execute(
            """
            INSERT INTO expenses (id, title, amount, description, expense_date)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                title = excluded.title,
                amount = excluded.amount,
                description = excluded.description,
                expense_date = excluded.expense_date
            """,
            (
                expense.id,
                expense.title,
                expense.amount,
                expense.description,
                expense.expense_date.isoformat(),
            ),
        )
        self._conn.commit()

    def remove(self, expense_id: int) -> None:
        cursor = self._conn.cursor()
        cursor.execute(
            "DELETE FROM expenses WHERE id = ?",
            (expense_id,),
        )
        self._conn.commit()

    def get_by_id(self, expense_id: int) -> Expense | None:
        cursor = self._conn.cursor()
        cursor.execute(
            "SELECT * FROM expenses WHERE id = ?",
            (expense_id,),
        )
        row = cursor.fetchone()

        if row is None:
            return None

        return Expense(
            id=row["id"],
            title=row["title"],
            amount=row["amount"],
            description=row["description"],
            expense_date=date.fromisoformat(row["expense_date"]),
        )

    def list_all(self) -> list[Expense]:
        cursor = self._conn.cursor()
        cursor.execute("SELECT * FROM expenses")

        expenses = []
        for row in cursor.fetchall():
            expenses.append(
                Expense(
                    id=row["id"],
                    title=row["title"],
                    amount=row["amount"],
                    description=row["description"],
                    expense_date=date.fromisoformat(row["expense_date"]),
                )
            )

        return expenses

    def empty(self) -> None:
        cursor = self._conn.cursor()
        cursor.execute("DELETE FROM expenses")
        self._conn.commit()
