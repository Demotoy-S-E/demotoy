from servicios.weblogging import Applogging
from comun.singleton import Singleton

class ClienteRPI1(metaclass=Singleton):

    def __init__(self, nombre_log):
        self.__cliente_log = Applogging(nombre_log)