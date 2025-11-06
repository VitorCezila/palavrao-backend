from palavrao.interfaces.dao.object_converter import ObjectConverter
from palavrao.model.word_challenge import WordChallenge
from typing import Dict, Any

from palavrao.implementations.dao.dynamodb.dao_processor import (
    PARTITION_KEY_NAME,
    SORT_KEY_NAME,
)


class WordChallengeConverter(ObjectConverter):

    PREFIX = "CHALLENGE"

    def from_dict(self, data: Dict[str, Any]) -> WordChallenge | None:
        if not data:
            return None

        return WordChallenge(
            challenge_code=data.get(SORT_KEY_NAME),
            word=data.get('word'),
            created_at=data.get('createdAt')
        )

    def to_dict(self, obj: WordChallenge) -> Dict[str, Any]:
        return {
            PARTITION_KEY_NAME: self.PREFIX,
            SORT_KEY_NAME: obj.challenge_code,
            'word': obj.word,
            'createdAt': obj.created_at
        }

    def generate_key(self, challenge_code: str) -> dict :
        return {
            PARTITION_KEY_NAME: self.PREFIX,
            SORT_KEY_NAME: challenge_code
        }