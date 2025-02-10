import os
#FRAMEWORK
from flask import Flask
#es para poder leer las variables de entorno
from dotenv import load_dotenv
#esta funcion levanta la aplicacion de nuestro servidor

#importacion de modulo para crear la api-rest
from flask_restful import Api
#importacion de modulo para conectarse a una base de datos
from flask_sqlalchemy import SQLAlchemy
#importacion modulo jsonwebtokens
from flask_jwt_extended import JWTManager
#importacion modulo para trabajar envio mail
from flask_mail import Mail

api = Api()

db = SQLAlchemy()

jwt = JWTManager()

mailSender = Mail()


def create_app():
    app = Flask(__name__)

    load_dotenv()

    #config base de datos
    PATH = os.getenv("DATABASE_PATH")
    DB_NAME = os.getenv("DATABASE_NAME")

    if not os.path.exists(f'{PATH}{DB_NAME}'):
        os.chdir(f'{PATH}')
        file = os.open(f'{DB_NAME}', os.O_CREAT)

    app.config['SQLALHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{PATH}{DB_NAME}'
    db.init_app(app)
    import main.resources as resources

    api.add_resource(resources.ClientesResource, '/clientes')
    api.add_resource(resources.ClienteResource, '/cliente/<id>')
    api.add_resource(resources.UsuariosResource,'/usuarios')
    api.add_resource(resources.UsuarioResource,'/usuario/<id>')

    api.add_resource(resources.ComprasResource,'/compras')
    api.add_resource(resources.CompraResource,'/compra/<id>')

    api.add_resource(resources.ProductosResource,'/productos')
    api.add_resource(resources.ProductoResource,'/producto/<id>')
    import main.Controllers as controllers
    api.add_resource(resources.ProductosCompraResource,'/productos-compras') 
    api.add_resource(resources.ProductoCompraResource,'/producto-compra/<id>')

    api.add_resource(controllers.CompraController,'/compra-controller/<id>')
    api.add_resource(controllers.ComprasController,'/compras-controller')
    api.init_app(app)

    #Configurar JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES'))
    jwt.init_app(app)
    #BluePrint
    from main.Auth import routes
    app.register_blueprint(Auth.routes.auth)
    from main.Mail import functions
    app.register_blueprint(Mail.functions.mail)
    
    #configurar mail
    app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')

    mailSender.init_app(app)
    return app