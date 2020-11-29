from flask import _app_ctx_stack, jsonify
from flask_cors import CORS
from servicios.weblogging import Applogging
from servicios.mysqlDB import MysqlDB
from modelos import usuario
from servicios.clienteRPI import clienteRPI

class Startup:

    def __init__(self, app):
        self.__app = app
        CORS(self.__app)
        self.__log_startup = Applogging("Startup")
        self.sesion = None
        self.__servicio_db = None
        self.__servicioRPi1 = None
        self.__servicioRPi2 = None
        self.__inyeccion_dependencias()

    def __inyeccion_dependencias(self):
        self.__log_startup.info_log("Iniciando instacias de la aplicacion")
        self.__add_servicio_db()
        self.__add_servicio_autenticacion()
        self.__add_servicio_cliente_rpi1()
        self.__add_servicio_cliente_rpi2()

    def __add_servicio_db(self):
        try: 
            self.__log_startup.info_log("Iniciando servicio mysql...")
            self.__servicio_db = MysqlDB(self.__app, _app_ctx_stack)
            self.sesion = self.__servicio_db.sesion
            self.__log_startup.info_log("Creando tablas")
            usuario.Base.metadata.create_all(bind = self.__servicio_db.engine)
        except:
            self.__log_startup.error_log("Error a la hora de crear tablas")

    def __add_servicio_autenticacion(self):
        self.__log_startup.info_log("Iniciando servicio autenticacion...")

    """ Aqui se aniade el metodo para cliente RPI1 """
    def __add_servicio_cliente_rpi1(self):
        self.__log_startup.info_log("Iniciando servicio cliente RPi1..")
        nombre_log = "RPI1"
        self.__servicioRPi1 = clienteRPI(nombre_log)

    """ Aqui se aniade el metodo para cliente RPI2 """
    def __add_servicio_cliente_rpi2(self):
        self.__log_startup.info_log("Iniciando servicio cliente RPi2..")
        nombre_log = "RPI"
        self.__servicioRPi2 = clienteRPI(nombre_log)