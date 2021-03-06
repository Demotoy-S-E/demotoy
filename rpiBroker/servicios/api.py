from servicios.weblogging import Applogging
import json
from modelos.usuario import Usuario
from modelos.medicionAccelerometro import MAcelerometro
from modelos.medicionTempemperaturaExterna import MTemperaturaExterna
from modelos.vista.updateModeloUsuario import UpdateModeloUsuario

class Api:

    def __init__(self, servicio_db):
        self.__servicio_db = servicio_db
        self.__sesion = servicio_db.sesion

    def modificar_usuario(self, id: int, modelo_actualizar_usuario: UpdateModeloUsuario):
        self.__sesion = self.__servicio_db.crear_nueva_conexion_si_ha_caducado()
        self.__sesion.query(Usuario).filter_by(id = id).update({
            Usuario.nombre : modelo_actualizar_usuario.nombre,
            "email" : modelo_actualizar_usuario.email,
            "nombre_completo" : modelo_actualizar_usuario.nombre_completo,
            "numero_telefono" : modelo_actualizar_usuario.numero_telefono,
            "direccion" : modelo_actualizar_usuario.direccion
        })
        self.__sesion.commit()

    def obtener_ultimas_mediciones_accel(self):
        self.__sesion = self.__servicio_db.crear_nueva_conexion_si_ha_caducado()
        mediciones = self.__sesion.query(MAcelerometro).filter_by().all()
        self.__sesion.commit()
        return mediciones

    def obtener_ultimas_mediciones_temperatura_externa(self):
        self.__sesion = self.__servicio_db.crear_nueva_conexion_si_ha_caducado()
        mediciones = self.__sesion.query(MTemperaturaExterna).filter_by().all()
        self.__sesion.commit()
        return mediciones