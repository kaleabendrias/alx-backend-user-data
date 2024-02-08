#!/usr/bin/env python3
"""that returns the log message obfuscated:"""
import re
import logging
import csv
from typing import List


def filter_datum(fields, redaction, message, separator):
    """helps filtering strings"""
    pattern = r'({})=(.*?)(?={})'.format(
        '|'.join(map(re.escape, fields)), re.escape(separator))
    return re.sub(pattern, r'\1={}'.format(redaction), message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields=()):
        """ Constructor method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in incoming log records """
        log_message = super().format(record)
        for field in self.fields:
            log_message = re.sub(r'{}=.*?(?=;)'.format(field),
                                 '{}={}'.format(field, self.REDACTION),
                                 log_message)
        return log_message


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger


PII_FIELDS: List[str] = ['name', 'email', 'phone', 'ssn', 'credit_card']
