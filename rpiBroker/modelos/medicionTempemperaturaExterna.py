from sqlalchemy import Column, Integer, String, DateTime
from servicios.mysqlDB import Base

class MTemperaturaExterna(Base):

    def __init__(self, fecha, temperatura_ambiente):
        self.fecha = fecha
        self.temperatura_ambiente = temperatura_ambiente

    __tablename__ = 'medicionTemperaturaExterna'
    id = Column(Integer, primary_key = True, index = True, nullable = False)
    fecha = Column(DateTime, index = True, nullable = False)
    temperatura_ambiente = Column(String(3), index = True, nullable = False)