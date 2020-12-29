from sqlalchemy import Column, Integer, String, LargeBinary
from servicios.mysqlDB import Base

class MAcelerometro(Base):

    def __init__(self, tiempo, eje_x, eje_y, eje_z):
        self.tiempo = tiempo
        self.eje_x = eje_x
        self.eje_y = eje_y
        self.eje_z = eje_z
        self.puerta_abierta = self.__verificar_si_esta_abierta()

    def __verificar_si_esta_abierta(self):
        x = "en desarrollo"