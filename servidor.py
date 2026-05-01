"""
Sistema de Gestión de Tareas con API y Base de Datos
Servidor Flask con autenticación y SQLite
"""

import sys
import io

# Configurar la codificación UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from flask import Flask, request, jsonify, render_template_string, session
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = 'clave_dev'

# Configurar CORS para permitir peticiones desde archivos locales
CORS(app, supports_credentials=True, origins=['*'])

# Configuración de la base de datos
DATABASE = 'database.db'

def get_db_connection():
    """Establece conexión con la base de datos SQLite"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la base de datos con las tablas necesarias"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de tareas (opcional para futuras expansiones)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✓ Base de datos inicializada correctamente")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({
                'error': 'No autorizado',
                'mensaje': 'Debe iniciar sesión primero'
            }), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Página de inicio con información de la API"""
    html = '''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API de Gestión de Tareas</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 40px;
                max-width: 800px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            }
            h1 {
                color: #667eea;
                margin-bottom: 10px;
                font-size: 2.5em;
            }
            .subtitle {
                color: #666;
                margin-bottom: 30px;
                font-size: 1.1em;
            }
            .endpoint {
                background: #f8f9fa;
                border-left: 4px solid #667eea;
                padding: 15px;
                margin: 15px 0;
                border-radius: 5px;
            }
            .method {
                display: inline-block;
                padding: 5px 10px;
                border-radius: 5px;
                font-weight: bold;
                margin-right: 10px;
                font-size: 0.9em;
            }
            .post { background: #28a745; color: white; }
            .get { background: #007bff; color: white; }
            .endpoint-path {
                font-family: 'Courier New', monospace;
                color: #333;
                font-weight: bold;
            }
            .description {
                margin-top: 10px;
                color: #666;
            }
            .example {
                background: #2d3748;
                color: #68d391;
                padding: 15px;
                border-radius: 5px;
                margin-top: 10px;
                font-family: 'Courier New', monospace;
                font-size: 0.9em;
                overflow-x: auto;
            }
            .status {
                display: inline-block;
                background: #28a745;
                color: white;
                padding: 5px 15px;
                border-radius: 20px;
                margin-top: 20px;
                font-weight: bold;
            }
            .footer {
                margin-top: 30px;
                padding-top: 20px;
                border-top: 2px solid #e9ecef;
                text-align: center;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 API de Gestión de Tareas</h1>
            <p class="subtitle">Sistema con autenticación y base de datos SQLite</p>
            
            <div class="status">✓ Servidor Activo</div>
            
            <h2 style="margin-top: 30px; color: #333;">📋 Endpoints Disponibles</h2>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <span class="endpoint-path">/registro</span>
                <div class="description">
                    Registra un nuevo usuario en el sistema
                </div>
                <div class="example">
{
  "usuario": "nombre_usuario",
  "contraseña": "tu_contraseña"
}
                </div>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <span class="endpoint-path">/login</span>
                <div class="description">
                    Inicia sesión con credenciales de usuario
                </div>
                <div class="example">
{
  "usuario": "nombre_usuario",
  "contraseña": "tu_contraseña"
}
                </div>
            </div>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-path">/tareas</span>
                <div class="description">
                    Muestra página de bienvenida (requiere autenticación)
                </div>
            </div>
            
            <div class="endpoint">
                <span class="method post">POST</span>
                <span class="endpoint-path">/logout</span>
                <div class="description">
                    Cierra la sesión del usuario actual
                </div>
            </div>
            
            <div class="footer">
                <p><strong>PFO 2:</strong> Sistema de Gestión de Tareas</p>
                <p>Programación sobre Redes - 2026</p>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/registro', methods=['POST'])
def registro():
    """
    Endpoint para registrar nuevos usuarios
    Recibe: {"usuario": "nombre", "contraseña": "1234"}
    """
    try:
        data = request.get_json()
        
        # Validación de datos
        if not data or 'usuario' not in data or 'contraseña' not in data:
            return jsonify({
                'error': 'Datos incompletos',
                'mensaje': 'Se requieren los campos "usuario" y "contraseña"'
            }), 400
        
        usuario = data['usuario'].strip()
        contraseña = data['contraseña']
        
        # Validaciones adicionales
        if len(usuario) < 3:
            return jsonify({
                'error': 'Usuario inválido',
                'mensaje': 'El usuario debe tener al menos 3 caracteres'
            }), 400
        
        if len(contraseña) < 4:
            return jsonify({
                'error': 'Contraseña inválida',
                'mensaje': 'La contraseña debe tener al menos 4 caracteres'
            }), 400
        
        # Hash de la contraseña
        contraseña_hash = generate_password_hash(contraseña, method='pbkdf2:sha256')
        
        # Insertar en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                'INSERT INTO users (usuario, contraseña_hash) VALUES (?, ?)',
                (usuario, contraseña_hash)
            )
            conn.commit()
            user_id = cursor.lastrowid
            
            return jsonify({
                'mensaje': 'Usuario registrado exitosamente',
                'usuario': usuario,
                'id': user_id
            }), 201
            
        except sqlite3.IntegrityError:
            return jsonify({
                'error': 'Usuario ya existe',
                'mensaje': f'El usuario "{usuario}" ya está registrado'
            }), 409
        
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({
            'error': 'Error del servidor',
            'mensaje': str(e)
        }), 500

@app.route('/login', methods=['POST'])
def login():
    """
    Endpoint para iniciar sesión
    Verifica credenciales y crea sesión
    """
    try:
        data = request.get_json()
        
        # Validación de datos
        if not data or 'usuario' not in data or 'contraseña' not in data:
            return jsonify({
                'error': 'Datos incompletos',
                'mensaje': 'Se requieren los campos "usuario" y "contraseña"'
            }), 400
        
        usuario = data['usuario'].strip()
        contraseña = data['contraseña']
        
        # Buscar usuario en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE usuario = ?', (usuario,))
        user = cursor.fetchone()
        conn.close()
        
        # Verificar si el usuario existe y la contraseña es correcta
        if user and check_password_hash(user['contraseña_hash'], contraseña):
            # Crear sesión
            session['user_id'] = user['id']
            session['usuario'] = user['usuario']
            
            return jsonify({
                'mensaje': 'Inicio de sesión exitoso',
                'usuario': user['usuario'],
                'id': user['id']
            }), 200
        else:
            return jsonify({
                'error': 'Credenciales inválidas',
                'mensaje': 'Usuario o contraseña incorrectos'
            }), 401
            
    except Exception as e:
        return jsonify({
            'error': 'Error del servidor',
            'mensaje': str(e)
        }), 500

@app.route('/logout', methods=['POST'])
@login_required
def logout():
    """Cierra la sesión del usuario actual"""
    usuario = session.get('usuario', 'Usuario')
    session.clear()
    return jsonify({
        'mensaje': f'Sesión cerrada exitosamente para {usuario}'
    }), 200

@app.route('/tareas')
@login_required
def tareas():
    """
    Endpoint que muestra un HTML de bienvenida
    Requiere autenticación previa
    """
    usuario = session.get('usuario', 'Usuario')
    user_id = session.get('user_id')
    
    # Obtener estadísticas del usuario
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as total FROM tasks WHERE user_id = ?', (user_id,))
    total_tasks = cursor.fetchone()['total']
    cursor.execute('SELECT COUNT(*) as completed FROM tasks WHERE user_id = ? AND completed = 1', (user_id,))
    completed_tasks = cursor.fetchone()['completed']
    conn.close()
    
    html = f'''
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Bienvenido - Sistema de Tareas</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }}
            .container {{
                background: white;
                border-radius: 20px;
                padding: 50px;
                max-width: 600px;
                text-align: center;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                animation: slideIn 0.5s ease-out;
            }}
            @keyframes slideIn {{
                from {{
                    opacity: 0;
                    transform: translateY(-30px);
                }}
                to {{
                    opacity: 1;
                    transform: translateY(0);
                }}
            }}
            .welcome-icon {{
                font-size: 80px;
                margin-bottom: 20px;
            }}
            h1 {{
                color: #667eea;
                margin-bottom: 10px;
                font-size: 2.5em;
            }}
            .username {{
                color: #764ba2;
                font-weight: bold;
                font-size: 1.3em;
            }}
            .message {{
                color: #666;
                margin: 20px 0;
                font-size: 1.1em;
                line-height: 1.6;
            }}
            .stats {{
                display: flex;
                justify-content: space-around;
                margin: 30px 0;
                gap: 20px;
            }}
            .stat-card {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 15px;
                flex: 1;
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }}
            .stat-number {{
                font-size: 2.5em;
                font-weight: bold;
                margin-bottom: 5px;
            }}
            .stat-label {{
                font-size: 0.9em;
                opacity: 0.9;
            }}
            .features {{
                background: #f8f9fa;
                padding: 25px;
                border-radius: 15px;
                margin-top: 30px;
                text-align: left;
            }}
            .features h3 {{
                color: #333;
                margin-bottom: 15px;
                text-align: center;
            }}
            .feature-item {{
                padding: 10px 0;
                color: #666;
                display: flex;
                align-items: center;
                gap: 10px;
            }}
            .feature-icon {{
                color: #667eea;
                font-size: 1.2em;
            }}
            .footer {{
                margin-top: 30px;
                padding-top: 20px;
                border-top: 2px solid #e9ecef;
                color: #999;
                font-size: 0.9em;
            }}
            .btn {{
                display: inline-block;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 12px 30px;
                border-radius: 25px;
                text-decoration: none;
                margin-top: 20px;
                font-weight: bold;
                transition: transform 0.3s ease;
            }}
            .btn:hover {{
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="welcome-icon">👋</div>
            <h1>¡Bienvenido!</h1>
            <p class="username">{usuario}</p>
            
            <p class="message">
                Has iniciado sesión exitosamente en el Sistema de Gestión de Tareas.
                Tu cuenta está activa y lista para usar.
            </p>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">{total_tasks}</div>
                    <div class="stat-label">Tareas Totales</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{completed_tasks}</div>
                    <div class="stat-label">Completadas</div>
                </div>
            </div>
            
            <div class="features">
                <h3>✨ Características del Sistema</h3>
                <div class="feature-item">
                    <span class="feature-icon">🔐</span>
                    <span>Autenticación segura con contraseñas hasheadas</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">💾</span>
                    <span>Persistencia de datos con SQLite</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">🚀</span>
                    <span>API REST completa y funcional</span>
                </div>
                <div class="feature-item">
                    <span class="feature-icon">📱</span>
                    <span>Interfaz responsive y moderna</span>
                </div>
            </div>
            
            <a href="/" class="btn">Volver al Inicio</a>
            
            <div class="footer">
                <p><strong>PFO 2:</strong> Sistema de Gestión de Tareas</p>
                <p>Sesión activa • ID: {user_id}</p>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)
# ============================================
# API ENDPOINTS PARA GESTIÓN DE TAREAS
# ============================================

@app.route('/api/tareas', methods=['GET'])
@login_required
def get_tareas():
    """
    Obtiene todas las tareas del usuario autenticado
    """
    try:
        user_id = session.get('user_id')
        usuario = session.get('usuario')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title, description, completed, created_at 
            FROM tasks 
            WHERE user_id = ? 
            ORDER BY created_at DESC
        ''', (user_id,))
        
        tasks = []
        for row in cursor.fetchall():
            tasks.append({
                'id': row['id'],
                'title': row['title'],
                'description': row['description'],
                'completed': bool(row['completed']),
                'created_at': row['created_at']
            })
        
        conn.close()
        
        return jsonify({
            'tareas': tasks,
            'usuario': usuario,
            'total': len(tasks)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error del servidor',
            'mensaje': str(e)
        }), 500

@app.route('/api/tareas', methods=['POST'])
@login_required
def create_tarea():
    """
    Crea una nueva tarea para el usuario autenticado
    """
    try:
        data = request.get_json()
        
        # Validación de datos
        if not data or 'title' not in data:
            return jsonify({
                'error': 'Datos incompletos',
                'mensaje': 'Se requiere el campo "title"'
            }), 400
        
        title = data['title'].strip()
        description = data.get('description', '').strip()
        user_id = session.get('user_id')
        
        # Validación de título
        if len(title) < 3:
            return jsonify({
                'error': 'Título inválido',
                'mensaje': 'El título debe tener al menos 3 caracteres'
            }), 400
        
        # Insertar en la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO tasks (user_id, title, description, completed)
            VALUES (?, ?, ?, 0)
        ''', (user_id, title, description))
        conn.commit()
        task_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'mensaje': 'Tarea creada exitosamente',
            'tarea': {
                'id': task_id,
                'title': title,
                'description': description,
                'completed': False
            }
        }), 201
        
    except Exception as e:
        return jsonify({
            'error': 'Error del servidor',
            'mensaje': str(e)
        }), 500

