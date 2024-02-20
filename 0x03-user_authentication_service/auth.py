#!/usr/bin/env python3
"""takes in a password string arguments and returns bytes."""
import bcrypt


def _hash_password(password: str) -> bytes:
    """takes in a password string arguments and returns bytes."""
    return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())
