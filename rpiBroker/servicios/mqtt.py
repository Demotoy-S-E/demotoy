import comun.excepciones as excepciones
try:
    import paho.mqtt.client as mqtt
except:
    excepciones.error_mosquito_import_log()

from servicios.weblogging import Applogging
import json

# Para enterder esto: https://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance
class Mqtt:

    # En desarrollo
    def __init__(self):
        self.__cofigurar_parametros_conexion_mqtt()

    def __cofigurar_parametros_conexion_mqtt(self):
        print()

    def _on_message(self):
        pass