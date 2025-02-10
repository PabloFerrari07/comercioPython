from .. import db
from main.Models import CompraModel

class CompraRepository:
    __modelo = CompraModel

    @property
    def modelo(self):
        return self.modelo
    
    def find_one(self, id):
        object = db.session.query(self.modelo).get(id)
        return object
    
    def find_all(self):
        objects = db.session.query(self.modelo).all()
        return objects
      
    def create(self,object):
        db.session.add(object)
        db.session.commit()
        return object
    
    def update(self,object):
      return  self.create(object)
    
    def delete(self,id):
        object = self.find_one(id)
        db.session.delete(object)
        db.session.commit()
        return object