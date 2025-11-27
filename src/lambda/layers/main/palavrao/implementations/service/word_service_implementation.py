import random
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from zoneinfo import ZoneInfo

from palavrao.implementations.logging import logger
from palavrao.implementations.repository.file_word_repository import FileWordRepository
from palavrao.interfaces.dao.daily_word_dao import DailyWordDao, DailyWordNotFound
from palavrao.interfaces.service.word_service import IWordService
from palavrao.requests.utils import internal_server_error, ERROR_CODE_UNKNOWN

TZ_BRASIL = ZoneInfo("America/Sao_Paulo")


@dataclass
class WordServiceImplementation(IWordService):
    file_repo: FileWordRepository = field(init=True)
    daily_word_dao: DailyWordDao = field(init=True)

    all_words: List[str] = field(init=False)

    def __post_init__(self):
        try:
            self.all_words = self.file_repo.get_all_words()
            logger.info(f"Word service initialized with {len(self.all_words)} words.")
        except Exception as e:
            logger.critical("Failed to load words from source.", exc_info=True)

    def get_daily_word(self) -> str:
        today_in_brazil = datetime.now(TZ_BRASIL).date()
        today_str = today_in_brazil.strftime('%Y-%m-%d')
        logger.info(f"Trying to get word for date: {today_str}")

        try:
            word = self.daily_word_dao.get_word_by_date(today_str)
            logger.info(f"Word found in database: {word}")
            return word

        except DailyWordNotFound:
            random_word = random.choice(self.all_words)
            logger.info(f"Word random selected: {random_word}")
            self.daily_word_dao.save_word(today_str, random_word)
            return random_word

        except Exception:
            logger.error("Unexpected Error.")
            internal_server_error("Service Error.", ERROR_CODE_UNKNOWN)