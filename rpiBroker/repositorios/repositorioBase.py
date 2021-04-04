from repositorios.abstracciones.iRepositorioBase import IRepositorioBase
from typing import TypeVar, Generic
from servicios.weblogging import Applogging

T = TypeVar('T')

class RepositorioBase(IRepositorioBase, Generic[T]):

    def __init__(self, servicio_db, sesion):
        self.servicio_db = servicio_db
        self.sesion = sesion
        self.__base_log = Applogging("RepositorioBase")

    def obtener_todo(self) -> [T]:
        try:
            self.sesion = self.servicio_db.crear_nueva_conexion_si_ha_caducado()
            entidades = self.seion.query(T).filter_by().all()
            self.sesion.commit()
            return entidades
        except Exception:
            self.__base_log.error_log(f"No se han podido obtener las entidades de tipo {T}")
            return None

    def obtener_entidad(self, entidad: T) -> T:
        try:
            self.sesion = self.servicio_db.crear_nueva_conexion_si_ha_caducado()
            entidad = self.esion.query(T).filter_by(T.id == entidad.id).first()
            self.sesion.commit()
            return entidad
        except Exception:
            self.__base_log.error_log(f"No se ha podido obtener la entidad {entidad}")
            return None

    def insertar_entidad(self, entidad: T) -> bool:
        try:
            self.sesion = self.servicio_db.crear_nueva_conexion_si_ha_caducado()
            self.sesion.add(entidad)
            self.sesion.commit()
            return True
        except Exception:
            self.__base_log.error_log(f"No se han podido insertar la entidad {entidad}")
            return False

    def eliminar_entidad(self, entidad: T) -> bool:
        try:
            self.sesion = self.servicio_db.crear_nueva_conexion_si_ha_caducado()
            self.sesion.query(T).filter_by(T.id == entidad.id).delete(synchronize_session='evaluate')
            self.sesion.commit()
            return True
        except Exception:
            self.__base_log.error_log(f"No se han podido eliminar la entidad {entidad}")
            return False