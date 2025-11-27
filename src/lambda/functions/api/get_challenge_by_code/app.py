import palavrao.requests.utils as req
from palavrao.dto.get_challenge_by_code_response import GetChallengeByCodeResponse
from palavrao.implementations.dao.dynamodb.challenge_dao_impl import ChallengeDaoDynamoDB
from palavrao.implementations.request.aws_lambda_request_context import AwsLambdaRequestContext
from palavrao.implementations.service.challenge_service_implementation import ChallengeServiceImplementation

def _get_challenge_by_code(event, context):
    challenge_dao = ChallengeDaoDynamoDB()
    request_context_provider = AwsLambdaRequestContext(event, context)
    challenge_service = ChallengeServiceImplementation(challenge_dao=challenge_dao,
                                                       request_context=request_context_provider)
    challenge = challenge_service.get_word_challenge()
    response_data: GetChallengeByCodeResponse = {
        "challenge_code": challenge.challenge_code,
        "word": challenge.word,
        "created_at": challenge.created_at
    }
    return req.success(response_data)



def lambda_handler(event, context):
    return req.error_handler(func=_get_challenge_by_code, event=event, context=context)
