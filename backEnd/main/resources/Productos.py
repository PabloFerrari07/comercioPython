from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.Models import ProductoModel
from main.Auth.decorators import role_required
class Producto(Resource):
    #OBTENER
    def get(self,id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        #select * FROM producto WHERE producto.id = <id>;
        try:
            return producto.to_json()
        except:
            return 'No encontrado',404
    #EDITAR
    @role_required(roles=["admin"])
    def put(self, id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(producto, key, value)
        try:
            db.session.add(producto)
            db.session.commit()
            return producto.to_json(),201
        except:
            return '',404
    #ELIMINAR
    @role_required(roles=["admin"])
    def delete(self,id):
        producto = db.session.query(ProductoModel).get_or_404(id)
        try:
            db.session.delete(producto)
            db.session.commit()
        except:
            return '',404



class Productos(Resource):

    def get(self):
        page = 1
        per_page = 5
        productos = db.session.query(ProductoModel)
        
        if request.get_json():
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    page = int(value)
                elif key == 'per_page':
                    per_page = int(value)

        try:
            productos = productos.paginate(page=page, per_page=per_page, error_out=False)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

        return jsonify({
            'productos': [producto.to_json() for producto in productos.items],
            'total': productos.total,
            'pages': productos.pages,
            'page': page
        })

        #SELECT * FROM productos
   
    #CREAR
    @role_required(roles=["admin"])
    def post(self):
        producto = ProductoModel.from_json(request.get_json())
        db.session.add(producto)
        db.session.commit()
        return producto.to_json(),201
