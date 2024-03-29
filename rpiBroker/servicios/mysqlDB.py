import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import create_engine, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sshtunnel import SSHTunnelForwarder
from comun.singleton import Singleton
from servicios.weblogging import Applogging
import json
from time import sleep
import traceback
import sys
from static.constantes import (
    MYSQL_IP_LOCAL, 
    MYSQL_USER, 
    MYSQL_CONTRASENIA, 
    MYSQl_PUERTO, 
    MYSQL_NOMBRE_DB, 
    SSH_IP_REMOTA, 
    SSH_PUERTO, 
    SSH_NOMBRE_USUARIO, 
    SSH_PRIVATE_KEY_PATH, 
    PUERTO_SOCKET_LOCAL)

Base = declarative_base()

class MysqlDB(metaclass=Singleton):

    def __init__(self, app, _app_ctx_stack):
        self.__app = app
        self.__mysql_log = Applogging("MysqlDB")
        self.__server_ssh = None
        self.engine = None
        self.sesion = None
        self.__iniciar_instancias_conexiones(_app_ctx_stack)

    def crear_nueva_conexion_si_ha_caducado(self):
        try:
            self.sesion.rollback()
            id = self.engine.execute("SELECT id FROM domotoyawsdatabase.usuario").first()
            return self.sesion
        except Exception:
            self.__mysql_log.warning_log("La sesion ha caducado o ha habido un problema inesperado")
            self.__server_ssh = self.__crear_tunel_ssh()
            self.__crear_conexion_demotoy_database()
            self.__mysql_log.info_log("Se ha establecido una nueva conexion")
            return self.sesion
        
    def __iniciar_instancias_conexiones(self, _app_ctx_stack):
        try:
            puerto_socket_ssh = self.__iniciar_ssh()
            self.__iniciar_mysql(puerto_socket_ssh)
        except Exception:
            self.__mysql_log.error_log("No se han podido iniciar las instancias de la conexion")
            self.__mysql_log.info_log("Inciando conexion con una base de datos local")
            self.__iniciar_mysql("3306")
        except Exception:
            self.__mysql_log.error_log("No se han podido iniciar las instancias de la conexion")

    def __iniciar_ssh(self) -> str:
        self.__obtener_direccion_remota_ssh()
        self.__server_ssh = self.__crear_tunel_ssh()
        puerto_socket_ssh = str(self.__server_ssh.local_bind_port)
        return puerto_socket_ssh

    def __obtener_direccion_remota_ssh(self) -> str:
        global SSH_IP_REMOTA, SSH_PUERTO, SSH_NOMBRE_USUARIO, SSH_PRIVATE_KEY_PATH
        try:
            with open("awsserversettings.json") as server_settings_json:
                datos = json.load(server_settings_json)
                for configuracion in datos['ssh-settings']:
                    SSH_IP_REMOTA = configuracion['host-remote']
                    SSH_PUERTO = configuracion['port']
                    SSH_NOMBRE_USUARIO = configuracion['server-user']
                    SSH_PRIVATE_KEY_PATH = configuracion['private-key']
        except Exception:
            self.__mysql_log.error_log("No se ha podido obtener las credenciales de servidor remoto")

    def __crear_tunel_ssh(self) -> SSHTunnelForwarder:
        try:
            server = SSHTunnelForwarder(
            (SSH_IP_REMOTA, SSH_PUERTO),
            ssh_username = SSH_NOMBRE_USUARIO,
            ssh_pkey = SSH_PRIVATE_KEY_PATH,
            remote_bind_address=(MYSQL_IP_LOCAL, MYSQl_PUERTO),
            )  
            self.__mysql_log.info_log(
                f"Utilizando la direccion remota {SSH_IP_REMOTA}:{SSH_PUERTO} con IP host servidor {MYSQL_IP_LOCAL}:{MYSQl_PUERTO}")

            server.start()
            return server 
        except Exception:
            self.__mysql_log.error_log("No se han podido establecer la conexion ssh")

    def __iniciar_mysql(self, puerto_socket_ssh):
            self.__cadena_conexion = self.__obtener_direcion_remota_mysql(puerto_socket_ssh)
            self.__mysql_log.info_log(f"Utilizando direccion mysql mediante ssh: {self.__cadena_conexion}")
            self.engine = create_engine(self.__cadena_conexion, pool_pre_ping = True)
            self.__crear_conexion_demotoy_database()

    def __obtener_direcion_remota_mysql(self, puerto_socket_ssh) -> str:
        global MYSQL_IP_LOCAL, MYSQL_USER, MYSQL_CONTRASENIA, MYSQl_PUERTO, MYSQL_NOMBRE_DB, PUERTO_SOCKET_LOCAL
        try:
            PUERTO_SOCKET_LOCAL = puerto_socket_ssh
            cadena_conexion = None
            with open("awsserversettings.json") as server_settings_json:
                datos = json.load(server_settings_json)
                self.__mysql_log.info_log(datos)
                for configuracion in datos['mysql-server-settings']:
                    MYSQL_IP_LOCAL = configuracion['host-local']
                    MYSQL_USER = configuracion['admin-user']
                    MYSQL_CONTRASENIA = configuracion['password']
                    MYSQl_PUERTO = configuracion['mysql-port']
                    MYSQL_NOMBRE_DB = configuracion['db']
                    cadena_conexion = self.__crear_cadena_conexion(MYSQL_USER, MYSQL_CONTRASENIA, MYSQL_IP_LOCAL, PUERTO_SOCKET_LOCAL, MYSQL_NOMBRE_DB)
            return cadena_conexion
        except Exception:
            self.__mysql_log.error_log("No se ha podido obtener las credenciales de servidor remoto")

    def __crear_cadena_conexion(self, usuario, contrasenia, ip_local, puerto_socket, base_de_datos):
        return f"mysql+mysqldb://{usuario}:{contrasenia}@{ip_local}:{puerto_socket}/{base_de_datos}"

    def __crear_conexion_demotoy_database(self):
        global MYSQL_NOMBRE_DB
        try:
            self.engine.connect()
            Session = sessionmaker(
                autocommit = False, 
                autoflush = False, 
                bind=self.engine)
            self.sesion = Session()
        except Exception:
            self.__mysql_log.error_log("Error al intentar crear la conexión con la base de datos: {MYSQL_NOMBRE_DB}")