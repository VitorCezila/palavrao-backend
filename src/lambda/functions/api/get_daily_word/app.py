import os
from datetime import datetime

import palavrao.requests.utils as req
from palavrao.dto.word_response import WordResponse
from palavrao.implementations.word_service_implementation import WordServiceImplementation, TZ_BRASIL
from palavrao.implementations.file_word_repository import FileWordRepository
from palavrao.interfaces.word_service import IWordService

TASK_ROOT = os.environ.get('LAMBDA_TASK_ROOT', '.')
WORD_FILE_PATH = os.path.join(TASK_ROOT, 'ptbr_5.txt')


def _get_word_logic():
    word_repository = FileWordRepository(full_file_path=WORD_FILE_PATH)
    word_service: IWordService = WordServiceImplementation(word_repository=word_repository)

    word = word_service.get_daily_word()
    response_data: WordResponse = {
        "daily_word": word,
        "reference_date": datetime.now(tz=TZ_BRASIL).isoformat()
    }
    return req.success(response_data)


def lambda_handler(event, context):
    return req.error_handler(func=_get_word_logic(), event=event, context=context, )
