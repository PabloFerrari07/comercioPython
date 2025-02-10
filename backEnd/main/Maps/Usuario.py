from marshmallow import Schema, fields, post_load,post_dump
from main.Models import UsuarioModel

class UsuarioSchema(Schema):
    id = fields.Integer(dump_only=True) 
    nombre = fields.String(required=True)
    apellido = fields.String(required=True)
    email = fields.String(required=True)
    password = fields.String(required=True)
    role = fields.String(required=True)
    telefono = fields.String(required=True) 
    fecha_registro = fields.DateTime(Required=False)

    @post_load
    def create_usuario(self,data):
        return UsuarioModel(**data)
    
    SKIP_VALUES = ['password']

    @post_dump
    def remove_skip_values(self,data):
        return {
            key: value for key, value in data.items()
            if value not in self.SKIP_VALUES
        }