from typing import TypedDict

class CreateChallengeResponse(TypedDict):
    challenge_code: str
    word: str
    created_at: str
