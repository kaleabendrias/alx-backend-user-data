#!/usr/bin/env python3
"""that returns the log message obfuscated:"""
import re
import logging
from typing import List
import os
import mysql.connector


PII_FIELDS: List[str] = ['name', 'email', 'phone', 'ssn', 'credit_card']


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """helps filtering strings"""
    pattern = r'({})=(.*?)(?={})'.format(
        '|'.join(map(re.escape, fields)), re.escape(separator))
    return re.sub(pattern, r'\1={}'.format(redaction), message)


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


def get_db():
    """Returns a connector to the database."""
    username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")

    db = mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=db_name
    )

    return db


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class"""
    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Constructor method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Filters values in incoming log records """
        log_message = super().format(record)
        for field in self.fields:
            log_message = filter_datum
            ([field], self.REDACTION, log_message, self.SEPARATOR)
        return log_message
