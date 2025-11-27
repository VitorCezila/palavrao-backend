from aws_lambda_powertools import Logger

class PalavraoLogger(Logger):
    def __init__(self):
        super().__init__()


logger = PalavraoLogger()