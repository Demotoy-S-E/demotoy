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

    def crear_usuario(self, nuevo_usuario) -> bool:
        try:
            self.__sesion = self.servicio_db.crear_nueva_conexion_si_ha_caducado()
            if (self.__usuario_existe(nuevo_usuario.nombre)):
                return False
            else:
                nuevo_usuario = Usuario(
                    nombre = nuevo_usuario.nombre, 
                    email = nuevo_usuario.email, 
                    contrasenia = nuevo_usuario.contrasenia,
                    nombre_completo = nuevo_usuario.nombre_completo,
                    numero_telefono = nuevo_usuario.numero_telefono,
                    direccion = nuevo_usuario.direccion)
                self.__sesion.add(nuevo_usuario)
                self.__sesion.commit()
                return True
        except:
            self.__autenticacion_log.error_log("Ha habido un problema para crear usuario")
            return False

    def comprobar_autenticacion(self, nombre_form, contrasenia_form) -> bool:
        try:
            self.__sesion = self.servicio_db.crear_nueva_conexion_si_ha_caducado()
            if (self.__usuario_existe(nombre_form)):
                usuario_existente = self.__obtener_usuario(nombre_form)
                self.__sesion.commit()
                self.__comprobar_credenciales(usuario_existente, nombre_form, contrasenia_form)
                return self.usuario_autenticado
            else:
                self.__autenticacion_log.warning_log(f"El usuario con nombre {nombre_form} no existe")
                return self.usuario_autenticado
        except:
            self.__autenticacion_log.error_log("Ha habido un problema con la autenticacion")

    def __usuario_existe(self, nombre_form) -> bool:
        if (self.__sesion.query(exists().where(Usuario.nombre == nombre_form)).scalar()):
                self.__autenticacion_log.info_log(f"El usuario con nombre {nombre_form} existe")
                return True
        else:
            return False

    def __obtener_usuario(self, nombre_form):
        usuario = self.__sesion.query(Usuario).filter_by(nombre = nombre_form).first()
        return usuario

    def __comprobar_credenciales(self, usuario_existente, nombre_form, contrasenia_form):
        if (usuario_existente.get_contrasenia() != contrasenia_form):
                self.__autenticacion_log.warning_log(
                    f"El usuario con nombre {nombre_form} existe pero las credenciales no son correctas")
        elif (usuario_existente.get_contrasenia() == contrasenia_form):
            self.__estado_autenticado_true(usuario_existente)

    def __estado_autenticado_true(self, usuario_existente):
        self.usuario_autenticado = True
        self.usuario = usuario_existente
        self.__autenticacion_log.info_log("Usuario autenticado")
        self.ultima_autenticacion = time.time()