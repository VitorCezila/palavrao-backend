from abc import ABC, abstractmethod

from palavrao.model.word_challenge import WordChallenge


class IWordChallengeService(ABC):
    """
    Try to found a challenge word by it code
    """
    @abstractmethod
    def get_word_challenge(self) -> WordChallenge:
        pass

    """
    Save a new challenge
    """
    @abstractmethod
    def create_challenge(self) -> WordChallenge:
        pass