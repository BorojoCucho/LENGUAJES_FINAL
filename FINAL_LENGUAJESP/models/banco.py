"""
Módulo de modelos de datos para el Sistema Bancario.
Define las estructuras de datos (cuentas y transacciones).
"""

from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP

# Constantes para tipos de cuenta
TIPOS_CUENTA = ["Ahorro", "Corriente", "Nómina"]

class Cuenta:
    """Modelo de datos para una cuenta bancaria."""
    
    def __init__(self, numero_cuenta, titular, tipo_cuenta, saldo_inicial):
        self.numero_cuenta = numero_cuenta
        self.titular = titular
        self.tipo_cuenta = tipo_cuenta
        self.saldo = Decimal(str(saldo_inicial)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.fecha_apertura = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.estado = "Activa"
    
    def to_dict(self):
        """Retorna la cuenta como un diccionario."""
        return {
            "numero_cuenta": self.numero_cuenta,
            "titular": self.titular,
            "tipo_cuenta": self.tipo_cuenta,
            "saldo": self.saldo,
            "fecha_apertura": self.fecha_apertura,
            "estado": self.estado
        }

class Transaccion:
    """Modelo de datos para una transacción bancaria."""
    
    def __init__(self, id_transaccion, numero_cuenta, tipo, monto, saldo_nuevo, saldo_anterior=None):
        self.id = id_transaccion
        self.numero_cuenta = numero_cuenta
        self.tipo = tipo
        self.monto = Decimal(str(monto)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        self.saldo_anterior = saldo_anterior if saldo_anterior is not None else saldo_nuevo
        self.saldo_nuevo = saldo_nuevo
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def to_dict(self):
        """Retorna la transacción como un diccionario."""
        return {
            "id": self.id,
            "numero_cuenta": self.numero_cuenta,
            "tipo": self.tipo,
            "monto": self.monto,
            "saldo_anterior": self.saldo_anterior,
            "saldo_nuevo": self.saldo_nuevo,
            "fecha": self.fecha
        }
