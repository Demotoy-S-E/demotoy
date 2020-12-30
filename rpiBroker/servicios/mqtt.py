import comun.excepciones as excepciones
try:
    import paho.mqtt.client as mqtt
except:
    excepciones.error_mosquito_import_log()

from servicios.weblogging import Applogging
import json
from comun.singleton import Singleton

class Mqtt(metaclass=Singleton):

    # En desarrollo
    def __init__(self):
        self.__cofigurar_parametros_conexion_mqtt()

    def __cofigurar_parametros_conexion_mqtt(self):
        print()

    def on_message(self):
        print()
