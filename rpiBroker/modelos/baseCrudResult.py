from abc import ABC, abstractmethod
from enum import Enum

class Results(Enum):
    Success = 1,
    NotFound = 2,
    Error = 3

class BaseCrudResult(ABC):

    def __init__(self, result: Results = None):
        self.result = result
        self.is_success = self.__is_success()
        self.is_not_found = self.__is_not_found()
        self.is_error = self.__is_error()

    def __is_success(self) -> bool:
        return self.result == Results.Success   

    def __is_not_found(self) -> bool:
        return self.result == Results.NotFound

    def __is_error(self) -> bool:
        return self.result == Results.Error