@app.route('/api/tareas/<int:task_id>', methods=['PUT'])
@login_required
def update_tarea(task_id):
    """
    Actualiza una tarea existente (título, descripción o estado)
    """
    try:
        data = request.get_json()
        user_id = session.get('user_id')
        
        # Verificar que la tarea pertenece al usuario
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ? AND user_id = ?', (task_id, user_id))
        task = cursor.fetchone()
        
        if not task:
            conn.close()
            return jsonify({
                'error': 'Tarea no encontrada',
                'mensaje': 'La tarea no existe o no tienes permiso para modificarla'
            }), 404
        
        # Actualizar campos
        title = data.get('title', task['title']).strip()
        description = data.get('description', task['description']).strip()
        completed = data.get('completed', task['completed'])
        
        cursor.execute('''
            UPDATE tasks 
            SET title = ?, description = ?, completed = ?
            WHERE id = ? AND user_id = ?
        ''', (title, description, completed, task_id, user_id))
        conn.commit()
        conn.close()
        
        return jsonify({
            'mensaje': 'Tarea actualizada exitosamente',
            'tarea': {
                'id': task_id,
                'title': title,
                'description': description,
                'completed': bool(completed)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error del servidor',
            'mensaje': str(e)
        }), 500

@app.route('/api/tareas/<int:task_id>', methods=['DELETE'])
@login_required
def delete_tarea(task_id):
    """
    Elimina una tarea del usuario autenticado
    """
    try:
        user_id = session.get('user_id')
        
        # Verificar que la tarea pertenece al usuario
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tasks WHERE id = ? AND user_id = ?', (task_id, user_id))
        task = cursor.fetchone()
        
        if not task:
            conn.close()
            return jsonify({
                'error': 'Tarea no encontrada',
                'mensaje': 'La tarea no existe o no tienes permiso para eliminarla'
            }), 404
        
        # Eliminar la tarea
        cursor.execute('DELETE FROM tasks WHERE id = ? AND user_id = ?', (task_id, user_id))
        conn.commit()
        conn.close()
        
        return jsonify({
            'mensaje': 'Tarea eliminada exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error del servidor',
            'mensaje': str(e)
        }), 500


@app.route('/status')
def status():
    """Endpoint para verificar el estado del servidor"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) as total FROM users')
    total_users = cursor.fetchone()['total']
    conn.close()
    
    return jsonify({
        'status': 'online',
        'mensaje': 'Servidor funcionando correctamente',
        'usuarios_registrados': total_users,
        'database': DATABASE,
        'timestamp': datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    # Inicializar la base de datos al arrancar
    print("=" * 50)
    print("🚀 Iniciando Sistema de Gestión de Tareas")
    print("=" * 50)
    
    if not os.path.exists(DATABASE):
        print("📦 Creando base de datos...")
    
    init_db()
    
    print("=" * 50)
    print("✓ Servidor listo en http://127.0.0.1:5000")
    print("=" * 50)
    print("\nEndpoints disponibles:")
    print("  • POST /registro - Registrar usuario")
    print("  • POST /login - Iniciar sesión")
    print("  • GET /tareas - Ver página de bienvenida")
    print("  • POST /logout - Cerrar sesión")
    print("  • GET /status - Estado del servidor")
    print("\nAPI de Tareas:")
    print("  • GET /api/tareas - Listar tareas del usuario")
    print("  • POST /api/tareas - Crear nueva tarea")
    print("  • PUT /api/tareas/<id> - Actualizar tarea")
    print("  • DELETE /api/tareas/<id> - Eliminar tarea")
    print("\n💡 Interfaz interactiva:")
    print("  • Abre app.html en tu navegador para usar la interfaz completa")
    print("=" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=5000)