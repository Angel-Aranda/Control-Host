import os

from flask import Flask, flash, redirect, render_template, request, url_for, Response
from flask_security import Security, SQLAlchemyUserDatastore, auth_required, current_user, roles_required
import base64

from models import *
from forms import *

from controls.computer.apagado import power_action
from controls.computer.computer_data_control import block_web_host, pc_hardware_id, info
from controls.computer.monitor import get_screenshot, video_generator

# Crea la carpeta db si no existe
if not os.path.exists(f"{os.path.abspath(os.curdir)}/db/"):
    os.makedirs(f"{os.path.abspath(os.curdir)}/db/")

Ruta404 = '404.html'
Ruta403 = '403.html'

docker = str(pc_hardware_id).lower().endswith("docker")

app = Flask(__name__)
app.config.update(
    SECRET_KEY= "be26337fa9a6f46d0b1fe90ee85cd17d296e7ebdf10c321df8bf7fb465f17a2d", # Se obtienen valores seguros y aleatorios del paquete secrets, con secrets.token_hex(32)
    SECURITY_PASSWORD_SALT= "b85c52cdd61f71867f69c435ba8e4b4ea187afca52baedb55d9d0387e04735bd",
    SQLALCHEMY_DATABASE_URI= f"sqlite:///{os.path.abspath(os.curdir)}/db/app.db",
    WTF_CSRF_ENABLED = False
)
# Esta linea sirve para indicar que los usuarios se pueden registrar y la de debajo de esta es enlace a Register que estaria en el header.html
#SECURITY_REGISTERABLE=True,
# <a href="{{ url_for('security.register') }}" class="btn btn-primary">Registrar</a>

db.init_app(app)

# https://flask-security-too.readthedocs.io/en/latest/quickstart.html
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Asignamos una pagina por defecto para el error 404 (Pagina no encontrada)
@app.errorhandler(404)
def not_found(e):
    return render_template(Ruta404), 404

# Asignamos una pagina por defecto para el error 403 (Falta de permisos)
@app.errorhandler(403)
def forbidden(e):
    return render_template(Ruta403), 403

@app.get("/")
def index():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return render_template("index.html")

@app.route("/dashboard", methods=["GET", "POST"])
@auth_required()
def dashboard():
    total_computers = Computer.query.count()

    # Solamente muestra el total de usuarios si tienes el rol de admin
    if current_user.has_role('admin'):
        total_users = User.query.count()
    else:
        total_users = None
    return render_template("dashboard.html", total_computers = total_computers, total_users = total_users)

@app.get("/computers")
@auth_required()
def computers_area():
    # Verificar primero si el equipo actual ya está en la BD
    computer = Computer.query.get(pc_hardware_id)

    # Solo obtener información si NO está en la BD
    if not computer:
        # Guardar en BD
        computer = Computer(
            pc_id=pc_hardware_id,
            cpu_cores=info["cpu_count"],
            cpu_name=info["cpu_name"],
            platform=info["platform"],
            os=info["os"],
            ram=info["ram_memory"],
            cpu_architecture=info["cpu_architecture"],
            hostname=info["hostname"],
            username=info["user"],
            docker=docker
        )

        db.session.add(computer)
        db.session.commit()

    # Se guarda en una lista, para que en caso de haber mas equipos y estar conectados (actualmente imposible), obtenga una captura de pantalla de cada uno de ellos
    imagenes = {}
        # Creamos una restricción para compatibilidad con contenedores docker (que no tienen interfaz grafica y da error cuando intentan capturar pantalla)
    if not docker:
        imagenes[pc_hardware_id] = get_screenshot()
    else:
        imagenes[pc_hardware_id] = None
        

    # Filtros
    hostname = request.args.get("hostname", "")
    os_select = request.args.get("os", "")
    platform_select = request.args.get("platform", "")
    ram_min = request.args.get("ram_min", "")
    core_min = request.args.get("core_min","")

    if ram_min:
        ram_min = int(ram_min)
    else: ram_min = None

    if core_min:
        core_min = int(core_min)
    else:
        core_min = None

    query = Computer.query

    if hostname:
        query = query.filter(Computer.hostname.ilike(f"%{hostname}%"))

    if os_select:
        query = query.filter(Computer.os == os_select)

    if platform_select:
        query = query.filter(Computer.platform == platform_select)

    if ram_min is not None:
        query = query.filter(Computer.ram >= ram_min)

    if core_min is not None:
        query = query.filter(Computer.cpu_cores >= core_min)

    computers = query.all()  # Ejecuta la consulta y obtiene los equipos

    # Lista de sistemas operativos y plataformas para el dropdown
    os_options = []
    platform_options = []
    for compu in Computer.query:
        if compu.os not in os_options:
            os_options.append(compu.os)
        if compu.platform not in platform_options:
            platform_options.append(compu.platform)

    return render_template("computers.html", computers=computers, os_options=os_options, platform_options=platform_options, images=imagenes)


