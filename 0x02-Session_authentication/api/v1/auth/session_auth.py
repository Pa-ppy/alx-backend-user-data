#!/usr/bin/env python3
"""Session authentication module"""

from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Session authentication class (empty for now)"""

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return user ID by session ID"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Return a User instance based on a cookie value"""
        session_id = self.session_cookie(request)
        if session_id is None:
            return None
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return None
        return User.get(user_id)
