#!/usr/bin/env python3
"""the class Auth"""
from flask import request
from typing import List, TypeVar


class Auth:
    """class named Auth"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth"""
        pass

    def authorization_header(self, request=None) -> str:
        """that returns None - request will be the Flask request object"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """that returns None - request will be the Flask request object"""
        return None
