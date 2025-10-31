from datetime import datetime
from zoneinfo import ZoneInfo

from palavrao.implementations.logging import logger
from palavrao.interfaces.word_repository import IWordRepository
from palavrao.interfaces.word_service import IWordService

TZ_BRASIL = ZoneInfo("America/Sao_Paulo")
EPOCH_DATE = datetime(2025, 10, 29, tzinfo=TZ_BRASIL)


class WordServiceImplementation(IWordService):

    def __init__(self, word_repository: IWordRepository):
        self.word_repository = word_repository
        logger.info("DefaultWordService initialized.")

    def get_daily_word(self) -> str:
        words_list = self.word_repository.get_all_words()
        total_words = len(words_list)

        now = datetime.now(tz=TZ_BRASIL)
        days_gone = (now.date() - EPOCH_DATE.date()).days

        if days_gone < 0:
            days_gone = 0

        index_words = days_gone % total_words

        word = words_list[index_words]
        logger.info(f"Daily word: {word} (Índice {index_words})")
        return word
