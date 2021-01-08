from servicios.weblogging import Applogging
import json
from modelos.usuario import Usuario

# Para enterder esto: https://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance
class Api:

    def __init__(self, servicio_db):
        self.__servicio_db = servicio_db
        self.__sesion = servicio_db.sesion

    def modificar_usuario(self, id, nombre, email, nombre_completo, numero_telefono, direccion):
        self.__sesion = self.__servicio_db.crear_nueva_conexion_si_ha_caducado()
        self.__sesion.query(Usuario).filter_by(id = id).update({
            "nombre" : nombre,
            "email" : email,
            "nombre_completo" : nombre_completo,
            "numero_telefono" : numero_telefono,
            "direccion" : direccion
        })
        self.__sesion.commit()

    def obtener_ultimas_mediciones_accel(self):
        print()

    def obtener_ultimas_mediciones_temperatura_externa(self):
        print()
