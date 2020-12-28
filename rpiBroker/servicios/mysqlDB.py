from sqlalchemy import create_engine, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import paramiko
from sshtunnel import SSHTunnelForwarder
from comun.singleton import Singleton
from servicios.weblogging import Applogging
import json
from time import sleep

Base = declarative_base()

class MysqlDB(metaclass=Singleton):

    def __init__(self, app, _app_ctx_stack):
        self.__app = app
        self.__mysql_log = Applogging("MysqlDB")
        self.__certificado_privado = paramiko.RSAKey.from_private_key_file("domotoy-key.pem")
        self.__ip_local_con_ssh = '127.0.0.1'
        self.__ip_host = None
        self.__puerto_host = None
        self.__server_ssh = None
        self.__cadena_conexion = None
        self.engine = None
        self.sesion = None
        self.__init_configuracion(_app_ctx_stack)

    def crear_nueva_conexion_si_ha_caducado(self):
        try:
            self.sesion.rollback()
            id = self.engine.execute("SELECT id FROM domotoyawsdatabase.usuario").first()
            return self.sesion
        except:
            self.__server_ssh.start()
            self.__mysql_log.warning_log("La sesion ha caducado o ha habido un problema inesperado")
            self.__crear_conexion()
            self.__mysql_log.info_log("Se ha establecido una nueva conexion")
            return self.sesion
        
    def __init_configuracion(self, _app_ctx_stack):
        try:
            self.__obtener_direccion_remota_ssh()
            self.__server_ssh = self.__tunel_ssh()
            self.__server_ssh.start()
            self.__cadena_conexion = self.__obtener_parametros_servidor_desde_json()
            self.__mysql_log.info_log(f"Utilizando direccion: {self.__cadena_conexion}")
            self.engine = create_engine(self.__cadena_conexion, pool_pre_ping = True)
            self.__crear_conexion()
        except:
            self.__mysql_log.error_log("No se han podido iniciar las instancias de la conexion")

    def __tunel_ssh(self):
        try:
            server = SSHTunnelForwarder(
            (self.__ip_host , 22),
            ssh_username='ubuntu',
            ssh_pkey='domotoy-key.pem',
            remote_bind_address=(self.__ip_local_con_ssh, int(self.__puerto_host)),
            )  
            self.__mysql_log.info_log(f"Utilizando la direccion remota {self.__ip_host}:22 con IP host servidor {self.__ip_local_con_ssh}:{self.__puerto_host}")
            return server 
        except:
            self.__mysql_log.error_log("No se han podido establecer la conexion ssh")

    def __crear_conexion(self):
        self.engine.connect()
        Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.sesion = Session()

    def __obtener_direccion_remota_ssh(self):
        try:
            with open("awsserversettings.json") as server_settings_json:
                datos = json.load(server_settings_json)
                for configuracion in datos['settings']:
                    self.__ip_host = configuracion['host']
                    self.__puerto_host = configuracion['port']
        except:
            self.__mysql_log.error_log("No se ha podido obtener las credenciales de servidor remoto")

    def __obtener_parametros_servidor_desde_json(self):
        try:
            cadena_conexion = None
            with open("awsserversettings.json") as server_settings_json:
                datos = json.load(server_settings_json)
                self.__mysql_log.info_log(datos)
                for configuracion in datos['settings']:
                    usuario = configuracion['admin-user']
                    contrasenia = configuracion['password']
                    puerto_local = str(self.__server_ssh.local_bind_port)
                    base_de_datos = configuracion['db']
                    cadena_conexion = self.__crear_cadena_conexion(usuario, contrasenia, self.__ip_local_con_ssh, puerto_local, base_de_datos)
            return cadena_conexion
        except:
            self.__mysql_log.error_log("No se ha podido obtener las credenciales de servidor remoto")

    def __crear_cadena_conexion(self, usuario, contrasenia, ip_host, puerto, base_de_datos):
        return f"mysql+mysqldb://{usuario}:{contrasenia}@{ip_host}:{puerto}/{base_de_datos}"