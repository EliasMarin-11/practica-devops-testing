import pytest
from datetime import date, timedelta

from core.expense import Expense
from core.domain_error import (
    EmptyTitleError,
    InvalidAmountError,       # Añadido para el test de cantidad negativa
    InvalidExpenseDateError,  # Añadido para el test de fecha futura
)


def test_create_valid_expense():
    expense = Expense(
        id=1,
        title="Comida",
        amount=10.5,
        description="Almuerzo",
        expense_date=date.today(),
    )

    assert expense.title == "Comida"
    assert expense.amount == 10.5


def test_empty_title_raises_error():
    with pytest.raises(EmptyTitleError):
        Expense(id=1, title="", amount=10, description="", expense_date=date.today())


def test_negative_amount_raises_error():
    """
    Prueba que crear un objeto Expense con un valor negativo en el campo 'amount' (por ejemplo, -5)
    genera la excepción específica InvalidAmountError definida en domain_error.py.
    """
    # <-- ¡CÓDIGO AÑADIDO!
    # Comprobamos que al intentar crear un gasto de -5€ salta el InvalidAmountError
    with pytest.raises(InvalidAmountError):
        Expense(id=1, title="Cena", amount=-5, description="", expense_date=date.today())


def test_future_date_raises_error():
    """
    Prueba que al intentar crear un objeto Expense con un campo 'expense_date' posterior a la fecha actual
    (por ejemplo, usando date.today() + timedelta(days=1)), se lanza la excepción InvalidExpenseDateError
    definida en domain_error.py.
    """
    # <-- ¡CÓDIGO AÑADIDO!
    # Calculamos la fecha de mañana sumando 1 día a hoy
    fecha_futura = date.today() + timedelta(days=1)
    
    # Comprobamos que al crear un gasto con la fecha de mañana salta el InvalidExpenseDateError
    with pytest.raises(InvalidExpenseDateError):
        Expense(id=1, title="Cine", amount=15, description="", expense_date=fecha_futura)