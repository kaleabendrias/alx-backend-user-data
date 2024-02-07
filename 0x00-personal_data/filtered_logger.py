#!/usr/bin/env python3
"""that returns the log message obfuscated:"""
import re


def filter_datum(fields, redaction, message, separator):
    """that returns the log message obfuscated:"""
    pattern = r'({})=(.*?)(?={})'.format('|'.join(fields),
                                         re.escape(separator))
    return re.sub(pattern, r'\1={}'.format(redaction), message)
