from wtforms import Form, IntegerField, StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, NumberRange,ValidationError

class ComputerForm(Form):
    pc_id = StringField("ID", validators=[DataRequired()], description="ID del equipo")
    username = StringField("Usuario", validators=[DataRequired()], description="Juan")
    hostname = StringField("Nombre de Host", validators=[DataRequired()], description="PC-01")
    platform = SelectField("Plataforma", choices=[('Windows', 'Windows'), ('Linux', 'Linux'), ('MacOS', 'MacOS')], validators=[DataRequired()],  description="Selecciona la plataforma")
    os = StringField("Sistema Operativo", validators=[DataRequired()], description="Ubuntu 22.04")
    ram = IntegerField("RAM (GB)", validators=[DataRequired(), NumberRange(min=1)], description="24")
    cpu_cores = IntegerField("Núcleos CPU", validators=[DataRequired(), NumberRange(min=1)], description="8")
    cpu_architecture = StringField("Arquitectura CPU", validators=[DataRequired()], description="x86_64")
    cpu_name = StringField("Nombre CPU", validators=[DataRequired()], description="Ryzen 9 9900X")
    submit = SubmitField("Guardar")

class BlockWebsiteForm(Form):
    web_url = StringField('URL del sitio web', validators=[DataRequired()])
    add_button = SubmitField('Añadir')
    remove_button = SubmitField('Eliminar')
    
    def validate_web_url(form, field):
        valor = field.data.strip()
        
        # Verificar que no tenga protocolo
        if 'http://' in valor or 'https://' in valor:
            raise ValidationError('No incluyas http:// o https://')
        
        # Verificar que no tenga www.
        if valor.startswith('www.'):
            raise ValidationError('No incluyas www.')
        
        # Verificar que no tenga barras
        if '/' in valor:
            raise ValidationError('No incluyas barras (/). Solo el dominio')

        if ' ' in valor:
            raise ValidationError('No incluyas espacios.')
        
        # Verificar que tenga al menos un punto
        if '.' not in valor:
            raise ValidationError('Ingresa un dominio válido (ejemplo: facebook.com)')

