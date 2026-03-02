import streamlit as st

from apps.streamlit.components.expense_card import expense_card
from core.expense_service import ExpenseService


def expense_list(service: ExpenseService):
    expenses = service.list_expenses()

    if not expenses:
        st.info("No hay gastos registrados")
        return

    for expense in expenses:
        expense_card(expense, service)
