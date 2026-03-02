from core.expense_service import ExpenseService
from core.in_memory_expense_repository import InMemoryExpenseRepository

repository = InMemoryExpenseRepository()
expense_service = ExpenseService(repository)
