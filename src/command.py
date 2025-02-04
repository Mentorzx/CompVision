from abc import ABC, abstractmethod
from typing import Callable


class Command(ABC):
    """
    Abstract command interface for executing logging operations.
    """

    @abstractmethod
    def execute(self) -> None:
        """
        Execute the command action.
        """
        pass


class LogCommand(Command):
    """
    Concrete command for logging robot parameters to a file.
    """

    def __init__(self, log_func: Callable[[], None]) -> None:
        self._log_func = log_func

    def execute(self) -> None:
        """
        Execute the logging function.
        """
        self._log_func()
