"""
Punto de entrada principal del Sistema de Gestión Bancaria.
Importa la GUI y la inicia.
"""

import tkinter as tk
import os
from gui import AplicacionBancaria


def main():
    """Función principal que inicia la aplicación bancaria."""
    # Crear la ventana principal de Tkinter
    ventana_principal = tk.Tk()
    
    # Establecer el ícono de la ventana
    try:
        # Usar una ruta absoluta para mayor robustez
        ruta_icono = os.path.join(os.path.dirname(__file__), 'bank_icon.ico')
        ventana_principal.iconbitmap(ruta_icono)
    except tk.TclError:
        # Manejar el error si el archivo no se encuentra o no es válido
        print("Advertencia: No se pudo cargar el ícono 'bank_icon.ico'.")
    
    # Crear la instancia de la aplicación
    app = AplicacionBancaria(ventana_principal)
    
    # Iniciar el loop de la aplicación
    app.iniciar()


if __name__ == "__main__":
    main()
