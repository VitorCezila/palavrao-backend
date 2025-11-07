import json
from typing import Optional

from attr import dataclass
from aws_lambda_powertools.utilities.typing import LambdaContext

from palavrao.implementations.logging import logger
from palavrao.interfaces.request.IRequestContextProvider import IRequestContextProvider
from palavrao.model.request_context import RequestContext


@dataclass
class AwsLambdaRequestContext(IRequestContextProvider):
    event: dict
    context: LambdaContext

    def get_request_context(self) -> RequestContext:
        return RequestContext(
            body=self.__get_body(),
            path_params=self.event.get('pathParameters'),
            headers=self.event.get('headers'),
            path=self.event.get('path')
        )

    def __get_body(self) -> Optional[dict]:
        body = self.event.get('body')
        if body:
            try:
                return json.loads(body)
            except json.JSONDecodeError as e:
                logger.info('Error decoding body, using pure text.', extra={'error_message': e.msg})
                return body
        return None
