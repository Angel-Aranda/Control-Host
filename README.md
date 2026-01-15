# Control Host
## Índice
>[Explicación del proyecto](#proyect-explanation)
>
>>[Base de datos del proyecto](#proyect-db)
>>
>>[Rutas del proyecto](#proyect-routes)
>>
>[Inciciación del proyecto](#proyect-run)
>
>>[Requisitos del proyecto](#proyect-requirements)
>>
>>[Ejecutar el proyecto](#proyect-start)
>
>[Caracteristicas del proyecto](#proyect-characteristics)
>
>>[Base de datos del proyecto](#proyect-db)
>>
>>[Rutas del proyecto](#proyect-routes)
>>
>>>[Comunes](#proyect-comun-routes)
>>>
>>>[Usuarios autenticados](#proyect-authenticated-routes)
>>>
>>>[Administradores](#proyect-admin-routes)

---

<h3 id="proyect-explanation">Explicación del proyecto</h3>

Este proyecto sirve para controlar la alimentación del equipo,visualizarlo en tiempo real y bloquear el acceso a paginas web, todo a traves de una aplicación web desarrollada usando **Python** junto con **Flask**.

Es compatible con Windows y Linux, ha sido probado en los siguientes equipos:

- Windows 11
- Ubuntu 22.04 (Xorg)


En Linux tendremos que usar Xorg.

Esto es importante porque, en Ubuntu 22.04, si se utiliza el servidor gráfico por defecto (Wayland), la funcionalidad de captura de pantalla no funciona correctamente: la aplicación no puede acceder al contenido de la pantalla por restricciones de seguridad de Wayland.

ATENCIÓN : Tanto en Windows como en Linux hay que ejecutar python con permisos de administrador, en caso contrario no tendrá permisos para cambiar el archivo hosts y por lo tanto la función de bloquear aplicaciones webs no funcionará.

---

<h3 id="proyect-run">Iniciación del proyecto</h3>

<h4 id="proyect-requirements">Requisitos del proyecto</h4>

Como primer paso vamos a clonar el proyecto en nuestra máquina con el comando: 

`git clone https://github.com/Angel-Aranda/Control-Host.git `

Para Windows ejecutaremos el siguiente comando:

` pip install -r requirements-windows.txt  `

Para Linux ejecutaremos el siguiente comando:

` pip install - requirements-linux.txt`

Como último requisito tendremos que ejecutar el siguiente comando para crear la base de datos del proyecto:

` python manage.py`

Este comando creará los roles y usuarios por defecto

- Roles:
    - admin: Usado para el administrador
    - user: Rol por defecto de los usuarios
- Usuarios:
    - admin@demo.com: Tendrá el rol de admin
    - user@demo.com: Tendrá el rol de usuario
    - Contraseña: password

<h4 id="proyect-start">Ejecutar el proyecto</h4>

Para ejecutar el proyecto usaremos:

` flask --app app run `

Para ejecutar en Windows como permisos de administrador abrimos cmd con permisos de Administrador y una vez dentro de la carpeta del proyecto ejecutamos:

` flask --app app run `

Para ejecutar en Linux con permisos de super usuario ejecutamos el siguiente comando (en caso de tenerlo en un entorno virtual):

` sudo venv/bin/python -m flask --app app run `

Si queremos que salga de localhost podemos usar el parametro ***--host 0.0.0.0***. De esta forma la aplicación empieza a ser más funcional pudiendo bloquear aplicaciones web, ver en tiempo real el ordenador y apagar el ordenador a traves de nuestro dispositivo movil.

---

<h3 id="proyect-characteristics">Características del proyecto</h3>

<h4 id="proyect-db">Base de datos del proyecto</h4>

Se usará una base de datos en sqlite, en esta habrá 5 tablas:
    - user: almacena usuarios, es creada y mantenida por el paquete flask_security
    - role: almacena los roles, es creada y mantenida por el paquete flask_security
    - roles_user: hace de tabla intermedia entre user y role, sirve para asignar roles a los usuarios, creada también por flask_security
    - computer: almacena información de los ordenadores, tiene como clave primaria el uuid
    - blocked_websites: almacena la url de la página web y el id del ordenador que la tiene bloqueada

<h4 id="proyect-routes">Rutas del proyecto</h4>

<h5 id="proyect-comun-routes">Comunes</h5>

- index (/)
    - Muestra la página inicial que contiene información sobre Control Host

<h5 id="proyect-authenticated-routes">Usuarios autenticados</h5>

- dashboard (/dashboard)
    - Muestra información como equipos totales, el rol del usuario, acciones rápidas, etc.
- computers (/computers)
    - Muestra información sobre los equipos.
- blocked_webs (/computer/blocked_webs/)
    - Muestra el listado de páginas web bloqueadas (los que tienen rol usuario tan solo podrán añadir páginas)

<h5 id="proyect-admin-routes">Administradores</h5>

- computer_new (/computer/new)
    - Permite añadir nuevos equipos
- computer_edit (/computer/edit/)
    - Permite editar los equipos ya existentes
- computer_delete (/computer/delete/)
    - Sirve para eliminar equipos
- computer_view (/computer/view/)
    - Permite ver la pantalla en tiempo real y controlar la alimentación del equipo
- video_src (/computer/video)
    - Permite ver la pantalla en tiempo real a pantalla completa

---