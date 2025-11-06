import os
from datetime import datetime

import palavrao.requests.utils as req
from palavrao.dto.word_response import WordResponse
from palavrao.implementations.dao.dynamodb.daily_word_dao_impl import DailyWordDaoDynamoDB
from palavrao.implementations.repository.file_word_repository import FileWordRepository
from palavrao.implementations.service.word_service_implementation import WordServiceImplementation, TZ_BRASIL
from palavrao.interfaces.service.word_service import IWordService

TASK_ROOT = os.environ.get('LAMBDA_TASK_ROOT', '.')
WORD_FILE_PATH = os.path.join(TASK_ROOT, 'ptbr_5.txt')
file_repo = FileWordRepository(full_file_path=WORD_FILE_PATH)


def _get_word_logic(event, context):
    word_repository = FileWordRepository(full_file_path=WORD_FILE_PATH)
    daily_word_dao = DailyWordDaoDynamoDB()
    word_service: IWordService = WordServiceImplementation(file_repo=word_repository, daily_word_dao=daily_word_dao)

    word = word_service.get_daily_word()
    response_data: WordResponse = {
        "daily_word": word,
        "reference_date": datetime.now(tz=TZ_BRASIL).isoformat()
    }
    return req.success(response_data)


def lambda_handler(event, context):
    return req.error_handler(func=_get_word_logic, event=event, context=context)
