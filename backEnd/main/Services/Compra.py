from main import CompraRepository

compra_repository = CompraRepository()  

class CompraService:
    def obtener_compra_con_descuento(self,id):
        compra = compra_repository.find_one(id)


    def agregar_compra(self,compra):
       compra = compra_repository.create(compra)    
       return compra