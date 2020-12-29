from sqlalchemy import Column, Integer, String, LargeBinary
from servicios.mysqlDB import Base

class MTemperaturaExterna(Base):

    def __init__(self, tiempo, temperatura_ambiente):
        self.tiempo = tiempo
        self.temperatura_ambiente = temperatura_ambiente