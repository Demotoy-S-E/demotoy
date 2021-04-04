from typing import TypeVar, Generic
from modelos.baseCrudResult import BaseCrudResult, Results

T = TypeVar('T')

class CrudResultT(BaseCrudResult, Generic[T]):

    def __init__(self, value: T = None, result: Results = None):
        if (value != None):
            self.value = value
        super().__init__(result)

# @staticmethod
def not_found() -> CrudResultT[T]:
    crudResult = CrudResultT(result = Results.NotFound)
    return crudResult

# @staticmethod
def error() -> CrudResultT[T]:
    crudResult = CrudResultT(result = Results.Error)
    return crudResult

# @staticmethod
def success(value: T) -> CrudResultT[T]:
    crudResult = CrudResultT(value = value, result =  Results.Success)
    return crudResult