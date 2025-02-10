from marshmallow import Schema, fields, post_load,post_dump
from main.Models import CompraModel
from .Usuario import UsuarioSchema   


class CompraSchema(Schema):
    id = fields.Integer(dump_only=True) 
    fecha_compra = fields.DateTime(required=False)
    usuarioId = fields.Integer(required=True)
    usuario = fields.Nested(UsuarioSchema)   

    @post_load
    def create_compra(self,data):
        return CompraModel(**data)
    

    SKIP_VALUE = ['usuarioId']

    @post_dump
    def remove_skip_values(self,data):
        return{
            key: value for key, value in data.items()
            if value not in self.SKIP_VALUE 
        }