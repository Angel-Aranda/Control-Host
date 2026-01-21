import os
import platform
from flask import flash

def power_action(action):
    action = action.lower()
    if action == "shutdown":
        shutdown()
    elif action == "restart":
        restart()
    elif action == "logout":
        logout()
    elif action == "suspend":
        suspend()

  
def shutdown():
    if platform.system() == 'Windows':
        # /s = Shutdown (apagar)
        # /f = Force (cierra programas a la fuerza)
        # /t 0 = Time 0 (lo hace inmediatamente, sin cuenta atrás)
        os.system("shutdown /s /f /t 0")
    else:
        # Linux (systemctl es el estándar moderno)
        os.system("systemctl poweroff")
        os.system("kill 1")
    flash("Apagando el equipo", "warning")

def restart():
    if platform.system() == 'Windows':
        # /r = Restart (reiniciar)
        os.system("shutdown /r /f /t 0")
    else:
        # Linux
        os.system("systemctl reboot")
    flash("Reinicio programado en 30 segundos", "warning")

def logout():
    if platform.system() == 'Windows':
        os.system("shutdown /l")
    else:
        # Intenta cerrar sesión educadamente (funciona en Ubuntu/GNOME)
        os.system("gnome-session-quit --no-prompt --force")

        # Obtenemos el usuario real (aunque uses sudo)
        usuario = os.environ.get('SUDO_USER') or os.environ.get('USER')
        
        # Matamos todos sus procesos (Cierra sesión sí o sí)
        if usuario and usuario != "root":
            os.system(f"pkill -KILL -u {usuario}")
    flash("Equipo bloqueado", "info")

def suspend():
    if platform.system() == 'Windows':
        # Truco clásico de Windows para suspender
        # Nota: Si tienes la "Hibernación" activada en Windows, esto podría hibernar en vez de suspender.
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
    
    else: # Linux
        # El estándar moderno (Ubuntu, Debian, Fedora...)
        # Normalmente no pide contraseña si estás en sesión gráfica
        os.system("systemctl suspend")
    flash("Equipo suspendido", "info")
