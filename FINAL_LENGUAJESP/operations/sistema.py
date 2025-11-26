"""
Módulo de lógica de negocio para el Sistema de Gestión Bancaria.
Contiene las funciones para manipular cuentas, transacciones y operaciones bancarias.
"""

from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from models.banco import Cuenta, Transaccion


class SistemaBancario:
    """Clase para gestionar el sistema bancario completo."""

    def __init__(self):
        """Inicializa el sistema bancario con listas vacías."""
        self.cuentas = {}  # Usar diccionario para acceso rápido por numero_cuenta
        self.transacciones = []
        self.siguiente_numero_cuenta = 1000001
        self.siguiente_id_transaccion = 1

    def crear_cuenta(self, titular, tipo_cuenta, saldo_inicial=0.0):
        """
        Crea una nueva cuenta bancaria.
        """
        if not titular.strip():
            raise ValueError("El nombre del titular no puede estar vacío")

        if saldo_inicial < 0:
            raise ValueError("El saldo inicial no puede ser negativo")

        nueva_cuenta = Cuenta(
            self.siguiente_numero_cuenta,
            titular.strip(),
            tipo_cuenta,
            saldo_inicial
        )

        self.cuentas[nueva_cuenta.numero_cuenta] = nueva_cuenta
        self.siguiente_numero_cuenta += 1

        # Registrar transacción de apertura si hay saldo inicial
        if saldo_inicial > 0:
            self._registrar_transaccion(
                nueva_cuenta.numero_cuenta,
                "Depósito Inicial",
                saldo_inicial,
                nueva_cuenta.saldo
            )

        return nueva_cuenta.to_dict()

    def buscar_cuenta(self, numero_cuenta):
        """
        Busca una cuenta por su número.
        """
        cuenta_obj = self.cuentas.get(numero_cuenta)
        return cuenta_obj.to_dict() if cuenta_obj else None

    def depositar(self, numero_cuenta, monto):
        """
        Realiza un depósito en una cuenta.
        """
        if monto <= 0:
            raise ValueError("El monto a depositar debe ser mayor a cero")

        cuenta_obj = self.cuentas.get(numero_cuenta)
        if not cuenta_obj:
            raise ValueError(f"La cuenta {numero_cuenta} no existe")

        if cuenta_obj.estado != "Activa":
            raise ValueError("La cuenta no está activa")

        saldo_anterior = cuenta_obj.saldo
        monto_decimal = Decimal(str(monto)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        cuenta_obj.saldo += monto_decimal

        transaccion = self._registrar_transaccion(
            numero_cuenta,
            "Depósito",
            monto_decimal,
            cuenta_obj.saldo,
            saldo_anterior
        )

        return transaccion.to_dict()

    def retirar(self, numero_cuenta, monto):
        """
        Realiza un retiro de una cuenta.
        """
        if monto <= 0:
            raise ValueError("El monto a retirar debe ser mayor a cero")

        cuenta_obj = self.cuentas.get(numero_cuenta)
        if not cuenta_obj:
            raise ValueError(f"La cuenta {numero_cuenta} no existe")

        if cuenta_obj.estado != "Activa":
            raise ValueError("La cuenta no está activa")

        monto_decimal = Decimal(str(monto)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        if cuenta_obj.saldo < monto_decimal:
            raise ValueError(f"Saldo insuficiente. Saldo disponible: ${cuenta_obj.saldo}")

        saldo_anterior = cuenta_obj.saldo
        cuenta_obj.saldo -= monto_decimal

        transaccion = self._registrar_transaccion(
            numero_cuenta,
            "Retiro",
            monto_decimal,
            cuenta_obj.saldo,
            saldo_anterior
        )

        return transaccion.to_dict()

    def transferir(self, numero_cuenta_origen, numero_cuenta_destino, monto):
        """
        Realiza una transferencia entre dos cuentas.
        """
        if monto <= 0:
            raise ValueError("El monto a transferir debe ser mayor a cero")

        if numero_cuenta_origen == numero_cuenta_destino:
            raise ValueError("No se puede transferir a la misma cuenta")

        cuenta_origen_obj = self.cuentas.get(numero_cuenta_origen)
        cuenta_destino_obj = self.cuentas.get(numero_cuenta_destino)

        if not cuenta_origen_obj:
            raise ValueError(f"La cuenta origen {numero_cuenta_origen} no existe")

        if not cuenta_destino_obj:
            raise ValueError(f"La cuenta destino {numero_cuenta_destino} no existe")

        if cuenta_origen_obj.estado != "Activa" or cuenta_destino_obj.estado != "Activa":
            raise ValueError("Ambas cuentas deben estar activas")

        monto_decimal = Decimal(str(monto)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        if cuenta_origen_obj.saldo < monto_decimal:
            raise ValueError(f"Saldo insuficiente en cuenta origen. Saldo disponible: ${cuenta_origen_obj.saldo}")

        # Realizar el retiro de la cuenta origen
        saldo_anterior_origen = cuenta_origen_obj.saldo
        cuenta_origen_obj.saldo -= monto_decimal

        # Realizar el depósito en la cuenta destino
        saldo_anterior_destino = cuenta_destino_obj.saldo
        cuenta_destino_obj.saldo += monto_decimal

        # Registrar ambas transacciones
        trans_origen = self._registrar_transaccion(
            numero_cuenta_origen,
            f"Transferencia a {numero_cuenta_destino}",
            monto_decimal,
            cuenta_origen_obj.saldo,
            saldo_anterior_origen
        )

        trans_destino = self._registrar_transaccion(
            numero_cuenta_destino,
            f"Transferencia desde {numero_cuenta_origen}",
            monto_decimal,
            cuenta_destino_obj.saldo,
            saldo_anterior_destino
        )

        return (trans_origen.to_dict(), trans_destino.to_dict())

    def obtener_todas_cuentas(self):
        """
        Obtiene todas las cuentas del sistema.
        """
        return [cuenta.to_dict() for cuenta in self.cuentas.values()]

    def obtener_transacciones_cuenta(self, numero_cuenta):
        """
        Obtiene todas las transacciones de una cuenta específica.
        """
        transacciones_cuenta = []
        for trans in self.transacciones:
            if trans.numero_cuenta == numero_cuenta:
                transacciones_cuenta.append(trans.to_dict())
        return transacciones_cuenta

    def obtener_todas_transacciones(self):
        """
        Obtiene todas las transacciones del sistema.
        """
        return [trans.to_dict() for trans in self.transacciones]

    def buscar_cuentas_por_titular(self, nombre_titular):
        """
        Busca cuentas por nombre del titular.
        """
        if not nombre_titular.strip():
            return self.obtener_todas_cuentas()

        termino = nombre_titular.strip().lower()
        cuentas_encontradas = []

        for cuenta in self.cuentas.values():
            if termino in cuenta.titular.lower():
                cuentas_encontradas.append(cuenta.to_dict())

        return cuentas_encontradas

    def obtener_estadisticas(self):
        """
        Obtiene estadísticas generales del sistema bancario.
        """
        total_cuentas = len(self.cuentas)
        total_transacciones = len(self.transacciones)
        saldo_total = sum(cuenta.saldo for cuenta in self.cuentas.values())

        cuentas_activas = sum(1 for cuenta in self.cuentas.values() if cuenta.estado == "Activa")

        return {
            "total_cuentas": total_cuentas,
            "cuentas_activas": cuentas_activas,
            "total_transacciones": total_transacciones,
            "saldo_total_sistema": saldo_total
        }

    def _registrar_transaccion(self, numero_cuenta, tipo, monto, saldo_nuevo, saldo_anterior=None):
        """
        Registra una transacción en el historial.
        """
        transaccion = Transaccion(
            self.siguiente_id_transaccion,
            numero_cuenta,
            tipo,
            monto,
            saldo_nuevo,
            saldo_anterior
        )

        self.transacciones.append(transaccion)
        self.siguiente_id_transaccion += 1

        return transaccion
