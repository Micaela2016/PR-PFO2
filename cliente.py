"""
Cliente de Consola para el Sistema de Gestión de Tareas
Interactúa con la API del servidor
"""

import requests
import json
import sys
from getpass import getpass

# Configuración
BASE_URL = "http://127.0.0.1:5000"
session = requests.Session()

# Colores para la terminal
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text):
    """Imprime un encabezado formateado"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text.center(60)}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'=' * 60}{Colors.RESET}\n")

def print_success(message):
    """Imprime mensaje de éxito"""
    print(f"{Colors.GREEN}✅ {message}{Colors.RESET}")

def print_error(message):
    """Imprime mensaje de error"""
    print(f"{Colors.RED}❌ {message}{Colors.RESET}")

def print_info(message):
    """Imprime información"""
    print(f"{Colors.YELLOW}ℹ️  {message}{Colors.RESET}")

def print_menu():
    """Muestra el menú principal"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}╔════════════════════════════════════════╗{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}║     SISTEMA DE GESTIÓN DE TAREAS      ║{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}╚════════════════════════════════════════╝{Colors.RESET}\n")
    print(f"{Colors.CYAN}1.{Colors.RESET} Registrar nuevo usuario")
    print(f"{Colors.CYAN}2.{Colors.RESET} Iniciar sesión")
    print(f"{Colors.CYAN}3.{Colors.RESET} Ver página de tareas")
    print(f"{Colors.CYAN}4.{Colors.RESET} Cerrar sesión")
    print(f"{Colors.CYAN}5.{Colors.RESET} Estado del servidor")
    print(f"{Colors.CYAN}0.{Colors.RESET} Salir")
    print()

def verificar_servidor():
    """Verifica que el servidor esté activo"""
    try:
        response = requests.get(f"{BASE_URL}/status", timeout=3)
        if response.status_code == 200:
            return True
        return False
    except:
        return False

