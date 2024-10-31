#Traduzido tambem ao espanol
import textwrap
from abc import ABC, abstractmethod
from datetime import datetime


class Cliente:
    def __init__(self, direccion):
        self.direccion = direccion
        self.cuentas = []

    def realizar_transaccion(self, cuenta, transaccion):
        transaccion.registrar(cuenta)

    def agregar_cuenta(self, cuenta):
        self.cuentas.append(cuenta)


class PersonaFisica(Cliente):
    def __init__(self, nombre, fecha_nacimiento, dni, direccion):
        super().__init__(direccion)
        self.nombre = nombre
        self.fecha_nacimiento = fecha_nacimiento
        self.dni = dni


class Cuenta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historial = Historial()

    @classmethod
    def nueva_cuenta(cls, cliente, numero):
        return cls(numero, cliente)

    #Asi no cambia los valores
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historial(self):
        return self._historial

    def retirar(self, monto):
        saldo_actual = self.saldo
        excede_saldo = monto > saldo_actual

        if excede_saldo:
            print("\n@@@ Operación fallida: saldo insuficiente. @@@")

        elif monto > 0:
            self._saldo -= monto
            print("\n=== Retiro realizado exitosamente! ===")
            return True

        else:
            print("\n@@@ Operación fallida: monto no válido. @@@")

        return False

    def depositar(self, monto):
        if monto > 0:
            self._saldo += monto
            print("\n=== Depósito realizado exitosamente! ===")
        else:
            print("\n@@@ Operación fallida: monto no válido. @@@")
            return False

        return True


