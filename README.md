# Sistema de Gestión de Tareas con API y Base de Datos

**PFO 2 - Programación sobre Redes**

Sistema completo de gestión de tareas implementado con Flask, SQLite y autenticación segura mediante hash de contraseñas.

## Características

- **API REST completa** con Flask
- **Autenticación segura** con contraseñas hasheadas (PBKDF2-SHA256)
- **Persistencia de datos** con SQLite
- **Interfaz HTML moderna** y responsive
- **Sistema de sesiones** para usuarios autenticados

## Respuestas conceptuales

Se encuentran las respuestas conceptuales del PFO en el archivo RESPUESTAS.md en la raíz del proyecto.

## Requisitos Previos

Asegúrate de tener instalado:

- **Python 3.8 o superior**
- **pip** (gestor de paquetes de Python)

Verifica tu instalación:

```bash
python --version
pip --version
```

## Instalación

### Paso 1: Clonar o descargar el proyecto

```bash
# Si usas Git
git clone <url-del-repositorio>
cd "PFO 2"
```

### Paso 2: Crear un entorno virtual 

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Ejecutar el servidor

```bash
python servidor.py
```

El servidor se iniciará en `http://127.0.0.1:5000`

## Uso

### Acceder a la interfaz

Abre tu navegador en:
```
http://127.0.0.1:5500/app.html
```

Se muestra la página principal de la aplicación.

Se muestran las capturas de su uso en la carpeta: capturas_uso

## Endpoints de la API

### 2. Registro de Usuario
```
POST /registro
Content-Type: application/json

{
  "usuario": "nombre_usuario",
  "contraseña": "tu_contraseña"
}
```

**Respuestas:**
- `201 Created`: Usuario registrado exitosamente
- `400 Bad Request`: Datos incompletos o inválidos
- `409 Conflict`: Usuario ya existe

### 3. Inicio de Sesión
```
POST /login
Content-Type: application/json

{
  "usuario": "nombre_usuario",
  "contraseña": "tu_contraseña"
}
```

**Respuestas:**
- `200 OK`: Inicio de sesión exitoso
- `400 Bad Request`: Datos incompletos
- `401 Unauthorized`: Credenciales inválidas

### 4. Página de Tareas (Requiere autenticación)
```
GET /tareas
```

**Respuestas:**
- `200 OK`: Página HTML
- `401 Unauthorized`: No autenticado

### 5. Cerrar Sesión
```
POST /logout
```

Cierra la sesión del usuario actual.

**Respuestas:**
- `200 OK`: Sesión cerrada exitosamente
- `401 Unauthorized`: No hay sesión activa

## Tecnologías Utilizadas

- **Flask 3.0.0**: Framework web para Python
- **Werkzeug 3.0.0**: Utilidades WSGI y hashing de contraseñas
- **SQLite3**: Base de datos relacional embebida
- **HTML5/CSS3**: Interfaz web moderna

## Seguridad

### Hash de Contraseñas

El sistema utiliza **PBKDF2-SHA256** para hashear contraseñas:

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Al registrar
hashed = generate_password_hash(password, method='pbkdf2:sha256')

# Al verificar
check_password_hash(stored_hash, provided_password)
```

## Autor

**Micaela Lujan Orellano**
- Tecnicatura en Software
- Programación sobre Redes - 2026