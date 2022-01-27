import logging


class RemoveNoise(logging.Filter):
    def __init__(self):
        super().__init__()

    def filter(self, record):
        if record.levelname == 'DEBUG' and (
                '[urllib3' in record.msg or "[prawcore" in record.msg
        ):
            return False
        return True
