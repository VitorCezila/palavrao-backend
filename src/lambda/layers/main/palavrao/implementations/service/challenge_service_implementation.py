import secrets
from dataclasses import dataclass, field
from datetime import datetime
from zoneinfo import ZoneInfo

import palavrao.requests.utils as req
from palavrao.implementations.logging import logger
from palavrao.interfaces.dao.challenge_dao import ChallengeDao, ChallengeNotFound
from palavrao.interfaces.request import IRequestContextProvider
from palavrao.interfaces.service.challenge_service import IWordChallengeService
from palavrao.model.word_challenge import WordChallenge
from palavrao.requests.utils import ERROR_CODE_INTERNAL_ERROR

TZ_BRASIL = ZoneInfo("America/Sao_Paulo")


@dataclass
class ChallengeServiceImplementation(IWordChallengeService):
    challenge_dao: ChallengeDao = field(init=True)
    request_context: IRequestContextProvider = field(init=True)

    def get_word_challenge(self) -> WordChallenge:
        request_context = self.request_context.get_request_context()
        challenge_code = request_context.path_params['code']
        try:
            challenge = self.challenge_dao.get_challenge_by_code(challenge_code)
            return challenge
        except ChallengeNotFound:
            logger.info('Challenge not found')
            req.not_found('Challenge not found')


    def create_challenge(self) -> WordChallenge:
        request_context = self.request_context.get_request_context()
        self._validate_request()
        challenge_code = self._generate_share_code(6)
        word = request_context.body['word']
        challenge = WordChallenge(
            challenge_code=challenge_code,
            word=word.upper(),
            created_at=datetime.now(TZ_BRASIL).isoformat()
        )

        try:
            self.challenge_dao.save_challenge(challenge)
            logger.info(f"Challenge created with code: {challenge_code}")
            return challenge
        except Exception:
            logger.error("Error creating challenge.")
            req.internal_server_error('Unknown error', ERROR_CODE_INTERNAL_ERROR)

    def _generate_share_code(self, length: int = 6) -> str:
        alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def _validate_request(self):
        schema = self.__create_challenge_request_json_schema()
        body = self.request_context.get_request_context().body
        self._validate_json(body, schema)

    @staticmethod
    def _validate_json(body: dict, schema: dict):
        return req.validate_json(body, schema)

    @staticmethod
    def __create_challenge_request_json_schema():
        return {
            "type": "object",
            "required": ['word'],
            "properties": {
                "word": {"type": "string"}
            }
        }