@app.route("/computers/new", methods=["GET", "POST"])
@roles_required("admin")
def computer_new():
    form = ComputerForm(request.form)
    if request.method == 'POST':
        if form.validate():
            pc_id_val = str(form.pc_id.data)
            exists = Computer.query.get(pc_id_val)
            if exists:
                flash("Ese equipo ya existe.", "warning")
            else:

                computer = Computer(
                    pc_id=pc_id_val,
                    username=form.username.data,
                    hostname=form.hostname.data,
                    platform=form.platform.data,
                    os=form.os.data,
                    ram=form.ram.data,
                    cpu_cores=form.cpu_cores.data,
                    cpu_architecture=form.cpu_architecture.data,
                    cpu_name=form.cpu_name.data,
                )
                db.session.add(computer)
                db.session.commit()
                flash("Equipo creado correctamente", "success")
                return redirect(url_for("computers_area"))
    return render_template("computer_form.html", form=form, title="Nuevo Equipo")

@app.route(f"/computer/edit/<pc_id>", methods=['GET', 'POST'])
@roles_required("admin")
def computer_edit(pc_id):
    computer = Computer.query.get(pc_id)
    if not computer:
        return render_template(Ruta404, error=f"No existe ningún ordenador con id {pc_id}"), 404
    form = ComputerForm(request.form, obj=computer)
    if request.method == 'POST':
        if form.validate():
            pc_id_val = str(form.pc_id.data)
            if pc_id_val != pc_id:
                flash("No puedes cambiar el ID del equipo", "warning")
                return render_template('computer_form.html', form=form)
                        
            computer.username = form.username.data
            computer.hostname = form.hostname.data
            computer.platform = form.platform.data
            computer.os = form.os.data
            computer.ram = form.ram.data
            computer.cpu_cores = form.cpu_cores.data
            computer.cpu_architecture = form.cpu_architecture.data
            computer.cpu_name = form.cpu_name.data
            
            db.session.commit()
            flash("Equipo actualizado correctamente", "success")
            return redirect(url_for('computers_area'))
    computer_pc_id = {"pc_id":pc_id, "username":computer.username} # Pasamos solamente el pc_id y username para que se muestren los botones de control del equipo en el header además del nombre de usuario
    
    return render_template('computer_form.html', form=form, title="Editar equipo", computer=computer_pc_id)

@app.route(f"/computer/delete/<pc_id>", methods=['GET', 'POST'])
@roles_required("admin")
def computer_delete(pc_id):
    computer = Computer.query.get(pc_id)
    if request.method == "GET":
        if computer:
            return render_template('computer_delete_confirm.html', pc_id=computer.pc_id)
        else:
            return render_template(Ruta404, error=f"No existe ningún ordenador con id {pc_id}"), 404
    else:
        if computer:
            action = request.form.get('action')
            if action == 'confirm':
                db.session.delete(computer)
                db.session.commit()
                flash("Equipo eliminado correctamente", "success")
            else:
                flash("Operación cancelada", "info")
    return redirect(url_for('computers_area'))
    
