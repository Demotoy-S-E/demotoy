
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
    TOPIC_ACELEROMETRO, 
    HOSTNAME_SIMULACION_LOCAL,
    HOSTNAME_RPI_1)

# Para enterder esto: https://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance
# class ClienteRPI1(Mqtt):
class ClienteRPI1:

    __metaclass__= Singleton

    def __init__(self, nombre_log):
        self.__cliente_log = Applogging(nombre_log)
        global SIMULACION
        if (SIMULACION == False):
            self.client = mqtt.Client()
            self.__cliente_log.info_log(f"Configuracion client rpi1 {TOPIC_ACELEROMETRO}:{HOSTNAME_SIMULACION_LOCAL}")
            # super(ClienteRPI1, self).__init__(
                # cliente = self.cliente, 
                # topic = TOPIC_ACELEROMETRO,
                # hostname = HOSTNAME_SIMULACION_LOCAL)
            self.client.on_connect = _on_connect
            self.client.on_message = _on_message
            self.client.connect(HOSTNAME_SIMULACION_LOCAL, 1883, 60)
            self.client.loop_forever()
    
def _on_connect(client, serdata, flags, rc):
        global TOPIC_ACELEROMETRO
        print("Connected with result code "+str(rc))
    
        # Nos subscribirmos al topic 
        client.subscribe(TOPIC_ACELEROMETRO)

def _on_message(client, userdata, msg):
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