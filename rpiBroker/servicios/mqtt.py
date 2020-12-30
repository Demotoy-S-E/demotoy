import comun.excepciones as excepciones
try:
    import paho.mqtt.client as mqtt
except:
    excepciones.error_mosquito_import_log()

from servicios.weblogging import Applogging
import json

class Mqtt:

    # En desarrollo
    def __init__(self):
        print()