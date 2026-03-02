from datetime import date

from core.expense import Expense
from core.expense_service import ExpenseService
from core.no_tocar.sqlite_expense_repository import SQLiteExpenseRepository

# Vamos a ver algunos ejemplos de la aplicación.

# Primero tenemos que crear nuestro repositorio la clase encargada de la responsabilidad de la base de datos
repository = SQLiteExpenseRepository()

# A continuación el servicio
expense_service = ExpenseService(repository)

# Ahora podemos crear expenses (gastos)
expense = Expense(
    id=1, title="Nuevo gasto", amount=4, description="", expense_date=date.today()
)

# Si queremos podemos guardar en nuestro repositorio nuestra expense
repository.save(expense)

# Ahora dentro de nuestro repositorio tendremos una expense
assert len(repository.list_all()) == 1

# También podemos eliminar gastos
repository.remove(1)

assert len(repository.list_all()) == 0

# Finalmente si queremos modificar nuestro gasto podemos simplemente modificar el objeto

expense.title = "Otro título"

# y guardar nuestro gasto
repository.save(expense)

assert repository.list_all()[0].title == "Otro título"


"""
Sin embargo, el repositorio no contiene lógica de negocio, respetando el principio de responsabilidad única
ya que solo se encarga de la responsabilidad del almacenamiento, leer, guardar, actualizar ... Y nuestra app, aunque
parezca tener un enfoque CRUD, en un futuro puede añadir bastante lógica. 

Ejemplo: Si en un futuro queremos que cuando se añada un gasto automáticamente se envíe una notificación push al móvil del usuario
eso iría en el servicio, no en el repositorio.

Otro ejemplo: Si en un futuro se quisiera limitar el gasto mensual a un determinado presupuesto establecido por el usuario, esa lógica
de comprobación iría en el servicio, no en el repositorio.

A través de nuestro servicio podemos realizar nuestros casos de uso:

Crear un gasto:
"""

expense_service.create_expense(title="Nuevo", amount=3)

"""
Indirectamente nuestro servicio ha utilizado el repositorio, inyectado mediante inyeccion de dependencias al servicio
y ha creado dentro de este un nuevo gasto, sin embargo, también incluye determinada lógica de negocio, por ejemplo
en caso de no conocerse la fecha esta se establece como hoy.
"""

"""
Nuestro servicio nos permite también listar nuestros gastos, de esa forma podemos listarlos sin necesidad de llamar al repositorio.
"""
gastos = expense_service.list_expenses()
assert len(gastos) == 1

"""
Finalmente nuestro servicio  nos permite realizar ciertos cálculos estadísticos como calcular el total gastado o calcular un histórico de gastos
por mes.
"""

total_gastado = expense_service.total_amount()
assert total_gastado == 3

gastos_mensuales = expense_service.total_by_month()
assert gastos_mensuales[date.today().strftime("%Y-%m")] == 3

"""
Si nos fijamos nuestra arquitectura tiene forma de cebolla si 
trazamos un diagrama con flechas, donde cada flecha indica el acoplamiento (que fichero importa que otro fichero), se vería
algo tal que así:

<- Tener un import de donde apunta.

Dominio        Servicios            Implementaciones

expense <- expense_service <- in_memory_expense_repository
        <----------------------|
        
es tan sencillo como preguntarse 

¿Expense conoce ExpenseService? No
¿Expense conoce InMemoryExpenseRepository? No

¿ExpenseService conoce Expense? Si
¿ExpenseService conoce InMemoryExpenseRepository? No


¿InMemoryExpenseRepository conoce Expense? Si
¿InMemoryExpenseRepository conoce ExpenseService? Si

¿Alguno de estos conoce la interfaz web? No.

¿Esto que significa? 
1. Cambios en el servicio o en el repositorio no van a afectar al dominio, ese código no va a fallar.
2. Cambios en el repositorio no van a afectar al servicio, es decir, si derrepente queremos crear un MysqlExpenseRepository
e implementarlo utilizando consultas SQL no hay que tocar ni una sola linea del servicio.

Pero también pasa al contario
1. Cabmios en el dominio provocarán hacer cambios en el servicio y el repositorio
2. Cambios en el servicio provocarán cambios en el respositorio.

"""


"""
¿Vuestro objetivo?
"""
