#!/usr/bin/env python3
"""returns a salted, hashed password, which is a byte string"""
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string."""
    password = password.encode('utf-8')
    hashed = bcrypt.hashpw(password, bcrypt.gensalt(14))
    return hashed