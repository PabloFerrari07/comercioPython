from .. import jwt
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def role_required(roles):
    def decorator(function):
        def wrapper(*args,**kwargs):
            #verificar que el jwt es correco
            verify_jwt_in_request()
            #obtener los claims(peticiones o valores o permitos) que estan dentro del JWT
            claims = get_jwt()
            
            #verificar que el rol sea permitido
            if claims['sub']['role'] in roles:
                return function(*args,**kwargs)
            else:
                return 'Rol not allowed', 403
        return wrapper
    return decorator


#Decoradores que ya trae el jwt pero los modificamos, redefinimos con los atributos que utiliza json web token
@jwt.user_identity_loader
def user_identity_lookup(usuario):
    return {
        'usuarioId': usuario.id,
        'role': usuario.role
    }

@jwt.additional_claims_loader
def add_claims_to_access_token(usuario):
    claims = {
        'id': usuario.id,
        'role': usuario.role,
        'email': usuario.email
    }
