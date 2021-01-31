from flask import _app_ctx_stack, jsonify
import pymysql
from controladores.indexcontroller import Indexcontroller
from controladores.registrocontroller import Registrocontroller
from controladores.principalcontroller import Principalcontroller
from controladores.monitorizacioncontroller import Monitorizacioncontroller
from servicios.weblogging import Applogging
from servicios.mysqlDB import MysqlDB
from servicios.autenticacion import Autenticacion
from modelos import usuario
from modelos import medicionTempemperaturaInterna
from modelos import medicionTempemperaturaExterna
from modelos import medicionAccelerometro
from servicios.clienteRPI1 import ClienteRPI1
from servicios.clienteRPI2 import ClienteRPI2
from servicios.rpiLocal import RpiLocal
from servicios.api import Api

pymysql.install_as_MySQLdb() # hay un error con el paquete principal de mysqlclient, utilizo esta linea para obligar utilizar este paquete

class Startup:

    def __init__(self, app):
        self.__app = app
        self.__log_startup = Applogging("Startup")
        self.__servicio_db = None
        self.__servicio_autenticacion = None
        self.__servicioRPi1 = None
        self.__servicioRPi2 = None
        self.__servicio_rpi_local = None
        self.__api = None
        self.__inyeccion_dependencias()

    def __inyeccion_dependencias(self):
        self.__log_startup.info_log("Iniciando instacias de la aplicacion")
        self.__add_servicio_db()
        self.__add_servicio_autenticacion()
        self.__add_servicio_cliente_rpi1()
        self.__add_servicio_cliente_rpi2()
        self.__add_servicio_principal()
        self.__add_servicio_monitorizacion()

    def __add_servicio_db(self):
        try: 
            self.__log_startup.info_log("Iniciando servicio mysql...")
            self.__servicio_db = MysqlDB(self.__app, _app_ctx_stack)
            self.sesion = self.__servicio_db.sesion
            self.__crear_tablas()
        except:
            self.__log_startup.error_log("Error a la hora de crear tablas")

    def __crear_tablas(self):
        self.__log_startup.info_log("Creando tablas")
        usuario.Base.metadata.create_all(bind = self.__servicio_db.engine)
        medicionTempemperaturaInterna.Base.metadata.create_all(bind = self.__servicio_db.engine)
        medicionTempemperaturaExterna.Base.metadata.create_all(bind = self.__servicio_db.engine)
        medicionAccelerometro.Base.metadata.create_all(bind = self.__servicio_db.engine)
        self.sesion.commit() 

    def __add_servicio_autenticacion(self):
        self.__log_startup.info_log("Iniciando servicio autenticacion...")
        self.__servicio_autenticacion = Autenticacion(self.__servicio_db)
        self.__add_index_controller()
        self.__add_registro_controller()

    def __add_index_controller(self):
        index_controller_log = Applogging("Controlador Index")
        self.__app.add_url_rule('/', endpoint = 'index', view_func = Indexcontroller.as_view(
            'index', 
            autenticacion = self.__servicio_autenticacion, 
            index_controller_log = index_controller_log), 
            methods = ["GET", "POST"])

    def __add_registro_controller(self):
        registro_controller_log = Applogging("Controlador Registro")
        self.__app.add_url_rule('/registro', endpoint = 'registro', view_func = Registrocontroller.as_view(
            'registro', 
            autenticacion = self.__servicio_autenticacion, 
            registro_controller_log = registro_controller_log), 
            methods = ["GET", "POST"])

    """ Aqui se aniade el metodo para cliente RPI1 """
    def __add_servicio_cliente_rpi1(self):
        self.__log_startup.info_log("Iniciando servicio cliente RPi1..")
        nombre_log = "RPI1"
        self.__servicioRPi1 = ClienteRPI1(nombre_log = nombre_log, servicio_db = self.__servicio_db)

    """ Aqui se aniade el metodo para cliente RPI2 """
    def __add_servicio_cliente_rpi2(self):
        self.__log_startup.info_log("Iniciando servicio cliente RPi2..")
        nombre_log = "RPI2"
        self.__servicioRPi2 = ClienteRPI2(nombre_log = nombre_log, servicio_db = self.__servicio_db)

    def __add_servicio_principal(self):
        self.__log_startup.info_log("Iniciando servicio rpi local y api...")
        self.__servicio_rpi_local = RpiLocal()
        self.__api = Api(servicio_db = self.__servicio_db)
        self.__add_principal_controller()

    def __add_principal_controller(self):
        principal_controller_log = Applogging("Controlador Principal")
        self.__app.add_url_rule('/principal', endpoint = 'principal', view_func = Principalcontroller.as_view(
            'principal', 
            autenticacion = self.__servicio_autenticacion, 
            rpi_local = self.__servicio_rpi_local, 
            principal_controller_log = principal_controller_log,
            api = self.__api), 
            methods = ["GET", "POST", "PUT"])

    def __add_servicio_monitorizacion(self):
        self.__log_startup.info_log("Iniciando servicio monitorizacion..")
        self.__add_monitorización_controller()

    def __add_monitorización_controller(self):
        monitorizacion_controller_log = Applogging("Controlador Principal")
        self.__app.add_url_rule('/monitorizacion', endpoint = 'monitorizacion', view_func = Monitorizacioncontroller.as_view(
            'monitorizacion', 
            autenticacion = self.__servicio_autenticacion, 
            monitorizacion_controller_log = monitorizacion_controller_log,
            api = self.__api), 
            methods = ["GET", "POST"])