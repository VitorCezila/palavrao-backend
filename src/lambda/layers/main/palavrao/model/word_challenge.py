from dataclasses import dataclass


@dataclass
class WordChallenge:
    challenge_code: str
    word: str
    created_at: str