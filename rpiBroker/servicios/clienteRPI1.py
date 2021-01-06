from servicios.mqtt import Mqtt
from servicios.weblogging import Applogging
from comun.singleton import Singleton

topic = "deustoLab/aceleracion"

# Para enterder esto: https://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance
class ClienteRPI1(Mqtt):

    __metaclass__= Singleton

    def __init__(self, nombre_log):
        super(ClienteRPI1, self).__init__()
        self.__cliente_log = Applogging(nombre_log)
    
# Callback que se llama cuando el cliente recibe el CONNACK del servidor 
#Restult code 0 significa conexion sin errores
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
 
    # Nos subscribirmos al topic 
        client.subscribe(topic)
 #-----------------------------------------------   
# Callback que se llama "automaticamente" cuando se recibe un mensaje del Publiser.
    int varx_ = 0
    def on_message(client, userdata, msg):
        msg.payload = msg.payload.decode("utf-8")
        mensaje_recibido = msg.payload
        print(msg.topic+" "+mensaje_recibido)

        #the message received starts with 'b, that mean bytes. 
        mensaje_recibido_json =json.loads(msg.payload )
        varx=mensaje_recibido_json["varx"]
        
        if( varx != varx_):
            print("Se ha movido la puerta")
        varx_ = varx

    #-----------------------------------------------
    # Creamos un cliente MQTT 
    client = mqtt.Client()

    #Definimos los callbacks para conectarnos y subscribirnos al topic
    client.on_connect = on_connect
    client.on_message = on_message

    #Para la actividad 1: usad la IP de la RPi que actúa como broker
    hostname ="169.254.28.119"

    #Para la actividad 2: usad la IP del servidor gratutio de mosquitto
    #hostname = "test.mosquitto.org"
    
    client.connect(hostname, 1883, 60)
    client.loop_forever()