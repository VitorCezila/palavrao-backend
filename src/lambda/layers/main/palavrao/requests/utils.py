import decimal
import json

import jsonschema

from palavrao.implementations.logging import logger

REGEX_DATETIME = r'^([12][0-9]{3}-?(0[1-9]|1[0-2])-?(0[1-9]|[12][0-9]|3[01])([ T]([01][0-9]|2[0-3]):?([0-5][0-9]):?([0-5][0-9]))(\.[0-9]+)?(([+\-]([01][0-9]|2[0-3])(:?[0-5][0-9])?)|Z)?)$'
REGEX_DATE_ISO = r'^([12][0-9]{3}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01]))$'
REGEX_DATE = r'^([12][0-9]{3}-?(0[1-9]|1[0-2])-?(0[1-9]|[12][0-9]|3[01]))$'
REGEX_ALPHA = r'^[a-zA-Z]+$'
REGEX_ALPHA_NUMERIC = r'^[a-zA-Z0-9]+$'
REGEX_NUMERIC = r'^[0-9]+$'
REGEX_TIMEZONE = r'^(([+\-]([01][0-9]|2[0-3])(:?[0-5][0-9])?)|Z)$'

ERROR_CODE_NOT_FOUND = 'NOT_FOUND'
ERROR_CODE_REQUIRED_PARAM = 'REQUIRED_PARAM'
ERROR_CODE_INVALID_PARAM_TYPE = 'INVALID_PARAM_TYPE'
ERROR_CODE_INVALID_PARAM_VALUE = 'INVALID_PARAM_VALUE'
ERROR_CODE_INVALID_PARAM = 'INVALID_PARAM'
ERROR_CODE_UNAUTHORIZED = 'UNAUTHORIZED'
ERROR_CODE_FORBIDDEN = 'FORBIDDEN'
ERROR_CODE_SUCCESS = 'SUCCESS'
ERROR_CODE_NULL_POINTER = 'NULL_POINTER'
ERROR_CODE_UNKNOWN = 'UNKNOWN_ERROR'
ERROR_CODE_CONFIG_ERROR = 'CONFIG_ERROR'
ERROR_CODE_INTERNAL_ERROR = 'INTERNAL_ERROR'
ERROR_CODE_INTEGRATION_ERROR = 'INTEGRATION_ERROR'
ERROR_CODE_UNPROCESSABLE_ENTITY = 'UNPROCESSABLE_ENTITY'


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            value = float(o)
            return int(value) if value.is_integer() else value
        if isinstance(o, set):
            return list(o)
        return super(DecimalEncoder, self).default(o)


class Error(Exception):
    pass


class PalavraoError(Error):
    def __init__(self, message):
        self.message = message


def get_body_json(event):
    param = 'body'
    if event is None:
        return None
    elif param not in event:
        return None
    if event[param] is None:
        return None
    try:
        return json.loads(event[param])
    except json.JSONDecodeError as e:
        logger.exception(e)
        return None


def generate_validator_response(message, error_code, field=None):
    return bad_request(message, error_code, field)


def __generate_oneof_return_message(fields: list):
    msg = ' or '.join([str(reqs['required']) for reqs in fields])
    return f'Fields {msg} are required!'


def validate_json(data, schema):
    try:
        jsonschema.validate(data, schema)
    except jsonschema.ValidationError as e:
        if e.validator != 'required':
            msg = get_validator_message(e)
            if e.validator == 'type':
                return generate_validator_response(msg, ERROR_CODE_INVALID_PARAM_TYPE, get_json_path(e.path))
            elif e.validator == 'additionalProperties':
                return generate_validator_response(msg, ERROR_CODE_INVALID_PARAM, get_json_path(e.path))
            elif e.validator == 'dependencies':
                return generate_validator_response(msg, ERROR_CODE_REQUIRED_PARAM, get_json_path(e.path))
            elif e.validator == 'oneOf':
                return generate_validator_response(__generate_oneof_return_message(e.validator_value),
                                                   ERROR_CODE_REQUIRED_PARAM, get_json_path(e.path))
            else:
                return generate_validator_response(msg, ERROR_CODE_INVALID_PARAM_VALUE, get_json_path(e.path))
        obj = data
        for k in e.path:
            obj = obj[k]
        for k in e.validator_value:
            if k not in obj:
                m_path = e.path
                m_path.append(k)
                m_field = get_json_path(m_path)
                msg = f'Field "{m_field}" is required.'
                return generate_validator_response(msg, ERROR_CODE_REQUIRED_PARAM, m_field)
    return None


