"""
Módulo de interfaz gráfica para el Sistema de Gestión Bancaria.
Implementa la GUI usando Tkinter con múltiples pestañas y funcionalidades completas.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from operations.sistema import SistemaBancario


class AplicacionBancaria:
    """Clase principal de la interfaz gráfica del sistema bancario."""
    
    def __init__(self, ventana_principal):
        """
        Inicializa la aplicación bancaria con la ventana principal.
        
        Args:
            ventana_principal: Instancia de tk.Tk()
        """
        self.ventana = ventana_principal
        self.ventana.title("Sistema de Gestión Bancaria")
        self.ventana.geometry("1000x700")
        self.ventana.resizable(True, True)
        
        # Instanciar el sistema bancario
        self.sistema = SistemaBancario()
        
        # Configurar la interfaz
        self._configurar_interfaz()
    
    def _configurar_interfaz(self):
        """Configura todos los componentes de la interfaz."""
        
        # Frame principal con padding
        frame_principal = ttk.Frame(self.ventana, padding="10")
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar expansión de la ventana
        self.ventana.columnconfigure(0, weight=1)
        self.ventana.rowconfigure(0, weight=1)
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.rowconfigure(1, weight=1)
        
        # ===== TÍTULO =====
        titulo = ttk.Label(
            frame_principal,
            text="🏦 SISTEMA DE GESTIÓN BANCARIA",
            font=("Arial", 18, "bold")
        )
        titulo.grid(row=0, column=0, pady=(0, 10))
        
        # ===== NOTEBOOK (PESTAÑAS) =====
        self.notebook = ttk.Notebook(frame_principal)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Crear las pestañas
        self._crear_pestaña_cuentas()
        self._crear_pestaña_operaciones()
        self._crear_pestaña_transacciones()
        self._crear_pestaña_busqueda()
        
        # ===== BARRA DE ESTADO =====
        self.label_estado = ttk.Label(
            frame_principal,
            text="Sistema iniciado | Cuentas: 0 | Transacciones: 0",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.label_estado.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Actualizar estado inicial
        self._actualizar_estado()
    
    def _crear_pestaña_cuentas(self):
        """Crea la pestaña de gestión de cuentas."""
        frame_cuentas = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame_cuentas, text="📋 Gestión de Cuentas")
        
        frame_cuentas.columnconfigure(0, weight=1)
        frame_cuentas.rowconfigure(2, weight=1)
        
        # ===== FORMULARIO DE NUEVA CUENTA =====
        frame_nueva_cuenta = ttk.LabelFrame(frame_cuentas, text="Crear Nueva Cuenta", padding="10")
        frame_nueva_cuenta.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        frame_nueva_cuenta.columnconfigure(1, weight=1)
        
        # Titular
        ttk.Label(frame_nueva_cuenta, text="Titular:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_titular = ttk.Entry(frame_nueva_cuenta, width=40)
        self.entry_titular.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 10), pady=5)
        
        # Tipo de cuenta
        ttk.Label(frame_nueva_cuenta, text="Tipo de Cuenta:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.combo_tipo_cuenta = ttk.Combobox(
            frame_nueva_cuenta,
            values=["Ahorro", "Corriente", "Nómina"],
            state="readonly",
            width=15
        )
        self.combo_tipo_cuenta.current(0)
        self.combo_tipo_cuenta.grid(row=0, column=3, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Saldo inicial
        ttk.Label(frame_nueva_cuenta, text="Saldo Inicial:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_saldo_inicial = ttk.Entry(frame_nueva_cuenta, width=20)
        self.entry_saldo_inicial.insert(0, "0.00")
        self.entry_saldo_inicial.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Botón crear cuenta
        self.btn_crear_cuenta = ttk.Button(
            frame_nueva_cuenta,
            text="Crear Cuenta",
            command=self._crear_cuenta
        )
        self.btn_crear_cuenta.grid(row=1, column=2, columnspan=2, padx=(10, 0), pady=5)
        
        # ===== BOTONES DE ACCIÓN =====
        frame_botones_cuentas = ttk.Frame(frame_cuentas)
        frame_botones_cuentas.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Button(
            frame_botones_cuentas,
            text="Actualizar Lista",
            command=self._actualizar_lista_cuentas
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        # ===== LISTA DE CUENTAS =====
        frame_lista_cuentas = ttk.LabelFrame(frame_cuentas, text="Cuentas Registradas", padding="10")
        frame_lista_cuentas.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame_lista_cuentas.columnconfigure(0, weight=1)
        frame_lista_cuentas.rowconfigure(0, weight=1)
        
        # Treeview para cuentas
        columnas_cuentas = ("Número", "Titular", "Tipo", "Saldo", "Fecha Apertura", "Estado")
        self.tree_cuentas = ttk.Treeview(
            frame_lista_cuentas,
            columns=columnas_cuentas,
            show="headings",
            height=15
        )
        
        # Configurar columnas
        self.tree_cuentas.heading("Número", text="Número de Cuenta")
        self.tree_cuentas.heading("Titular", text="Titular")
        self.tree_cuentas.heading("Tipo", text="Tipo")
        self.tree_cuentas.heading("Saldo", text="Saldo")
        self.tree_cuentas.heading("Fecha Apertura", text="Fecha Apertura")
        self.tree_cuentas.heading("Estado", text="Estado")
        
        self.tree_cuentas.column("Número", width=120, anchor=tk.CENTER)
        self.tree_cuentas.column("Titular", width=200, anchor=tk.W)
        self.tree_cuentas.column("Tipo", width=100, anchor=tk.CENTER)
        self.tree_cuentas.column("Saldo", width=120, anchor=tk.E)
        self.tree_cuentas.column("Fecha Apertura", width=150, anchor=tk.CENTER)
        self.tree_cuentas.column("Estado", width=80, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar_cuentas = ttk.Scrollbar(frame_lista_cuentas, orient=tk.VERTICAL, command=self.tree_cuentas.yview)
        self.tree_cuentas.configure(yscrollcommand=scrollbar_cuentas.set)
        
        self.tree_cuentas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_cuentas.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def _crear_pestaña_operaciones(self):
        """Crea la pestaña de operaciones bancarias."""
        frame_operaciones = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame_operaciones, text="💰 Operaciones")
        
        frame_operaciones.columnconfigure(0, weight=1)
        
        # ===== DEPÓSITO =====
        frame_deposito = ttk.LabelFrame(frame_operaciones, text="Depósito", padding="10")
        frame_deposito.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        frame_deposito.columnconfigure(1, weight=1)
        
        ttk.Label(frame_deposito, text="Número de Cuenta:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_deposito_cuenta = ttk.Entry(frame_deposito, width=20)
        self.entry_deposito_cuenta.grid(row=0, column=1, sticky=tk.W, padx=(10, 10), pady=5)
        
        ttk.Label(frame_deposito, text="Monto:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.entry_deposito_monto = ttk.Entry(frame_deposito, width=20)
        self.entry_deposito_monto.grid(row=0, column=3, sticky=tk.W, padx=(10, 10), pady=5)
        
        ttk.Button(
            frame_deposito,
            text="Realizar Depósito",
            command=self._realizar_deposito
        ).grid(row=0, column=4, padx=(10, 0), pady=5)
        
        # ===== RETIRO =====
        frame_retiro = ttk.LabelFrame(frame_operaciones, text="Retiro", padding="10")
        frame_retiro.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        frame_retiro.columnconfigure(1, weight=1)
        
        ttk.Label(frame_retiro, text="Número de Cuenta:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_retiro_cuenta = ttk.Entry(frame_retiro, width=20)
        self.entry_retiro_cuenta.grid(row=0, column=1, sticky=tk.W, padx=(10, 10), pady=5)
        
        ttk.Label(frame_retiro, text="Monto:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.entry_retiro_monto = ttk.Entry(frame_retiro, width=20)
        self.entry_retiro_monto.grid(row=0, column=3, sticky=tk.W, padx=(10, 10), pady=5)
        
        ttk.Button(
            frame_retiro,
            text="Realizar Retiro",
            command=self._realizar_retiro
        ).grid(row=0, column=4, padx=(10, 0), pady=5)
        
        # ===== TRANSFERENCIA =====
        frame_transferencia = ttk.LabelFrame(frame_operaciones, text="Transferencia", padding="10")
        frame_transferencia.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        frame_transferencia.columnconfigure(1, weight=1)
        
        ttk.Label(frame_transferencia, text="Cuenta Origen:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_trans_origen = ttk.Entry(frame_transferencia, width=20)
        self.entry_trans_origen.grid(row=0, column=1, sticky=tk.W, padx=(10, 10), pady=5)
        
        ttk.Label(frame_transferencia, text="Cuenta Destino:").grid(row=0, column=2, sticky=tk.W, pady=5)
        self.entry_trans_destino = ttk.Entry(frame_transferencia, width=20)
        self.entry_trans_destino.grid(row=0, column=3, sticky=tk.W, padx=(10, 10), pady=5)
        
        ttk.Label(frame_transferencia, text="Monto:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_trans_monto = ttk.Entry(frame_transferencia, width=20)
        self.entry_trans_monto.grid(row=1, column=1, sticky=tk.W, padx=(10, 10), pady=5)
        
        ttk.Button(
            frame_transferencia,
            text="Realizar Transferencia",
            command=self._realizar_transferencia
        ).grid(row=1, column=2, columnspan=2, padx=(10, 0), pady=5)
        
        # ===== CONSULTA DE SALDO =====
        frame_consulta = ttk.LabelFrame(frame_operaciones, text="Consulta de Saldo", padding="10")
        frame_consulta.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        frame_consulta.columnconfigure(0, weight=1)
        frame_consulta.rowconfigure(1, weight=1)
        
        frame_consulta_input = ttk.Frame(frame_consulta)
        frame_consulta_input.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(frame_consulta_input, text="Número de Cuenta:").pack(side=tk.LEFT, padx=(0, 10))
        self.entry_consulta_cuenta = ttk.Entry(frame_consulta_input, width=20)
        self.entry_consulta_cuenta.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            frame_consulta_input,
            text="Consultar Saldo",
            command=self._consultar_saldo
        ).pack(side=tk.LEFT)
        
        # Área de resultado
        self.text_consulta = tk.Text(frame_consulta, height=10, width=80, wrap=tk.WORD)
        self.text_consulta.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar_consulta = ttk.Scrollbar(frame_consulta, orient=tk.VERTICAL, command=self.text_consulta.yview)
        self.text_consulta.configure(yscrollcommand=scrollbar_consulta.set)
        scrollbar_consulta.grid(row=1, column=1, sticky=(tk.N, tk.S))
    
    def _crear_pestaña_transacciones(self):
        """Crea la pestaña de historial de transacciones."""
        frame_transacciones = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame_transacciones, text="📊 Transacciones")
        
        frame_transacciones.columnconfigure(0, weight=1)
        frame_transacciones.rowconfigure(1, weight=1)
        
        # ===== FILTROS =====
        frame_filtros = ttk.LabelFrame(frame_transacciones, text="Filtros", padding="10")
        frame_filtros.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(frame_filtros, text="Número de Cuenta (opcional):").pack(side=tk.LEFT, padx=(0, 10))
        self.entry_filtro_cuenta = ttk.Entry(frame_filtros, width=20)
        self.entry_filtro_cuenta.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            frame_filtros,
            text="Mostrar Transacciones",
            command=self._mostrar_transacciones
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            frame_filtros,
            text="Mostrar Todas",
            command=self._mostrar_todas_transacciones
        ).pack(side=tk.LEFT)
        
        # ===== LISTA DE TRANSACCIONES =====
        frame_lista_trans = ttk.LabelFrame(frame_transacciones, text="Historial de Transacciones", padding="10")
        frame_lista_trans.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame_lista_trans.columnconfigure(0, weight=1)
        frame_lista_trans.rowconfigure(0, weight=1)
        
        # Treeview para transacciones
        columnas_trans = ("ID", "Cuenta", "Tipo", "Monto", "Saldo Anterior", "Saldo Nuevo", "Fecha")
        self.tree_transacciones = ttk.Treeview(
            frame_lista_trans,
            columns=columnas_trans,
            show="headings",
            height=20
        )
        
        # Configurar columnas
        self.tree_transacciones.heading("ID", text="ID")
        self.tree_transacciones.heading("Cuenta", text="Cuenta")
        self.tree_transacciones.heading("Tipo", text="Tipo")
        self.tree_transacciones.heading("Monto", text="Monto")
        self.tree_transacciones.heading("Saldo Anterior", text="Saldo Anterior")
        self.tree_transacciones.heading("Saldo Nuevo", text="Saldo Nuevo")
        self.tree_transacciones.heading("Fecha", text="Fecha")
        
        self.tree_transacciones.column("ID", width=50, anchor=tk.CENTER)
        self.tree_transacciones.column("Cuenta", width=100, anchor=tk.CENTER)
        self.tree_transacciones.column("Tipo", width=180, anchor=tk.W)
        self.tree_transacciones.column("Monto", width=100, anchor=tk.E)
        self.tree_transacciones.column("Saldo Anterior", width=120, anchor=tk.E)
        self.tree_transacciones.column("Saldo Nuevo", width=120, anchor=tk.E)
        self.tree_transacciones.column("Fecha", width=150, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar_trans = ttk.Scrollbar(frame_lista_trans, orient=tk.VERTICAL, command=self.tree_transacciones.yview)
        self.tree_transacciones.configure(yscrollcommand=scrollbar_trans.set)
        
        self.tree_transacciones.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar_trans.grid(row=0, column=1, sticky=(tk.N, tk.S))
    
    def _crear_pestaña_busqueda(self):
        """Crea la pestaña de búsqueda y estadísticas."""
        frame_busqueda = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(frame_busqueda, text="🔍 Búsqueda")
        
        frame_busqueda.columnconfigure(0, weight=1)
        frame_busqueda.rowconfigure(1, weight=1)
        
        # ===== BÚSQUEDA POR TITULAR =====
        frame_buscar = ttk.LabelFrame(frame_busqueda, text="Buscar Cuentas por Titular", padding="10")
        frame_buscar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        ttk.Label(frame_buscar, text="Nombre del Titular:").pack(side=tk.LEFT, padx=(0, 10))
        self.entry_buscar_titular = ttk.Entry(frame_buscar, width=40)
        self.entry_buscar_titular.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            frame_buscar,
            text="Buscar",
            command=self._buscar_por_titular
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            frame_buscar,
            text="Mostrar Todas",
            command=self._actualizar_lista_cuentas
        ).pack(side=tk.LEFT)
        
        # ===== ESTADÍSTICAS =====
        frame_estadisticas = ttk.LabelFrame(frame_busqueda, text="Estadísticas del Sistema", padding="10")
        frame_estadisticas.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame_estadisticas.columnconfigure(0, weight=1)
        frame_estadisticas.rowconfigure(0, weight=1)
        
        self.text_estadisticas = tk.Text(frame_estadisticas, height=15, width=80, wrap=tk.WORD, font=("Courier", 10))
        self.text_estadisticas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar_stats = ttk.Scrollbar(frame_estadisticas, orient=tk.VERTICAL, command=self.text_estadisticas.yview)
        self.text_estadisticas.configure(yscrollcommand=scrollbar_stats.set)
        scrollbar_stats.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Botón actualizar estadísticas
        ttk.Button(
            frame_busqueda,
            text="Actualizar Estadísticas",
            command=self._actualizar_estadisticas
        ).grid(row=2, column=0, pady=(10, 0))
        
        # Actualizar estadísticas iniciales
        self._actualizar_estadisticas()
    
    # ===== MÉTODOS DE ACCIÓN =====
    
    def _crear_cuenta(self):
        """Crea una nueva cuenta bancaria."""
        titular = self.entry_titular.get()
        tipo_cuenta = self.combo_tipo_cuenta.get()
        saldo_inicial_str = self.entry_saldo_inicial.get()
        
        try:
            saldo_inicial = float(saldo_inicial_str)
            cuenta = self.sistema.crear_cuenta(titular, tipo_cuenta, saldo_inicial)
            
            self._actualizar_lista_cuentas()
            self._actualizar_estado()
            
            # Limpiar campos
            self.entry_titular.delete(0, tk.END)
            self.entry_saldo_inicial.delete(0, tk.END)
            self.entry_saldo_inicial.insert(0, "0.00")
            
            messagebox.showinfo(
                "Éxito",
                f"Cuenta creada exitosamente\n\n"
                f"Número de cuenta: {cuenta['numero_cuenta']}\n"
                f"Titular: {cuenta['titular']}\n"
                f"Tipo: {cuenta['tipo_cuenta']}\n"
                f"Saldo inicial: ${cuenta['saldo']}"
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def _realizar_deposito(self):
        """Realiza un depósito en una cuenta."""
        try:
            numero_cuenta = int(self.entry_deposito_cuenta.get())
            monto = float(self.entry_deposito_monto.get())
            
            transaccion = self.sistema.depositar(numero_cuenta, monto)
            
            self._actualizar_lista_cuentas()
            self._actualizar_estado()
            
            # Limpiar campos
            self.entry_deposito_cuenta.delete(0, tk.END)
            self.entry_deposito_monto.delete(0, tk.END)
            
            messagebox.showinfo(
                "Éxito",
                f"Depósito realizado exitosamente\n\n"
                f"Cuenta: {numero_cuenta}\n"
                f"Monto depositado: ${transaccion['monto']}\n"
                f"Nuevo saldo: ${transaccion['saldo_nuevo']}"
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def _realizar_retiro(self):
        """Realiza un retiro de una cuenta."""
        try:
            numero_cuenta = int(self.entry_retiro_cuenta.get())
            monto = float(self.entry_retiro_monto.get())
            
            transaccion = self.sistema.retirar(numero_cuenta, monto)
            
            self._actualizar_lista_cuentas()
            self._actualizar_estado()
            
            # Limpiar campos
            self.entry_retiro_cuenta.delete(0, tk.END)
            self.entry_retiro_monto.delete(0, tk.END)
            
            messagebox.showinfo(
                "Éxito",
                f"Retiro realizado exitosamente\n\n"
                f"Cuenta: {numero_cuenta}\n"
                f"Monto retirado: ${transaccion['monto']}\n"
                f"Nuevo saldo: ${transaccion['saldo_nuevo']}"
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def _realizar_transferencia(self):
        """Realiza una transferencia entre cuentas."""
        try:
            cuenta_origen = int(self.entry_trans_origen.get())
            cuenta_destino = int(self.entry_trans_destino.get())
            monto = float(self.entry_trans_monto.get())
            
            trans_origen, trans_destino = self.sistema.transferir(cuenta_origen, cuenta_destino, monto)
            
            self._actualizar_lista_cuentas()
            self._actualizar_estado()
            
            # Limpiar campos
            self.entry_trans_origen.delete(0, tk.END)
            self.entry_trans_destino.delete(0, tk.END)
            self.entry_trans_monto.delete(0, tk.END)
            
            messagebox.showinfo(
                "Éxito",
                f"Transferencia realizada exitosamente\n\n"
                f"De cuenta: {cuenta_origen}\n"
                f"A cuenta: {cuenta_destino}\n"
                f"Monto: ${monto}\n\n"
                f"Saldo cuenta origen: ${trans_origen['saldo_nuevo']}\n"
                f"Saldo cuenta destino: ${trans_destino['saldo_nuevo']}"
            )
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def _consultar_saldo(self):
        """Consulta el saldo y detalles de una cuenta."""
        try:
            numero_cuenta = int(self.entry_consulta_cuenta.get())
            cuenta = self.sistema.buscar_cuenta(numero_cuenta)
            
            if not cuenta:
                messagebox.showerror("Error", f"La cuenta {numero_cuenta} no existe")
                return
            
            # Obtener transacciones de la cuenta
            transacciones = self.sistema.obtener_transacciones_cuenta(numero_cuenta)
            
            # Mostrar información
            self.text_consulta.delete(1.0, tk.END)
            
            info = f"""
