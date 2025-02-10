from flask_restful import Resource
from main.Maps import Compra
from main.Services import CompraService
from flask import request

compra_schema = Compra()
compra_services = CompraService()


class CompraController(Resource):
    def get(self,id):
        compra = compra_services.obtener_compra_con_descuento(id)
        return compra_schema.dump(compra, many=False)


class ComprasController(Resource):
    def post(self):
        compra = compra_schema.load(request.get_json())
        return compra_schema.dump(compra_services.agregar_compra(compra), many=False)