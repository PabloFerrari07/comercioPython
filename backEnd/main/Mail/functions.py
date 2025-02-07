from .. import mailSender, db
from flask import current_app, render_template, Blueprint
from flask_mail import Message
from smtplib import SMTPException
from main.Models import UsuarioModel, ProductoModel
from main.Auth.decorators import role_required

def send_mail(to,subject,template,**kwargs):
    msg = Message(subject, sender=current_app.config['FLASKY_MAIL_SENDER'], recipients=to)
    try:
        msg.body = render_template(f'{template}.txt',**kwargs)
        mailSender.send(msg)
    except SMTPException as error:
        return 'Mail deliver failed'
    
    return True


mail = Blueprint('mail',__name__,url_prefix='/mail')


@mail.route('/newsletter', methods=["POST"])
@role_required(roles=["admin"])
def newsletter():
    usuarios = db.session.query(UsuarioModel).filter(UsuarioModel.role == 'cliente').all()
    productos = db.session.query(ProductoModel).all()
    try:
        for usuario in usuarios:
            send_mail([usuario.email],"Productos en venta","newsletter",usuario = usuario, producto = [productos.nombre for producto in productos])

    except SMTPException as error:
        return 'mail deliver failed'
    
    return 'mail sender',200