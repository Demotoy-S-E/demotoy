from sqlalchemy import Column, Integer, String, LargeBinary
from servicios.mysqlDB import Base
from sqlalchemy_utils import EmailType, PasswordType
from fernet import Fernet

class Usuario(Base):
    
    def __init__(self, nombre, email, contrasenia, nombre_completo, numero_telefono, direccion):
        self.nombre = nombre
        self.email = email
        self.nombre_completo = nombre_completo
        self.numero_telefono = numero_telefono
        self.direccion = direccion
        self.__clave = None
        self.__token = None
        self.__generar_clave_token(contrasenia)

    def get_contrasenia(self):
        contrasenia_desencriptada = self.__decrypt(self.__token, self.__clave)
        contrasenia_desencriptada = contrasenia_desencriptada.decode("utf-8")
        return contrasenia_desencriptada

    def __generar_clave_token(self, contrasenia):
        self.__clave = Fernet.generate_key()
        self.__clave.decode()
        self.__token = self.__encrypt(contrasenia.encode(), self.__clave)

    def __encrypt(self, message: bytes, key: bytes) -> bytes:
        return Fernet(key).encrypt(message)

    def __decrypt(self, token: bytes, key: bytes) -> bytes:
        return Fernet(key).decrypt(token)
  
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key = True, index = True, nullable = False)
    nombre = Column(String(15), index = True, nullable = False)
    email = Column(EmailType)
    __clave = Column(LargeBinary(2048), nullable = False)
    __token = Column(LargeBinary(2048), nullable = False)
    nombre_completo = Column(String(20), index = True, nullable = True)
    numero_telefono = Column(String(9), index = True, nullable = False)
    direccion = Column(String(20), index = True, nullable = False)