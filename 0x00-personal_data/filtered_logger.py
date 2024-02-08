#!/usr/bin/env python3
"""that returns the log message obfuscated:"""
import re
import logging
import csv
from typing import List


def filter_datum(fields, redaction, message, separator):
    """filtering strings"""
    pattern = r'({})=(.*?)(?={})'.format(
        '|'.join(map(re.escape, fields)), re.escape(separator))
    return re.sub(pattern, r'\1={}'.format(redaction), message)
