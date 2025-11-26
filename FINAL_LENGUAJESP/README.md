# Sistema de Gestión Bancaria - Arquitectura Modular Avanzada 🏦

Esta es una versión reestructurada del Sistema de Gestión Bancaria, siguiendo un patrón de diseño modular más avanzado, similar al solicitado, separando los modelos de datos de las operaciones de negocio.

## Estructura del Proyecto

La nueva estructura del proyecto es la siguiente:

```
sistema_bancario/
├── main.py           # Punto de entrada de la aplicación
├── gui.py            # Interfaz gráfica con Tkinter
├── models/           # Módulos de Modelos de Datos
│   ├── __init__.py
│   └── banco.py      # Definición de las clases Cuenta y Transaccion
├── operations/       # Módulos de Lógica de Negocio y Operaciones
│   ├── __init__.py
│   └── sistema.py    # Clase SistemaBancario con toda la lógica de operaciones
├── test_operations.py # Script de pruebas automatizadas
└── README.md         # Este archivo
```

## Mapeo de Archivos

| Archivo Anterior | Nueva Ubicación | Propósito |
| :--- | :--- | :--- |
| `logic.py` | `operations/sistema.py` | Contiene la clase `SistemaBancario` (la lógica de negocio). |
| N/A | `models/banco.py` | Contiene las clases `Cuenta` y `Transaccion` (los modelos de datos). |
| `gui.py` | `gui.py` | Contiene la clase `AplicacionBancaria` (la interfaz de usuario). |
| `main.py` | `main.py` | Punto de entrada. |

## Funcionalidades

Todas las funcionalidades del sistema bancario completo se mantienen:

- **Creación de Cuentas** (Ahorro, Corriente, Nómina)
- **Operaciones** (Depósito, Retiro, Transferencia)
- **Consulta de Saldo** y **Historial de Transacciones**
- **Búsqueda** de cuentas por titular
- **Estadísticas** completas del sistema

## Requisitos

- Python 3.11 o superior
- Tkinter (incluido en Python)

## Uso

### Ejecutar la aplicación

```bash
python3.11 main.py
```

### Ejecutar las pruebas

```bash
python3.11 test_operations.py
```

## Cambios Clave en la Lógica (`operations/sistema.py`)

1. **Importación de Modelos:** Se importa `Cuenta` y `Transaccion` desde `models.banco`.
2. **Uso de Objetos:** La clase `SistemaBancario` ahora utiliza instancias de `Cuenta` y `Transaccion` internamente, y convierte a diccionario (`to_dict()`) solo al retornar datos a la GUI.
3. **Almacenamiento:** Las cuentas se almacenan en un diccionario (`self.cuentas = {}`) para un acceso más rápido por número de cuenta.

## Cambios Clave en la Interfaz (`gui.py`)

1. **Importación de Lógica:** La importación de la lógica se actualizó de `from logic import SistemaBancario` a `from operations.sistema import SistemaBancario`.

## Conclusión

La aplicación ahora sigue una estructura más limpia y escalable, separando claramente la capa de Modelos (`models/banco.py`) de la capa de Operaciones (`operations/sistema.py`), manteniendo la interfaz gráfica (`gui.py`) y el punto de entrada (`main.py`).


## Autor

**Nombre:** Joseph Alexander Morales Cardona
**Carrera:** Ingeniería Informática

## Licencia

Este proyecto está bajo la Licencia MIT.

**Licencia MIT**

Una licencia de software libre permisiva.

```
MIT License

Copyright (c) 2025 Joseph Alexander Morales Cardona

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
