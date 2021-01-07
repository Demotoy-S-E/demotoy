SIMULACION = False

import comun.excepciones as excepciones
try:
    import paho.mqtt.client as mqtt
except:
    excepciones.error_mosquito_import_log()
    SIMULACION = True

import json
from servicios.mqtt import Mqtt
from servicios.weblogging import Applogging
from comun.singleton import Singleton
from static.constantes import (
    TOPIC_TEMPERATURA, 
    HOSTNAME_SIMULACION_LOCAL,
    HOSTNAME_RPI_2)

# Para enterder esto: https://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance
class ClienteRPI2:

    __metaclass__= Singleton

    def __init__(self, nombre_log):
        global SIMULACION
        if (SIMULACION == False):
            self.cliente.on_connect = _on_connect()
            self.cliente.on_message = _on_message()

    def _on_connect(self, serdata, flags, rc):
        global TOPIC_TEMPERATURA
        print("Connected with result code "+str(rc))
    
        # Nos subscribirmos al topic 
        self.client.subscribe(TOPIC_TEMPERATURA)

    def _on_message(self, userdata, msg):
        msg.payload = msg.payload.decode("utf-8")
        mensaje_recibido = msg.payload
        print(msg.topic+" "+mensaje_recibido)

        #the message received starts with 'b, that mean bytes. 
        mensaje_recibido_json =json.loads(msg.payload )
    
        varx=mensaje_recibido_json["varx"]
        print(varx)

        vary=mensaje_recibido_json["vary"]
        print(vary)

        varz=mensaje_recibido_json["varz"]
        print(varz)