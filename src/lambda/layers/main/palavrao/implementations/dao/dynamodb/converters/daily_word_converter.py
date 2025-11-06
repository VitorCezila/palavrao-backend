from palavrao.interfaces.dao.object_converter import ObjectConverter

from palavrao.interfaces.dao.object_converter import ObjectConverter
from palavrao.model.daily_word import DailyWord
from typing import Dict, Any

from palavrao.implementations.dao.dynamodb.dao_processor import (
    PARTITION_KEY_NAME,
    SORT_KEY_NAME,
)


class DailyWordConverter(ObjectConverter):

    PREFIX = "DAILY_WORD"

    def from_dict(self, data: Dict[str, Any]) -> DailyWord | None:
        if not data:
            return None

        date_str = data.get(SORT_KEY_NAME)

        return DailyWord(
            date_str=date_str,
            word=data.get('word')
        )

    def to_dict(self, obj: DailyWord) -> Dict[str, Any]:
        return {
            PARTITION_KEY_NAME: self.PREFIX,
            SORT_KEY_NAME: obj.date_str,
            'word': obj.word
        }

    def generate_key(self, date_str: str) -> dict :
        return {
            PARTITION_KEY_NAME: self.PREFIX,
            SORT_KEY_NAME: date_str
        }