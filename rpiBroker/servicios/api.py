from servicios.weblogging import Applogging
import json

# Para enterder esto: https://stackoverflow.com/questions/3277367/how-does-pythons-super-work-with-multiple-inheritance
class Api:

    def __init__(self, servicio_db):
        self.__servicio_db = servicio_db

    def modificar_usuario(self):
        print()

    def obtener_ultimas_mediciones_accel(self):
        print()

    def obtener_ultimas_mediciones_temperatura_externa(self):
        print()
