import streamlit as st
from core.expense import Expense
from core.expense_service import ExpenseService


def expense_card(expense: Expense, service: ExpenseService):
    with st.container(border=True):
        col1, col2, col3 = st.columns([5, 2, 1])
        with col1:
            st.write(f"**{expense.title}**")
            st.caption(expense.expense_date.strftime("%d/%m/%Y, %H:%M:%S"))
            if expense.description:
                st.caption(expense.description)

        with col2:
            st.write(f"{expense.amount:.2f} €")

        with col3:
            if st.button("🗑️", key=f"delete-{expense.id}"):
                service.remove_expense(expense.id)
                st.rerun()
