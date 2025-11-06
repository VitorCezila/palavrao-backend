import os

import boto3

from palavrao import env
from palavrao.implementations.logging import logger
from palavrao.interfaces.dao.object_converter import ObjectConverter
from palavrao.requests.utils import internal_server_error, ERROR_CODE_INTERNAL_ERROR, ERROR_CODE_CONFIG_ERROR

PARTITION_KEY_NAME = 'PK'
SORT_KEY_NAME = 'SK'


class DaoProcessor:

    def __init__(self, converter: ObjectConverter,
                 table_name: str = env.PALAVRAO_TABLE):

        if not table_name:
            logger.error("Error to init dynamodb, table name not found.")
            internal_server_error("Config error.", ERROR_CODE_CONFIG_ERROR)

        self.converter = converter
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(self.table_name)

    def put_item(self, item):
        try:
            self.table.put_item(
                Item=self.converter.to_dict(item)
            )
            logger.info(f"DynamoDB PUT_ITEM Successfully")

        except Exception as e:
            logger.exception(f"Error DynamoDB PUT_ITEM: {e}")
            internal_server_error("Error saving to database.", ERROR_CODE_INTERNAL_ERROR)

    def get_item(self, item_key):
        try:
            logger.debug(f'DynamoDB GetItem Data: key: {item_key}, converter: {self.converter.__class__.__name__}')

            response = self.table.get_item(
                Key=item_key
            )
            item = response.get('Item')
            logger.info(
                f"DynamoDB GET_ITEM: PK={item_key.get(PARTITION_KEY_NAME)}, SK={item_key.get(SORT_KEY_NAME)}. Found={bool(item)}")

            return self.converter.from_dict(item)
        except Exception as e:
            logger.exception(f"Error DynamoDB GET_ITEM: {e}")
            internal_server_error("Error getting from database.", ERROR_CODE_INTERNAL_ERROR)

    @staticmethod
    def __generate_key(item) -> str:
        key = f'{item[PARTITION_KEY_NAME]}#{item[SORT_KEY_NAME]}'
        return key