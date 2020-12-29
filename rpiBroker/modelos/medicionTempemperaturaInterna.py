from sqlalchemy import Column, Integer, String, LargeBinary
from servicios.mysqlDB import Base

class MTemperaturaInterna(Base):

    def __init__(self, tiempo, temperatura_cpu):
        self.tiempo = tiempo
        self.temperatura_cpu = temperatura_cpu
