from sqlalchemy import exists
from repositorios.repositorioBase import RepositorioBase
from modelos.usuario import Usuario
import modelos.crudResult as crudResult
CrudResult = crudResult.CrudResult
import modelos.crudResultT as crudResultT
CrudResultT = crudResultT.CrudResultT
from modelos.crudResult import CrudResult
from servicios.weblogging import Applogging
import asyncio

class RepositorioUsuario(RepositorioBase[Usuario]):

    def __init__(self, servicio_db, sesion):
        super().__init__(servicio_db, sesion)
        self.__repositorio_log = Applogging("UsuarioRepo")

    def obtener_usuario(self, nombre: str) -> CrudResultT[Usuario]:
        try:
            self.sesion = self.servicio_db.crear_nueva_conexion_si_ha_caducado()
            usuario = self.sesion.query(Usuario).filter_by(Usuario.nombre == nombre).first()
            self.sesion.commit()
            if (usuario == None):
                self.__repositorio_log.warning_log(f"El suaurio con nombre:{nombre} no fue encontrado")
                return crudResultT.not_found()
            else:
                self.__repositorio_log.info_log(f"El suaurio con nombre:{nombre} no fue encontrado")
                return crudResultT.success(usuario)
        except Exception:
            self.__repositorio_log.error_log(f"No se han podido obtener la entidad con nombre:{nombre}")
            return crudResultT.error()

    def obtener_usuarios(self) -> list:
        usuarios = self.obtener_todo()
        if (usuarios == None):
            self.__repositorio_log.error_log("No se han encontrado usuarios")
            return crudResultT.not_found()
        else:
            self.__repositorio_log.error_log("Obteniendo todos los suarios")
            return crudResultT.success(usuarios)

    async def task_crear_usuario(self, usuario: Usuario) -> CrudResult:
        if (await self.sesion.query(exists().where(Usuario.nombre == usuario.nombre)).scalar()):
            self.__repositorio_log.warning_log(f"El suaurio {usuario.nombre} ya existe")
            return crudResult.error()
        else: 
            self.__repositorio_log.info_log(f"El suaurio {usuario.nombre} no existe")
            resultado = await self.task_insertar_entidad(usuario)
            if (resultado):
                crudResult.success()
            else:
                return crudResult.error()

    def eliminar_usuario(self, usuario: Usuario) -> CrudResult:
        try:
            self.sesion = self.servicio_db.crear_nueva_conexion_si_ha_caducado()
            if (self.sesion.query(exists().where(Usuario.id == usuario.id)).scalar()):
                self.sesion.query(Usuario).filter_by(Usuario.id == usuario.id).delete(synchronize_session='evaluate')
                self.sesion.commit()
                return crudResult.success()
            else:
                return crudResult.not_found()
        except Exception:
            self.__repositorio_log.error_log(f"No se han podido eliminar la entidad {usuario}")
            return crudResult.error()