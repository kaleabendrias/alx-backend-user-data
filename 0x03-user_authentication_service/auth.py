#!/usr/bin/env python3
"""takes in a password string arguments and returns bytes."""
from db import DB
import bcrypt
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """takes in a password string arguments and returns bytes."""
    return bcrypt.hashpw(bytes(password, 'utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """should return a string representation of a new UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Return a User object."""
        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            new_user = self._db.add_user(email, hashed_pwd)
        return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """validates login"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                password = bytes(password, "utf-8")
                if bcrypt.checkpw(password, user.hashed_password):
                    return True
                return False
        except NoResultFound:
            return False
