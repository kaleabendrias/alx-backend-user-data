#!/usr/bin/env python3
"""session db auth"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """new authentication class"""
    def create_session(self, user_id=None):
        """creates and stores new instance of UserSession"""
        try:
            session_id = super().create_session(user_id)
        except Exception:
            return None

        if type(session_id) is str:
            kwargs = {
                "user_id": user_id,
                "session_id": session_id
            }
            user_session = UserSession(**kwargs)
            user_session.save()

            return session_id

    def user_id_for_session_id(self, session_id=None):
        """returns the User ID by requesting UserSession"""
        if not session_id:
            return None
        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})
        if not user_session:
            return None

        created = user_session[0].created_at
        session_time = timedelta(seconds=self.session_duration)

        if created + session_time < datetime.now():
            return None

        return user_session[0].user_id

    def destroy_session(self, request=None):
        """destroys the UserSession based on the Session ID"""
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({"session_id": session_id})
        except Exception:
            return False

        if len(sessions) <= 0:
            return False

        sessions[0].remove()

        return True
