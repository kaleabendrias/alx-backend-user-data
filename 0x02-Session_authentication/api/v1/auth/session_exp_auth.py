#!/usr/bin/env python3
"""add an expiration date to a Session ID."""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """add an expiration date to a Session ID"""
    def __init__(self):
        """init method"""
        session_duration_str = getenv('SESSION_DURATION')
        try:
            self.session_duration = int(session_duration_str)
        except (TypeError, ValueError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a Session ID by calling"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        if 'created_at' not in session_dict:
            return None

        created_at = session_dict['created_at']
        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if expiration_time < datetime.now():
            return None

        return session_dict.get('user_id')
