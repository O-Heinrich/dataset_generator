from abc import ABC, abstractmethod
from typing import Any

class EntryInterface(ABC):
    """Interface for Widgets which serve as Entries"""

    @abstractmethod
    def get(self) -> Any:
        pass