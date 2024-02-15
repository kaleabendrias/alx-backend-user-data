#!/usr/bin/env python3
"""the class Session Auth"""
from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    """class SessionAuth"""
    user_id_by_session_id = {}
    
    def __init__(self) -> None:
        """init method"""
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        """creates a Session ID for a user_id"""
        if user_id is None or type(user_id) != str:
            return None
        session_id = uuid.uuid4()
        self.user_id_by_session_id[session_id] = user_id
        return session_id