def registrar_usuario():
    """Registra un nuevo usuario"""
    print_header("REGISTRO DE USUARIO")
    
    usuario = input(f"{Colors.CYAN}Usuario (mínimo 3 caracteres): {Colors.RESET}").strip()
    contraseña = getpass(f"{Colors.CYAN}Contraseña (mínimo 4 caracteres): {Colors.RESET}")
    
    if len(usuario) < 3:
        print_error("El usuario debe tener al menos 3 caracteres")
        return
    
    if len(contraseña) < 4:
        print_error("La contraseña debe tener al menos 4 caracteres")
        return
    
    data = {
        "usuario": usuario,
        "contraseña": contraseña
    }
    
    try:
        print_info("Registrando usuario...")
        response = session.post(
            f"{BASE_URL}/registro",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 201:
            result = response.json()
            print_success(f"Usuario '{usuario}' registrado exitosamente")
            print_info(f"ID de usuario: {result.get('id')}")
        elif response.status_code == 409:
            print_error("El usuario ya existe")
        elif response.status_code == 400:
            error = response.json()
            print_error(error.get('mensaje', 'Datos inválidos'))
        else:
            print_error(f"Error al registrar usuario (código {response.status_code})")
            
    except requests.exceptions.ConnectionError:
        print_error("No se puede conectar al servidor")
        print_info("Asegúrate de que el servidor esté ejecutándose")
    except Exception as e:
        print_error(f"Error: {e}")

def iniciar_sesion():
    """Inicia sesión con un usuario"""
    print_header("INICIO DE SESIÓN")
    
    usuario = input(f"{Colors.CYAN}Usuario: {Colors.RESET}").strip()
    contraseña = getpass(f"{Colors.CYAN}Contraseña: {Colors.RESET}")
    
    data = {
        "usuario": usuario,
        "contraseña": contraseña
    }
    
    try:
        print_info("Iniciando sesión...")
        response = session.post(
            f"{BASE_URL}/login",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print_success(f"¡Bienvenido, {usuario}!")
            print_info(f"ID de usuario: {result.get('id')}")
            return True
        elif response.status_code == 401:
            print_error("Usuario o contraseña incorrectos")
        elif response.status_code == 400:
            error = response.json()
            print_error(error.get('mensaje', 'Datos inválidos'))
        else:
            print_error(f"Error al iniciar sesión (código {response.status_code})")
            
    except requests.exceptions.ConnectionError:
        print_error("No se puede conectar al servidor")
    except Exception as e:
        print_error(f"Error: {e}")
    
    return False

def ver_tareas():
    """Accede a la página de tareas"""
    print_header("PÁGINA DE TAREAS")
    
    try:
        print_info("Accediendo a tareas...")
        response = session.get(f"{BASE_URL}/tareas")
        
        if response.status_code == 200:
            print_success("Acceso exitoso a la página de tareas")
            print_info("La página HTML se ha cargado correctamente")
            print_info(f"Tamaño de respuesta: {len(response.text)} caracteres")
            
            # Preguntar si quiere abrir en navegador
            abrir = input(f"\n{Colors.CYAN}¿Desea abrir la página en el navegador? (s/n): {Colors.RESET}").lower()
            if abrir == 's':
                import webbrowser
                webbrowser.open(f"{BASE_URL}/tareas")
                print_success("Página abierta en el navegador")
                
        elif response.status_code == 401:
            print_error("Debe iniciar sesión primero")
        else:
            print_error(f"Error al acceder a tareas (código {response.status_code})")
            
    except requests.exceptions.ConnectionError:
        print_error("No se puede conectar al servidor")
    except Exception as e:
        print_error(f"Error: {e}")

def cerrar_sesion():
    """Cierra la sesión actual"""
    print_header("CERRAR SESIÓN")
    
    try:
        print_info("Cerrando sesión...")
        response = session.post(f"{BASE_URL}/logout")
        
        if response.status_code == 200:
            result = response.json()
            print_success(result.get('mensaje', 'Sesión cerrada exitosamente'))
        elif response.status_code == 401:
            print_error("No hay sesión activa")
        else:
            print_error(f"Error al cerrar sesión (código {response.status_code})")
            
    except requests.exceptions.ConnectionError:
        print_error("No se puede conectar al servidor")
    except Exception as e:
        print_error(f"Error: {e}")

def estado_servidor():
    """Muestra el estado del servidor"""
    print_header("ESTADO DEL SERVIDOR")
    
    try:
        print_info("Consultando estado del servidor...")
        response = requests.get(f"{BASE_URL}/status", timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print_success("Servidor activo y funcionando")
            print(f"\n{Colors.CYAN}Información del servidor:{Colors.RESET}")
            print(f"  • Estado: {result.get('status')}")
            print(f"  • Usuarios registrados: {result.get('usuarios_registrados')}")
            print(f"  • Base de datos: {result.get('database')}")
            print(f"  • Timestamp: {result.get('timestamp')}")
        else:
            print_error(f"Servidor respondió con código {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print_error("No se puede conectar al servidor")
        print_info("Asegúrate de que el servidor esté ejecutándose en http://127.0.0.1:5000")
    except Exception as e:
        print_error(f"Error: {e}")

def main():
    """Función principal del cliente"""
    clear_screen()
    print_header("CLIENTE DE GESTIÓN DE TAREAS")
    
    # Verificar servidor al inicio
    print_info("Verificando conexión con el servidor...")
    if not verificar_servidor():
        print_error("No se puede conectar al servidor")
        print_info("Asegúrate de ejecutar: python servidor.py")
        sys.exit(1)
    
    print_success("Conexión establecida con el servidor")
    
    while True:
        print_menu()
        
        try:
            opcion = input(f"{Colors.CYAN}Seleccione una opción: {Colors.RESET}").strip()
            
            if opcion == '1':
                registrar_usuario()
            elif opcion == '2':
                iniciar_sesion()
            elif opcion == '3':
                ver_tareas()
            elif opcion == '4':
                cerrar_sesion()
            elif opcion == '5':
                estado_servidor()
            elif opcion == '0':
                print_info("Saliendo del cliente...")
                print_success("¡Hasta luego!")
                break
            else:
                print_error("Opción inválida")
            
            input(f"\n{Colors.YELLOW}Presione Enter para continuar...{Colors.RESET}")
            clear_screen()
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Operación cancelada{Colors.RESET}")
            print_success("¡Hasta luego!")
            break
        except Exception as e:
            print_error(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()
