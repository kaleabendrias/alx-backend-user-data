#!/usr/bin/env python3
"""session db auth"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """new authentication class"""
    def create_session(self, user_id=None):
        """creates and stores new instance of UserSession"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        user_session = UserSession({"user_id": user_id,
                                    "session_id": session_id})
        user_session.save()
        user_session.save_to_file()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID by requesting UserSession"""
        if not session_id:
            return None
        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return None

        return user_session[0].user_id

    def destroy_session(self, request=None):
        """destroys the UserSession based on the Session ID"""
        if not request:
            return None
        session_id = self.session_cookie(request)
        if not session_id or not self.user_id_for_session_id(session_id):
            return None
        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return None
        user_session[0].remove()
        UserSession.save_to_file()
        return True
