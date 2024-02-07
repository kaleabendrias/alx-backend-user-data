#!/usr/bin/env python3
"""that returns the log message obfuscated:"""
import re
import logging


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields=()):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields


    def format(self, record: logging.LogRecord) -> str:
        log_message = super().format(record)
        for field in self.fields:
            log_message = re.sub(r'{}=.*?(?=;)'.format(field), '{}={}'.format(field, self.REDACTION), log_message)
        return log_message
