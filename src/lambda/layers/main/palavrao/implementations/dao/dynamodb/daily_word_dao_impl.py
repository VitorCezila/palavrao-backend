from dataclasses import dataclass, field

from palavrao.implementations.dao.dynamodb.converters.daily_word_converter import DailyWordConverter
from palavrao.implementations.dao.dynamodb.dao_processor import (
    DaoProcessor,
)
from palavrao.interfaces.dao.daily_word_dao import DailyWordDao, DailyWordNotFound
from palavrao.model.daily_word import DailyWord


@dataclass
class DailyWordDaoDynamoDB(DailyWordDao):
    converter: DailyWordConverter = field(init=True, default=None)
    processor: DaoProcessor = field(init=True, default=None)

    def __post_init__(self):
        self.converter = DailyWordConverter()
        self.processor = DaoProcessor(converter=self.converter)

    def get_word_by_date(self, date_str: str) -> str:
        item_key = self.converter.generate_key(date_str)
        item = self.processor.get_item(item_key)

        if not item:
            raise DailyWordNotFound(f"Word for date {date_str} not found.")

        return item.word

    def save_word(self, date_str: str, word: str):
        daily_word = DailyWord(date_str=date_str, word=word)
        self.processor.put_item(daily_word)
