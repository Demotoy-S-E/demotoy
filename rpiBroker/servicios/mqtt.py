from servicios.weblogging import Applogging
import json

# Para enterder esto: https://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance
class Mqtt:

    # En desarrollo
    def __init__(self, cliente, topic, hostname):
        # cliente.on_connect = _on_connect()
        # cliente.on_message = _on_message()
        cliente.connect(hostname, 1883, 60)
        cliente.loop_forever()

    def _on_connect(self):
        pass

    def _on_message(self):
        pass
