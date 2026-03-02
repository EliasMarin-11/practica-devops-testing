from email.errors import InvalidDateDefect

import streamlit as st
from datetime import date

from core.domain_error import EmptyTitleError, InvalidAmountError
from core.expense_service import ExpenseService


@st.dialog("➕ Nuevo gasto")
def expense_form(service: ExpenseService):
    title = st.text_input("Título")
    amount = st.number_input("Importe (€)", min_value=0.0, step=0.5)
    expense_date = st.date_input(
        "Fecha",
        value=date.today(),
        max_value=date.today(),
    )
    if not isinstance(expense_date, date):
        expense_date = date.today()
    description = st.text_area("Descripción (opcional)")
    col1, col2 = st.columns(2)

    try:
        with col1:
            if st.button("Guardar"):
                service.create_expense(
                    title=title,
                    amount=amount,
                    description=description,
                    expense_date=expense_date,
                )
                st.session_state.show_new_expense = False
                st.rerun()
        with col2:
            if st.button("Cancelar"):
                st.session_state.show_new_expense = False
                st.rerun()
    except EmptyTitleError:
        st.error("El título no puede estar vacío")
    except InvalidAmountError:
        st.error("El gasto debe ser mayor a cero")
    except InvalidDateDefect:
        st.error("La fecha debe ser pasada no futura")
