from servicios.mqtt import Mqtt
from servicios.weblogging import Applogging
from comun.singleton import Singleton

topic = "deustoLab/aceleracion"

# Para enterder esto: https://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance
class ClienteRPI1(Mqtt):

    __metaclass__= Singleton

    def __init__(self, nombre_log):
        super(ClienteRPI1, self).__init__(nombre = "asier")
        self.__cliente_log = Applogging(nombre_log)
    
    def _on_message(self):
            pass 