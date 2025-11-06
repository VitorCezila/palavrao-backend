from abc import ABC, abstractmethod


class DailyWordDao(ABC):

    @abstractmethod
    def get_word_by_date(self, date_str: str) -> str:
        pass

    @abstractmethod
    def save_word(self, date_str: str, word: str):
        pass

class DailyWordNotFound(RuntimeError):
    pass