═══════════════════════════════════════════════════════════════
                    INFORMACIÓN DE LA CUENTA
═══════════════════════════════════════════════════════════════

Número de Cuenta:    {cuenta['numero_cuenta']}
Titular:             {cuenta['titular']}
Tipo de Cuenta:      {cuenta['tipo_cuenta']}
Saldo Actual:        ${cuenta['saldo']}
Fecha de Apertura:   {cuenta['fecha_apertura']}
Estado:              {cuenta['estado']}

═══════════════════════════════════════════════════════════════
                    ÚLTIMAS TRANSACCIONES
═══════════════════════════════════════════════════════════════

Total de transacciones: {len(transacciones)}

"""
            self.text_consulta.insert(1.0, info)
            
            if transacciones:
                for trans in transacciones[-10:]:  # Últimas 10 transacciones
                    trans_info = f"""
[{trans['fecha']}]
Tipo: {trans['tipo']}
Monto: ${trans['monto']}
Saldo anterior: ${trans['saldo_anterior']} → Saldo nuevo: ${trans['saldo_nuevo']}
{'-' * 60}
"""
                    self.text_consulta.insert(tk.END, trans_info)
            else:
                self.text_consulta.insert(tk.END, "\nNo hay transacciones registradas para esta cuenta.\n")
            
        except ValueError as e:
            messagebox.showerror("Error", "Ingrese un número de cuenta válido")
    
    def _actualizar_lista_cuentas(self):
        """Actualiza la lista de cuentas en el Treeview."""
        # Limpiar el Treeview
        for item in self.tree_cuentas.get_children():
            self.tree_cuentas.delete(item)
        
        # Obtener todas las cuentas
        cuentas = self.sistema.obtener_todas_cuentas()
        
        # Insertar cuentas en el Treeview
        for cuenta in cuentas:
            self.tree_cuentas.insert(
                "",
                tk.END,
                values=(
                    cuenta["numero_cuenta"],
                    cuenta["titular"],
                    cuenta["tipo_cuenta"],
                    f"${cuenta['saldo']}",
                    cuenta["fecha_apertura"],
                    cuenta["estado"]
                )
            )
    
    def _mostrar_transacciones(self):
        """Muestra transacciones filtradas por cuenta."""
        cuenta_str = self.entry_filtro_cuenta.get().strip()
        
        if not cuenta_str:
            self._mostrar_todas_transacciones()
            return
        
        try:
            numero_cuenta = int(cuenta_str)
            transacciones = self.sistema.obtener_transacciones_cuenta(numero_cuenta)
            self._actualizar_lista_transacciones(transacciones)
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número de cuenta válido")
    
    def _mostrar_todas_transacciones(self):
        """Muestra todas las transacciones del sistema."""
        self.entry_filtro_cuenta.delete(0, tk.END)
        transacciones = self.sistema.obtener_todas_transacciones()
        self._actualizar_lista_transacciones(transacciones)
    
    def _actualizar_lista_transacciones(self, transacciones=None):
        """Actualiza la lista de transacciones en el Treeview."""
        # Limpiar el Treeview
        for item in self.tree_transacciones.get_children():
            self.tree_transacciones.delete(item)
        
        if transacciones is None:
            transacciones = self.sistema.obtener_todas_transacciones()
        
        # Insertar transacciones en el Treeview
        for trans in transacciones:
            self.tree_transacciones.insert(
                "",
                tk.END,
                values=(
                    trans["id"],
                    trans["numero_cuenta"],
                    trans["tipo"],
                    f"${trans['monto']}",
                    f"${trans['saldo_anterior']}",
                    f"${trans['saldo_nuevo']}",
                    trans["fecha"]
                )
            )
    
    def _buscar_por_titular(self):
        """Busca cuentas por nombre del titular."""
        nombre = self.entry_buscar_titular.get()
        cuentas = self.sistema.buscar_cuentas_por_titular(nombre)
        
        # Limpiar el Treeview
        for item in self.tree_cuentas.get_children():
            self.tree_cuentas.delete(item)
        
        # Insertar resultados
        for cuenta in cuentas:
            self.tree_cuentas.insert(
                "",
                tk.END,
                values=(
                    cuenta["numero_cuenta"],
                    cuenta["titular"],
                    cuenta["tipo_cuenta"],
                    f"${cuenta['saldo']}",
                    cuenta["fecha_apertura"],
                    cuenta["estado"]
                )
            )
        
        # Cambiar a la pestaña de cuentas
        self.notebook.select(0)
    
    def _actualizar_estadisticas(self):
        """Actualiza las estadísticas del sistema."""
        stats = self.sistema.obtener_estadisticas()
        
        self.text_estadisticas.delete(1.0, tk.END)
        
        estadisticas_texto = f"""
