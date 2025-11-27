from dataclasses import dataclass, field

from palavrao.implementations.dao.dynamodb.converters.word_challenge_converter import WordChallengeConverter
from palavrao.implementations.dao.dynamodb.dao_processor import (
    DaoProcessor,
)
from palavrao.interfaces.dao.challenge_dao import ChallengeDao, ChallengeNotFound
from palavrao.model.word_challenge import WordChallenge


@dataclass
class ChallengeDaoDynamoDB(ChallengeDao):
    converter: WordChallengeConverter = field(init=True, default=None)
    processor: DaoProcessor = field(init=True, default=None)

    def __post_init__(self):
        self.converter = WordChallengeConverter()
        self.processor = DaoProcessor(converter=self.converter)


    def get_challenge_by_code(self, challenge_code: str) -> WordChallenge:
        item_key = self.converter.generate_key(challenge_code)
        item = self.processor.get_item(item_key)

        if not item:
            raise ChallengeNotFound(f"Challenge {challenge_code} not found.")

        return item

    def save_challenge(self, word: WordChallenge):
        self.processor.put_item(word)

