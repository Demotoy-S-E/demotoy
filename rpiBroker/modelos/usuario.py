from sqlalchemy import Column, Integer, String
from servicios.mysqlDB import Base

class Usuario(Base):
    
    def __init__(self, nombre, email, contrasenia):
        self.nombre = nombre
        self.email = email
        self.contrasenia = contrasenia
    
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key = True, index = True, nullable = False)
    nombre = Column(String(15), index = True, nullable = False)
    email = Column(String(25), index = True, unique = True)
    contrasenia = Column(String(15), index = True, nullable = False)



    