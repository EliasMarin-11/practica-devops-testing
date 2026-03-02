from datetime import date
from collections import defaultdict
from core.expense import Expense
import abc


class ExpenseRepository(abc.ABC):
    @abc.abstractmethod
    def remove(self, expense_id: int) -> None: ...

    @abc.abstractmethod
    def save(self, expense: Expense) -> None: ...

    @abc.abstractmethod
    def get_by_id(self, expense_id: int) -> Expense | None: ...

    @abc.abstractmethod
    def list_all(self) -> list[Expense]: ...


class ExpenseService:
    def __init__(self, repository: ExpenseRepository):
        self._repository = repository
        self._next_id = 1

    def create_expense(
        self,
        title: str,
        amount: float,
        description: str = "",
        expense_date: date | None = None, # Añadido el tipo opcional para mejor claridad
    ) -> Expense:
        if expense_date is None:  # <-- ¡CAMBIADO! Antes era == None
            expense_date = date.today()
        expense = Expense(
            id=self._next_id,
            title=title,
            amount=amount,
            description=description,
            expense_date=expense_date,
        )
        self._repository.save(expense)
        self._next_id += 1
        return expense

    def remove_expense(self, expense_id: int) -> None:
        self._repository.remove(expense_id)

    def update_expense(
        self,
        expense_id: int,
        title: str | None = None,
        amount: float | None = None,
        description: str | None = None,
    ) -> None:
        expense = self._repository.get_by_id(expense_id)
        if not expense:
            return
        if title is not None:
            expense.title = title
        if amount is not None:
            expense.amount = amount
        if description is not None:
            expense.description = description
        self._repository.save(expense)

    def list_expenses(self) -> list[Expense]:
        return self._repository.list_all()

    def total_amount(self) -> float:
        """
        Devuelve la suma de los amounts de todos los Expenses.
        """
        # <-- ¡AÑADIDO! Sumamos el 'amount' de todos los gastos que nos devuelve el repositorio
        gastos = self._repository.list_all()
        return sum(gasto.amount for gasto in gastos)

    def total_by_month(self) -> dict[str, float]:
        totals = defaultdict(float)

        for expense in self._repository.list_all():
            key = expense.expense_date.strftime("%Y-%m")
            totals[key] += expense.amount

        return dict(totals)
