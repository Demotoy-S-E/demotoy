from servicios.weblogging import Applogging
class clienteRPI:

    def __init__(self, nombre_log):
        self.__cliente1_log = Applogging(nombre_log)