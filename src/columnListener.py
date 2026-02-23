import random

from typing import Any

class ColumnListener:
    
    def __init__(self) -> None:
        self.data: dict[int, Any] = {}
    
    def add(self, key: int, value=None):
        if key in self.data:
            raise KeyError("No duplicate keys allowed for Listener")
        self.data[key] = value

    def addAll(self, startkey: int, values: list[Any]):
        k = startkey
        for value in values:
            self.add(k, value)
            k += 1

    def get(self, key: int) -> Any:
        if key not in self.data:
            raise KeyError(f'Key {key} does not exist in this Listener')
        return self.data.get(key)
    
    def randomKey(self) -> int:
        return random.choice(list(self.data.keys()))
    
    def randomValue(self) -> Any:
        return random.choice(list(self.data.values()))