@app.route(f"/computer/view/<pc_id>", methods=['GET', 'POST'])
@roles_required("admin")
def computer_view(pc_id):
    # Verificar primero si el equipo actual ya está en la BD
    computer = Computer.query.get(pc_id)
    if not computer or pc_id != pc_hardware_id:
        return render_template(Ruta404, error=f"No existe ningún ordenador con id {pc_id}"), 404
    
    if request.method == 'GET':
        return render_template('computer_view.html', computer=computer)
    else:
        action = request.form.get('action')
        if computer.docker:
            # Validar que la acción sea válida
            valid_actions = ['shutdown']
        else:
            valid_actions = ['shutdown', 'restart', 'logout', 'suspend']

        if not action or action not in valid_actions:
            flash("Acción no válida", "danger")
            return redirect(url_for('computer_view',pc_id=pc_id))
        
        # Verificar permisos (solo admin puede ejecutar acciones)
        if not current_user.has_role("admin"):
            flash("No tienes permisos para ejecutar esta acción", "danger")
            return redirect(url_for('computer_view', pc_id=pc_id))
        
        power_action(action)
    
        return redirect(url_for('computer_view', pc_id=pc_id))
        

@app.route('/computer/video/<pc_id>')
@roles_required("admin")
def video_src(pc_id):
    if pc_id != pc_hardware_id:
        return render_template(Ruta404, error=f"El ordenador con id {pc_id} está apagado o fuera de línea"), 404
    # Esta ruta actúa como un archivo de video infinito
    if not docker:
        return Response(video_generator(),mimetype='multipart/x-mixed-replace; boundary=frame')
    else: 
        image_path = os.path.join(app.root_path, 'static', 'images', 'no-image.jpg')
        with open(image_path, 'rb') as f:
            img_bytes = f.read()
        return Response(img_bytes, mimetype='image/jpeg')

@app.route(f'/computer/blocked_webs/<pc_id>', methods=['GET', 'POST'])
@auth_required()
def blocked_webs(pc_id):
    computer = Computer.query.get(pc_id)
    if not computer:
        return render_template(Ruta404, error=f"No existe ningún ordenador con id {pc_id}"), 404
    
    # Crear el formulario con formdata si es POST
    if request.method == 'POST':
        form = BlockWebsiteForm(formdata=request.form)
    else:
        form = BlockWebsiteForm()
    
    if request.method == 'POST':
        # Validar el formulario primero
        if not form.validate():
            # Si falla la validación, mostrar los errores
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"Error en {field}: {error}", "danger")

        else:
            url = form.web_url.data.strip().lower()
            
            if 'add_button' in request.form:
                # Añadir sitio web
                existe = Blocked_websites.query.filter_by(
                    pc_id=computer.pc_id,
                    url=url
                ).first()
                
                if existe:
                    flash(f"El sitio {url} ya está bloqueado", "warning")
                else:
                    nuevo = Blocked_websites(pc_id=computer.pc_id, url=url)
                    db.session.add(nuevo)
                    db.session.commit()
                    block_web_host(computer.pc_id)
                    flash(f"Sitio {url} bloqueado correctamente", "success")
            
            elif 'remove_button' in request.form:
                if not current_user.has_role('admin'):
                    flash("No tienes permisos para borrar páginas web", "danger")
                    return redirect(url_for('blocked_webs', pc_id=pc_id))

                # Comprobamos si existe el sitio web
                site = Blocked_websites.query.filter_by(
                    pc_id=computer.pc_id,
                    url=url
                ).first()
                
                if site:
                    # Borramos el sitio web
                    db.session.delete(site)
                    db.session.commit()
                    block_web_host(computer.pc_id)
                    flash(f"Sitio {url} desbloqueado correctamente", "success")
                else:
                    flash(f"El sitio {url} no estaba bloqueado", "warning")
            
            return redirect(url_for('blocked_webs', pc_id=pc_id))
            
    suggest_sites = [
        {'url': 'amazon.com', 'name': 'Amazon'},
        {'url': 'facebook.com', 'name': 'Facebook'},
        {'url': 'hbo.com', 'name': 'HBO'},
        {'url': 'instagram.com', 'name': 'Instagram'},
        {'url': 'netflix.com', 'name': 'Netflix'},
    ]

    pc_blocked_sites = []
    for site in computer.blocked_websites:
        pc_blocked_sites.append(site.url)
        
    return render_template('computer_block_websites.html', form=form, suggest_sites=suggest_sites, pc_blocked_sites=pc_blocked_sites, computer=computer)
