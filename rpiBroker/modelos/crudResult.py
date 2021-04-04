from typing import TypeVar, Generic
from modelos.baseCrudResult import BaseCrudResult, Results

class CrudResult(BaseCrudResult):

    def __init__(self, result: Results = None):
        super().__init__(result)

# @staticmethod
def success() -> CrudResult:
    crudResult = CrudResult(result =  Results.Success)
    return crudResult

# @staticmethod
def not_found() -> CrudResult:
    crudResult = CrudResult(result = Results.NotFound)
    return crudResult

# @staticmethod
def error() -> CrudResult:
    crudResult = CrudResult(result = Results.Error)
    return crudResult