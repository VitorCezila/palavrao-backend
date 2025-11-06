from abc import ABC, abstractmethod
from typing import List

"""
Interface for a word repository.
Defines the contract to obtain the list of words.
"""
class IWordRepository(ABC):
    @abstractmethod
    def get_all_words(self) -> List[str]:
        pass
