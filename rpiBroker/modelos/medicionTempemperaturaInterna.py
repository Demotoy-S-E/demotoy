from sqlalchemy import Column, Integer, String, DateTime
from servicios.mysqlDB import Base

class MTemperaturaInterna(Base):

    def __init__(self, fecha, temperatura_cpu):
        self.fecha = fecha
        self.temperatura_cpu = temperatura_cpu  

    __tablename__ = 'medicionTemperaturaInterna'
    id = Column(Integer, primary_key = True, index = True, nullable = False)
    fecha = Column(DateTime, index = True, nullable = False)
    temperatura_cpu = Column(String(3), index = True, nullable = False)