from typing import TypedDict

class GetChallengeByCodeResponse(TypedDict):
    challenge_code: str
    word: str
    created_at: str
