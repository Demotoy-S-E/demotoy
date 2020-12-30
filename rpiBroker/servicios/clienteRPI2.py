from servicios.weblogging import Applogging
from comun.singleton import Singleton
class ClienteRPI2(Mqtt):

    def __init__(self, nombre_log):
        super(ClienteRPI2, self).__init__()
        self.__cliente_log = Applogging(nombre_log)