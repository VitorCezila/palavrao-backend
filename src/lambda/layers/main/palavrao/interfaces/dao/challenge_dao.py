from abc import ABC, abstractmethod

from palavrao.model.word_challenge import WordChallenge


class ChallengeDao(ABC):

    @abstractmethod
    def get_challenge_by_code(self, challenge_code: str) -> WordChallenge:
        pass

    @abstractmethod
    def save_challenge(self, word: WordChallenge):
        pass

class ChallengeNotFound(RuntimeError):
    pass