def get_json_path(path):
    m_path = ''
    m_separator = ''
    for p in path:
        if type(p) is str:
            m_path += f'{m_separator}{p}'
            m_separator = '.'
        elif type(p) is int:
            m_path += f'[{p}]'
    return m_path


def get_validator_message(error):
    if type(error) is not jsonschema.ValidationError:
        return 'Unknown error'

    m_field = get_json_path(error.path)
    if error.validator == 'type':
        return f'Field "{m_field}" must be of type "{error.validator_value}".'
    elif error.validator == 'pattern':
        if error.validator_value == REGEX_DATE:
            return f'Field "{m_field}" must be a date with format "YYYY-MM-DD".'
        elif error.validator_value == REGEX_DATE_ISO:
            return f'Field "{m_field}" must be a date with format "YYYY-MM-DD".'
        elif error.validator_value == REGEX_DATETIME:
            return f'Field "{m_field}" must be a date-time with format "YYYY-MM-DDTHH:mm:ss<time zone offset>".'
        elif error.validator_value == REGEX_ALPHA:
            return f'Field "{m_field}" must contain only letters.'
        elif error.validator_value == REGEX_ALPHA_NUMERIC:
            return f'Field "{m_field}" must contain only letters and numbers.'
        elif error.validator_value == REGEX_NUMERIC:
            return f'Field "{m_field}" must contain only numbers.'
        return f'Field "{m_field}" must match "{error.validator_value}"'
    elif error.validator == 'minimum':
        return f'Field "{m_field}" can not be less than "{error.validator_value}"'
    elif error.validator == 'maximum':
        return f'Field "{m_field}" can not be greater than "{error.validator_value}"'
    elif error.validator == 'multipleOf':
        return f'Field "{m_field}" must be multiple of "{error.validator_value}"'
    elif error.validator == 'maxLength':
        return f'Field "{m_field}" can not be longer than "{error.validator_value}"'
    elif error.validator == 'minLength':
        return f'Field "{m_field}" can not be shorter than "{error.validator_value}"'
    elif error.validator == 'enum':
        return f'Field "{m_field}" must be one of "{error.validator_value}"'
    elif error.validator == 'additionalProperties':
        return error.message
    else:
        return error.message


def http_result(code, error_code, message, field=None):
    ret = format_http_result(code, error_code, message)
    return ret


def format_http_result(code, error_code, message):
    if is_success(code):
        return {
            'statusCode': code,
            'body': json.dumps(message, separators=(',', ':'), cls=DecimalEncoder)
        }
    else:
        return {
            'statusCode': code,
            'body': json.dumps({
                'errorCode': error_code,
                'message': message
            }, separators=(',', ':'), cls=DecimalEncoder)
        }


def error_handler(func, event, context):
    try:
        return func(event, context)
    except PalavraoError as fe:
        return json.loads(fe.message)


def is_success(code):
    return code == 200 or code == 201 or code == 204


def not_found(message, error_code=ERROR_CODE_NOT_FOUND):
    res = http_result(404, error_code, message)
    raise PalavraoError(json.dumps(res))


def internal_server_error(message, error_code):
    res = http_result(500, error_code, message)
    raise PalavraoError(json.dumps(res))


def no_content(message):
    res = http_result(204, ERROR_CODE_SUCCESS, message)
    raise PalavraoError(json.dumps(res))


def success(message):
    return http_result(200, ERROR_CODE_SUCCESS, message)


def created(message):
    return http_result(200, ERROR_CODE_SUCCESS, message)


def bad_request(message, error_code, field=None):
    res = http_result(400, error_code, message, field)
    raise PalavraoError(json.dumps(res))


def unauthorized(message, error_code=ERROR_CODE_UNAUTHORIZED):
    res = http_result(401, error_code, message)
    raise PalavraoError(json.dumps(res))


def forbidden(message, error_code=ERROR_CODE_FORBIDDEN):
    res = http_result(403, error_code, message)
    raise PalavraoError(json.dumps(res))
