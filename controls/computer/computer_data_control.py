import platform, subprocess, os
from flask import flash
from models import Blocked_websites
from cpuinfo import get_cpu_info
import psutil

def get_pc_id():
    sistema = platform.system()
    if sistema == "Linux":

        # Opción 1: Para contenedores Docker
        try:
            result = subprocess.run(
                ['cat', '/docker/dmi/id/product_uuid'],
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            pass
        if not result:
            # Intentar leer UUID con permisos elevados usando pkexec o sudo
            try:
                # Opción 2: pkexec (GUI password prompt)
                result = subprocess.run(
                    ['pkexec', 'cat', '/sys/class/dmi/id/product_uuid'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip()
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
        if not result:
            # Opción 3: sudo (CLI password prompt)
            try:
                result = subprocess.run(
                    ['sudo', 'cat', '/sys/class/dmi/id/product_uuid'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0 and result.stdout.strip():
                    return result.stdout.strip()
            except subprocess.TimeoutExpired:
                pass

    elif sistema == "Windows":
        try:
            cmd = 'powershell -Command "(Get-CimInstance -Class Win32_ComputerSystemProduct).UUID"'
            uuid = os.popen(cmd).read().strip()
            if not uuid or "Access denied" in uuid:
                raise print("ERROR: Ejecuta el script como administrador")
            return uuid
        except Exception:
            return f"ERROR DE SISTEMA: {str(Exception)}"
    else:
        return "SISTEMA NO SOPORTADO"


def get_pc_info():
    info_cpu = get_cpu_info()
    ram_info = psutil.virtual_memory()
    pc_hardware_id = get_pc_id()
    info = {
            "pc_id": pc_hardware_id,
            "cpu_count": os.cpu_count(),
            "cpu_name": info_cpu["brand_raw"],
            "platform": platform.system(),
            "ram_memory": round(ram_info.total / (1024 ** 3) + 0.5, 0),
            "cpu_architecture": platform.machine(),
            "hostname": os.getenv("HOSTNAME") or platform.node(),
            "user": os.getenv("USER") or os.getenv("USERNAME"),
        }
    if platform.system() == "Linux":
        import distro
        info["os"] = f"{distro.name()} {distro.version()}"
    else:
        info["os"] = f"{platform.system()} {platform.release()}"

    return info

def block_web_host(pc_id):
    # Añadimos una verificación para que se edite solamente el equipo con ese pc_id
    if pc_id != get_pc_id():
        return False
    if platform.system() == 'Windows':
        hosts_file = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
    else:
        hosts_file = '/etc/hosts'
    
    redirect_ip = '0.0.0.0'
    marker = '# Flask-blocked (IF YOU EDIT THIS FILE PUT UP OF THIS COMMENT)'
    blocked = Blocked_websites.query.filter_by(pc_id=pc_id)
    try:
        # Leer todas las líneas del archivo
        with open(hosts_file, 'r') as file:
            lines = file.readlines()
        
        # Separar: lo que viene antes del marker y lo que viene después
        before_marker = []
        after_marker = []
        marker_found = False
        
        for line in lines:
            # Si encontramos el marker, todo lo siguiente va después
            if marker in line:
                marker_found = True
                before_marker.append(line)
            elif not marker_found:
                before_marker.append(line)

        # Si no existe el marker, agregarlo
        if not marker_found:
            before_marker.append(f'\n{marker}\n')
        
        # Construir el nuevo contenido
        new_lines = before_marker + after_marker
        
        if blocked:
            for block_site in blocked:
                new_lines.append(f'{redirect_ip} {block_site.url}\n')
                new_lines.append(f'{redirect_ip} www.{block_site.url}\n')
            
        # Escribir el archivo
        with open(hosts_file, 'w') as file:
            file.writelines(new_lines)
        
        return True
    except PermissionError:
        flash('Error: Sin permisos para modificar el archivo hosts, por favor inicie Flask en una terminal como Administrador', 'danger')
        return False

# Lo ejecutamos directamente para evitar repeticiones
pc_hardware_id = get_pc_id()
info = get_pc_info()