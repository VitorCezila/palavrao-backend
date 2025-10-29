from typing import List, Optional

import palavrao.requests.utils as req
from palavrao.implementations.logging import logger
from palavrao.interfaces.word_repository import IWordRepository

_CACHED_WORDS: Optional[List[str]] = None


class FileWordRepository(IWordRepository):

    def __init__(self, full_file_path: str):
        self.file_path = full_file_path
        logger.info(f"FileWordRepository initialized. Reading from: {self.file_path}")

    def get_all_words(self) -> List[str]:
        global _CACHED_WORDS
        if _CACHED_WORDS is not None:
            return _CACHED_WORDS

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                words = [line.strip().upper() for line in f if line.strip()]
            if not words:
                logger.error("The word file is empty.", file_path=self.file_path)
                return req.not_found("Word not found")
            else:
                logger.info(f"Success: {len(words)} words loaded.")
                _CACHED_WORDS = words
            return _CACHED_WORDS
        except FileNotFoundError:
            logger.error(f"FATAL: Words file not found.", file_path=self.file_path)
            return req.not_found("Word not found")
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            return req.internal_server_error("Internal server error", req.ERROR_CODE_INTERNAL_ERROR)
