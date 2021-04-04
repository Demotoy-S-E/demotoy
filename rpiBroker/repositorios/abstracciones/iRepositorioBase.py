from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')

class IRepositorioBase(ABC, Generic[T]):

    @abstractmethod
    def obtener_todo (self):
        pass

    @abstractmethod
    def obtener_entidad(self, entidad: T) -> T:
        pass

    @abstractmethod
    def insertar_entidad(self, entidad: T) -> bool:
        pass

    @abstractmethod
    def eliminar_entidad(self, entidad: T) -> bool:
        pass