from comun.singleton import Singleton
from sqlalchemy import exists
from servicios.weblogging import Applogging
from modelos.usuario import Usuario
import time 

class Autenticacion(metaclass=Singleton):

    def __init__(self, servicio_db):
        self.__autenticacion_log = Applogging("Autenticacion")
        self.servicio_db = servicio_db
        self.__sesion = servicio_db.sesion
        self.usuario_autenticado = False
        self.ultima_autenticacion = None
        self.usuario = None

    def crear_usuario(self, nombre_form, email_form, contrasenia_form, nombre_completo_form, numero_form, direccion_form) -> bool:
        try:
            self.__sesion = self.servicio_db.crear_nueva_conexion_si_ha_caducado()
            if (self.__sesion.query(exists().where(Usuario.nombre == nombre_form)).scalar()):
                self.__autenticacion_log.warning_log(f"El usuario con nombre {nombre_form} ya existe")
                return False
            else:
                nuevo_usuario = Usuario(
                    nombre = nombre_form, 
                    email = email_form, 
                    contrasenia = contrasenia_form,
                    nombre_completo = nombre_completo_form,
                    numero_telefono = numero_form,
                    direccion = direccion_form)
                self.__sesion.add(nuevo_usuario)
                self.__sesion.commit()
                return True
        except:
            self.__autenticacion_log.error_log("Ha habido un problema para crear usuario")
            return False

    def comprobar_autenticacion(self, nombre_form, contrasenia_form) -> bool:
        try:
            self.__sesion = self.servicio_db.crear_nueva_conexion_si_ha_caducado()
            if (self.__sesion.query(exists().where(Usuario.nombre == nombre_form)).scalar()):
                usuario = self.__sesion.query(Usuario).filter_by(nombre = nombre_form).first()
                self.__sesion.commit()
                if (usuario.get_contrasenia() != contrasenia_form):
                    self.__autenticacion_log.warning_log(
                        f"El usuario con nombre {nombre_form} existe pero las credenciales no son correctas")
                    return self.usuario_autenticado
                elif (usuario.get_contrasenia() == contrasenia_form):
                    self.usuario_autenticado = True
                    self.usuario = usuario
                    self.__autenticacion_log.info_log("Usuario autenticado")
                    self.ultima_autenticacion = time.time()
                    return self.usuario_autenticado
            else:
                self.__autenticacion_log.warning_log(f"El usuario con nombre {nombre_form} no existe")
                return self.usuario_autenticado
        except:
            self.__autenticacion_log.error_log("Ha habido un problema con la autenticacion")