import streamlit as st

from apps.streamlit.components.expense_form import expense_form
from apps.streamlit.components.expense_list import expense_list
from apps.streamlit.config import expense_service


@st.dialog("❌ Error")
def error_popup():
    st.error(st.session_state.domain_error)
    if st.button("Cerrar"):
        st.session_state.domain_error = None
        st.rerun()


def run_app():
    st.title("💸 Student Expense Tracker")
    tab1, tab2 = st.tabs(["Gastos", "Estadísticas"])

    with tab2:
        # 📊 Métrica
        st.metric(
            "Total gastado", f"{expense_service.total_amount():.2f} €", border=True
        )

        monthly = expense_service.total_by_month()
        if monthly:
            st.subheader("Gastos por mes")
            st.bar_chart(monthly)
        else:
            st.info("Aun no existen datos de gastos")

    with tab1:
        st.subheader("Gastos")
        if st.button("➕ Añadir gasto"):
            st.session_state.show_new_expense = True

        if st.session_state.get("show_new_expense", False):
            expense_form(expense_service)

        if st.session_state.get("domain_error"):
            error_popup()

        expense_list(expense_service)


if __name__ == "__main__":
    run_app()
