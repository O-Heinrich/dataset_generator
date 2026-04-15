import random
from typing import Any

class ColumnListener:
    """
    A wrapper for a dictionary, where the keys are primary key values mapped to generated values.
    Objects of this class are coupled between two Columns, when one Column depends on the other.
    One Column can insert the generated values into a Listener and another Column can later get it asynchronously.
    Values in the dictionary cannot be overriden once they've been put in.
    """
    
    def __init__(self) -> None:
        """Create an empty Listener"""
        self.data: dict[int, Any] = {}
    
    def add(self, key: int, value=None):
        """Add a value to this Listener"""
        if key in self.data:
            raise KeyError("No duplicate keys allowed for Listener")
        self.data[key] = value

    def addAll(self, startkey: int, values: list[Any]):
        """Add multiple values to this Listener, starting with the given key and adding all values sequentially."""
        k = startkey
        for value in values:
            self.add(k, value)
            k += 1

    def get(self, key: int) -> Any:
        """Returns the value this Listener was given for a key."""
        if key not in self.data:
            raise KeyError(f'Key {key} does not exist in this Listener')
        return self.data.get(key)
    
    def randomKey(self) -> int:
        """Returns a random valid key from this Listener."""
        return random.choice(list(self.data.keys()))
    
    def randomValue(self) -> Any:
        """Returns a random value from this Listener."""
        return random.choice(list(self.data.values()))