╔═══════════════════════════════════════════════════════════════╗
║           ESTADÍSTICAS DEL SISTEMA BANCARIO                   ║
╚═══════════════════════════════════════════════════════════════╝

📊 RESUMEN GENERAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total de Cuentas:              {stats['total_cuentas']}
Cuentas Activas:               {stats['cuentas_activas']}
Total de Transacciones:        {stats['total_transacciones']}
Saldo Total en el Sistema:     ${stats['saldo_total_sistema']}


💼 DETALLE POR TIPO DE CUENTA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        # Contar por tipo de cuenta
        cuentas = self.sistema.obtener_todas_cuentas()
        tipos = {}
        for cuenta in cuentas:
            tipo = cuenta['tipo_cuenta']
            if tipo not in tipos:
                tipos[tipo] = {'cantidad': 0, 'saldo_total': 0}
            tipos[tipo]['cantidad'] += 1
            tipos[tipo]['saldo_total'] += cuenta['saldo']
        
        for tipo, datos in tipos.items():
            estadisticas_texto += f"\n{tipo}:\n"
            estadisticas_texto += f"  • Cantidad: {datos['cantidad']}\n"
            estadisticas_texto += f"  • Saldo total: ${datos['saldo_total']}\n"
        
        if cuentas:
            saldos = [float(c['saldo']) for c in cuentas]
            estadisticas_texto += f"""

📈 ANÁLISIS DE SALDOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Saldo Promedio:                ${sum(saldos) / len(saldos):.2f}
Saldo Máximo:                  ${max(saldos):.2f}
Saldo Mínimo:                  ${min(saldos):.2f}
"""
        
        self.text_estadisticas.insert(1.0, estadisticas_texto)
    
    def _actualizar_estado(self):
        """Actualiza la barra de estado."""
        stats = self.sistema.obtener_estadisticas()
        self.label_estado.config(
            text=f"Sistema Activo | Cuentas: {stats['total_cuentas']} | "
                 f"Transacciones: {stats['total_transacciones']} | "
                 f"Saldo Total: ${stats['saldo_total_sistema']}"
        )
    
    def iniciar(self):
        """Inicia el loop principal de la aplicación."""
        self.ventana.mainloop()
