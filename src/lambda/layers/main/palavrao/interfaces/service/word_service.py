from abc import ABC, abstractmethod


class IWordService(ABC):
    """
    Calculates and returns the word of the day.
    """
    @abstractmethod
    def get_daily_word(self) -> str:
        pass
