from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Mountain:

    name: str
    difficulty_level: int
    length: int

    def __lt__(self, other: Mountain) -> bool:
        """
        Overwriting '<' operator to compare 2 mountains length and names.
        other: instance of Mountain class
        """
        if self.length == other.length:
            return self.name <= other.name
        return self.length < other.length

    def __eq__(self, other: Mountain) -> bool:
        """
        Overwriting '=' operator to compare 2 mountains length and names.
        other: instance of Mountain class
        """
        if self.length == other.length:
            return self.name == other.name

    def __gt__(self, other: Mountain) -> bool:
        """
        Overwriting '>' operator to compare 2 mountains length and names.
        other: instance of Mountain class
        """
        if self.length == other.length:
            return self.name >= other.name
        return self.length > other.length