class CuentaCorriente(Cuenta):#Herencia
    def __init__(self, numero, cliente, limite=500, max_retiros=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._max_retiros = max_retiros

    def retirar(self, monto):
        num_retiros = len(
            [transaccion for transaccion in self.historial.transacciones if transaccion["tipo"] == Retiro.__name__]
        )

        excede_limite = monto > self._limite
        excede_retiros = num_retiros >= self._max_retiros

        if excede_limite:
            print("\n@@@ Operación fallida: monto excede el límite de retiro. @@@")

        elif excede_retiros:
            print("\n@@@ Operación fallida: cantidad máxima de retiros alcanzada. @@@")

        else:
            return super().retirar(monto)

        return False

    def __str__(self):
        return f"""\n
            Agencia:\t{self.agencia}
            Cuenta:\t\t{self.numero}
            Titular:\t{self.cliente.nombre}
        """


class Historial:
    def __init__(self):
        self._transacciones = []

    @property
    def transacciones(self):
        return self._transacciones

    def agregar_transaccion(self, transaccion):
        self._transacciones.append(
            {
                "tipo": transaccion.__class__.__name__,
                "monto": transaccion.valor,
                "fecha": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class Transaccion(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, cuenta):
        pass


class Retiro(Transaccion):
    def __init__(self, monto):
        self._monto = monto

    @property
    def valor(self):
        return self._monto

    def registrar(self, cuenta):
        exito_transaccion = cuenta.retirar(self.valor)

        if exito_transaccion:
            cuenta.historial.agregar_transaccion(self)


class Deposito(Transaccion):
    def __init__(self, monto):
        self._monto = monto

    @property
    def valor(self):
        return self._monto

    def registrar(self, cuenta):
        exito_transaccion = cuenta.depositar(self.valor)

        if exito_transaccion:
            cuenta.historial.agregar_transaccion(self)


def menu():
    opes_menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [r]\tRetirar
    [e]\tVer Extracto
    [nc]\tNueva cuenta
    [lc]\tListar cuentas
    [nu]\tNuevo usuario
    [q]\tSalir
    => """
    return input(textwrap.dedent(opes_menu))


def buscar_cliente(dni, clientes):
    cliente_encontrado = [cliente for cliente in clientes if cliente.dni == dni]
    return cliente_encontrado[0] if cliente_encontrado else None


def obtener_cuenta_cliente(cliente):
    if not cliente.cuentas:
        print("\n@@@ El cliente no posee cuentas! @@@")
        return None

    # Seleccionar cual cuenta, podria imprimir cada una
    print(f"\nTiene {len(cliente.cuentas)}")
    n = int(input("Cual desea seleccionar"))
    if n>len(cliente.cuentas) or n<0: print("Error seleccion invalida")

    return cliente.cuentas[n]


def realizar_deposito(clientes):
    dni = input("Ingrese el DNI del cliente: ")
    cliente = buscar_cliente(dni, clientes) #Ya retorna el cliente

    if not cliente:
        print("\n@@@ Cliente no encontrado! @@@")
        return

    monto = float(input("Ingrese el monto a depositar: "))
    transaccion = Deposito(monto)

    cuenta = obtener_cuenta_cliente(cliente)
    if not cuenta:
        return

    cliente.realizar_transaccion(cuenta, transaccion)


def realizar_retiro(clientes):
    dni = input("Ingrese el DNI del cliente: ")
    cliente = buscar_cliente(dni, clientes)

    if not cliente:
        print("\n@@@ Cliente no encontrado! @@@")
        return

    monto = float(input("Ingrese el monto a retirar: "))
    transaccion = Retiro(monto)

    cuenta = obtener_cuenta_cliente(cliente)
    if not cuenta:
        return

    cliente.realizar_transaccion(cuenta, transaccion)


def mostrar_extracto(clientes):
    dni = input("Ingrese el DNI del cliente: ")
    cliente = buscar_cliente(dni, clientes)

    if not cliente:
        print("\n@@@ Cliente no encontrado! @@@")
        return

    cuenta = obtener_cuenta_cliente(cliente)
    if not cuenta:
        return

    print("\n================ EXTRACTO ================")
    transacciones = cuenta.historial.transacciones

    extracto = "No hay transacciones registradas." if not transacciones else ""
    for transaccion in transacciones:
        extracto += f"\n{transaccion['tipo']}:\n\t$ {transaccion['monto']:.2f}"

    print(extracto)
    print(f"\nSaldo:\n\t$ {cuenta.saldo:.2f}")
    print("==========================================")


def registrar_cliente(clientes):
    dni = input("Ingrese el DNI (solo números): ")
    cliente = buscar_cliente(dni, clientes)

    if cliente:
        print("\n@@@ Ya existe un cliente con este DNI! @@@")
        return

    nombre = input("Ingrese el nombre completo: ")
    fecha_nacimiento = input("Ingrese la fecha de nacimiento (dd-mm-aaaa): ")
    direccion = input("Ingrese la dirección (calle, nro - barrio - ciudad/estado): ")

    cliente = PersonaFisica(nombre=nombre, fecha_nacimiento=fecha_nacimiento, dni=dni, direccion=direccion)

    clientes.append(cliente)

    print("\n=== Cliente registrado exitosamente! ===")


def crear_cuenta(numero_cuenta, clientes, cuentas):
    dni = input("Ingrese el DNI del cliente: ")
    cliente = buscar_cliente(dni, clientes)

    if not cliente:
        print("\n@@@ Cliente no encontrado, proceso de creación de cuenta cancelado! @@@")
        return

    cuenta = CuentaCorriente.nueva_cuenta(cliente=cliente, numero=numero_cuenta)
    cuentas.append(cuenta)
    cliente.cuentas.append(cuenta)

    print("\n=== Cuenta creada exitosamente! ===")


def listar_cuentas(cuentas):
    for cuenta in cuentas:
        print("=" * 100)
        print(textwrap.dedent(str(cuenta)))


def main():
    clientes = []
    cuentas = []

    while True:
        op = menu()

        if op == "d":
            realizar_deposito(clientes)

        elif op == "r":
            realizar_retiro(clientes)

        elif op == "e":
            mostrar_extracto(clientes)

        elif op == "nu":
            registrar_cliente(clientes)

        elif op == "nc":
            numero_cuenta = len(cuentas) + 1
            crear_cuenta(numero_cuenta, clientes, cuentas)

        elif op == "lc":
            listar_cuentas(cuentas)

        elif op == "q":
            break

        else:
            print("\n@@@ Opción inválida. Por favor, seleccione nuevamente. @@@")

main()
