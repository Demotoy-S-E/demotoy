from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from comun.singleton import Singleton
from servicios.weblogging import Applogging
from sqlalchemy.orm import scoped_session, sessionmaker

Base = declarative_base()

class MysqlDB(metaclass=Singleton):

    def __init__(self, app, _app_ctx_stack):
        self.__app = app
        self.__mysql_log = Applogging("MysqlDB")
        self.engine = None
        self.sesion = None
        self.__init_configuracion(_app_ctx_stack)
        
    def __init_configuracion(self, _app_ctx_stack):
        try:
            DATABASE_URI = 'mysql://adminuser:adminuser@127.0.0.1:7000/ServicioWeb'
            TEST_URI = 'sqlite:///./test.db'
            self.__mysql_log.info_log(f"Utilizando direccion: {DATABASE_URI}")
            self.engine = create_engine(DATABASE_URI)
            self.engine.connect()
            Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
            self.sesion = Session()
        except:
            self.__mysql_log.error_log("No se han podido iniciar las instancias de la conexion")

    def cerrar_conexion(self):
        self.sesion.commit()
        self.sesion.close()