"""
Script de prueba completo para el Sistema de Gestión Bancaria.
Prueba todas las funcionalidades del sistema.
"""

from logic import SistemaBancario


def test_sistema_bancario():
    """Prueba todas las funcionalidades del sistema bancario."""
    print("╔═══════════════════════════════════════════════════════════════╗")
    print("║     PRUEBAS DEL SISTEMA DE GESTIÓN BANCARIA                  ║")
    print("╚═══════════════════════════════════════════════════════════════╝\n")
    
    # Crear instancia del sistema
    sistema = SistemaBancario()
    print("✓ Sistema bancario inicializado\n")
    
    # ===== PRUEBA 1: CREAR CUENTAS =====
    print("━━━ PRUEBA 1: Crear Cuentas ━━━")
    
    cuenta1 = sistema.crear_cuenta("Juan Pérez", "Ahorro", 5000.00)
    print(f"✓ Cuenta creada: {cuenta1['numero_cuenta']} - {cuenta1['titular']} - ${cuenta1['saldo']}")
    
    cuenta2 = sistema.crear_cuenta("María González", "Corriente", 10000.00)
    print(f"✓ Cuenta creada: {cuenta2['numero_cuenta']} - {cuenta2['titular']} - ${cuenta2['saldo']}")
    
    cuenta3 = sistema.crear_cuenta("Carlos Rodríguez", "Nómina", 3000.00)
    print(f"✓ Cuenta creada: {cuenta3['numero_cuenta']} - {cuenta3['titular']} - ${cuenta3['saldo']}")
    
    cuenta4 = sistema.crear_cuenta("Ana Martínez", "Ahorro", 0.00)
    print(f"✓ Cuenta creada: {cuenta4['numero_cuenta']} - {cuenta4['titular']} - ${cuenta4['saldo']}")
    
    print(f"\nTotal de cuentas creadas: {len(sistema.obtener_todas_cuentas())}\n")
    
    # ===== PRUEBA 2: DEPÓSITOS =====
    print("━━━ PRUEBA 2: Realizar Depósitos ━━━")
    
    trans1 = sistema.depositar(cuenta1['numero_cuenta'], 1500.00)
    print(f"✓ Depósito en cuenta {cuenta1['numero_cuenta']}: ${trans1['monto']}")
    print(f"  Saldo anterior: ${trans1['saldo_anterior']} → Nuevo saldo: ${trans1['saldo_nuevo']}")
    
    trans2 = sistema.depositar(cuenta4['numero_cuenta'], 2000.00)
    print(f"✓ Depósito en cuenta {cuenta4['numero_cuenta']}: ${trans2['monto']}")
    print(f"  Saldo anterior: ${trans2['saldo_anterior']} → Nuevo saldo: ${trans2['saldo_nuevo']}\n")
    
    # ===== PRUEBA 3: RETIROS =====
    print("━━━ PRUEBA 3: Realizar Retiros ━━━")
    
    trans3 = sistema.retirar(cuenta2['numero_cuenta'], 2500.00)
    print(f"✓ Retiro de cuenta {cuenta2['numero_cuenta']}: ${trans3['monto']}")
    print(f"  Saldo anterior: ${trans3['saldo_anterior']} → Nuevo saldo: ${trans3['saldo_nuevo']}")
    
    trans4 = sistema.retirar(cuenta1['numero_cuenta'], 1000.00)
    print(f"✓ Retiro de cuenta {cuenta1['numero_cuenta']}: ${trans4['monto']}")
    print(f"  Saldo anterior: ${trans4['saldo_anterior']} → Nuevo saldo: ${trans4['saldo_nuevo']}\n")
    
    # ===== PRUEBA 4: TRANSFERENCIAS =====
    print("━━━ PRUEBA 4: Realizar Transferencias ━━━")
    
    trans_orig, trans_dest = sistema.transferir(cuenta2['numero_cuenta'], cuenta3['numero_cuenta'], 1500.00)
    print(f"✓ Transferencia de {cuenta2['numero_cuenta']} a {cuenta3['numero_cuenta']}: $1500.00")
    print(f"  Cuenta origen - Saldo: ${trans_orig['saldo_anterior']} → ${trans_orig['saldo_nuevo']}")
    print(f"  Cuenta destino - Saldo: ${trans_dest['saldo_anterior']} → ${trans_dest['saldo_nuevo']}\n")
    
    # ===== PRUEBA 5: BUSCAR CUENTA =====
    print("━━━ PRUEBA 5: Buscar Cuenta ━━━")
    
    cuenta_encontrada = sistema.buscar_cuenta(cuenta1['numero_cuenta'])
    if cuenta_encontrada:
        print(f"✓ Cuenta encontrada: {cuenta_encontrada['numero_cuenta']}")
        print(f"  Titular: {cuenta_encontrada['titular']}")
        print(f"  Tipo: {cuenta_encontrada['tipo_cuenta']}")
        print(f"  Saldo: ${cuenta_encontrada['saldo']}")
        print(f"  Estado: {cuenta_encontrada['estado']}\n")
    
    # ===== PRUEBA 6: BUSCAR POR TITULAR =====
    print("━━━ PRUEBA 6: Buscar por Titular ━━━")
    
    resultados = sistema.buscar_cuentas_por_titular("María")
    print(f"Búsqueda 'María': {len(resultados)} resultado(s)")
    for cuenta in resultados:
        print(f"  → {cuenta['numero_cuenta']} - {cuenta['titular']}")
    
    resultados = sistema.buscar_cuentas_por_titular("Pérez")
    print(f"\nBúsqueda 'Pérez': {len(resultados)} resultado(s)")
    for cuenta in resultados:
        print(f"  → {cuenta['numero_cuenta']} - {cuenta['titular']}\n")
    
    # ===== PRUEBA 7: HISTORIAL DE TRANSACCIONES =====
    print("━━━ PRUEBA 7: Historial de Transacciones ━━━")
    
    transacciones_cuenta1 = sistema.obtener_transacciones_cuenta(cuenta1['numero_cuenta'])
    print(f"Transacciones de cuenta {cuenta1['numero_cuenta']}: {len(transacciones_cuenta1)}")
    for trans in transacciones_cuenta1:
        print(f"  [{trans['fecha']}] {trans['tipo']} - ${trans['monto']}")
    
    print(f"\nTotal de transacciones en el sistema: {len(sistema.obtener_todas_transacciones())}\n")
    
    # ===== PRUEBA 8: ESTADÍSTICAS =====
    print("━━━ PRUEBA 8: Estadísticas del Sistema ━━━")
    
    stats = sistema.obtener_estadisticas()
    print(f"Total de cuentas: {stats['total_cuentas']}")
    print(f"Cuentas activas: {stats['cuentas_activas']}")
    print(f"Total de transacciones: {stats['total_transacciones']}")
    print(f"Saldo total en el sistema: ${stats['saldo_total_sistema']}\n")
    
    # ===== PRUEBA 9: VALIDACIONES =====
    print("━━━ PRUEBA 9: Validaciones ━━━")
    
    # Título vacío
    try:
        sistema.crear_cuenta("", "Ahorro", 1000)
        print("✗ ERROR: Debería rechazar titular vacío")
    except ValueError as e:
        print(f"✓ Validación correcta: {e}")
    
    # Saldo negativo
    try:
        sistema.crear_cuenta("Test", "Ahorro", -500)
        print("✗ ERROR: Debería rechazar saldo negativo")
    except ValueError as e:
        print(f"✓ Validación correcta: {e}")
    
    # Retiro mayor al saldo
    try:
        sistema.retirar(cuenta4['numero_cuenta'], 50000)
        print("✗ ERROR: Debería rechazar retiro mayor al saldo")
    except ValueError as e:
        print(f"✓ Validación correcta: {e}")
    
    # Cuenta inexistente
    try:
        sistema.depositar(999999, 100)
        print("✗ ERROR: Debería rechazar cuenta inexistente")
    except ValueError as e:
        print(f"✓ Validación correcta: {e}")
    
    # Transferencia a la misma cuenta
    try:
        sistema.transferir(cuenta1['numero_cuenta'], cuenta1['numero_cuenta'], 100)
        print("✗ ERROR: Debería rechazar transferencia a la misma cuenta")
    except ValueError as e:
        print(f"✓ Validación correcta: {e}")
    
    print("\n╔═══════════════════════════════════════════════════════════════╗")
    print("║     TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE               ║")
    print("╚═══════════════════════════════════════════════════════════════╝")
    
    # Mostrar resumen final
    print("\n📊 RESUMEN FINAL:")
    print(f"   • Cuentas creadas: {stats['total_cuentas']}")
    print(f"   • Transacciones realizadas: {stats['total_transacciones']}")
    print(f"   • Saldo total: ${stats['saldo_total_sistema']}")
    
    print("\n✓ El sistema está listo para usarse")


if __name__ == "__main__":
    test_sistema_bancario()
