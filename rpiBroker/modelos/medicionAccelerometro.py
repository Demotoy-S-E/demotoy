from sqlalchemy import Column, Integer, String, DateTime, Boolean
from servicios.mysqlDB import Base

class MAcelerometro(Base):

    def __init__(self, fecha, eje_x, eje_y, eje_z):
        self.fecha = fecha
        self.eje_x = eje_x
        self.eje_y = eje_y
        self.eje_z = eje_z
        self.puerta_abierta = self.__verificar_si_esta_abierta()

    # Sin implementar
    def __verificar_si_esta_abierta(self):
        return False

    __tablename__ = 'medicionAcelerometro'
    id = Column(Integer, primary_key = True, index = True, nullable = False)
    fecha = Column(DateTime, index = True, nullable = False)
    eje_x = Column(String(10), index = True, nullable = False)
    eje_y = Column(String(10), index = True, nullable = False)
    eje_z = Column(String(10), index = True, nullable = False)
    puerta_abierta = Column(Boolean, index = False, nullable = True)