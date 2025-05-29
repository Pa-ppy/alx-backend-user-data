#!/usr/bin/env python3
"""BasicAuth class for Basic Authentication"""
from api.v1.auth.auth import Auth
from typing import Tuple
from models.user import User


class BasicAuth(Auth):
    """Basic authentication class"""

    def extract_base64_authorization_header(
            self, authorization_header: str
    ) -> str:
        """Extract Base64 part of Authorization header"""
        if authorization_header is None or not isinstance(
            authorization_header, str
        ):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split(' ', 1)[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str
    ) -> str:
        """Decode a Base64-encoded authorization header"""
        import base64
        if base64_authorization_header is None or not isinstance(
            base64_authorization_header, str
        ):
            return None
        try:
            decoded_bytes = base64.b64decode(
                base64_authorization_header, validate=True)
            return decoded_bytes.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """Extract user email and password (handle colons in password)"""
        if decoded_base64_authorization_header is None or not isinstance(
            decoded_base64_authorization_header, str
        ):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(self, user_email: str, user_pwd: str):
        """Returns the User instance based on email and password"""
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        try:
            users = User.search({"email": user_email})
        except Exception:
            return None

        if not users:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None):
        """Retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        if not auth_header:
            return None

        b64 = self.extract_base64_authorization_header(auth_header)
        if not b64:
            return None

        decoded = self.decode_base64_authorization_header(b64)
        if not decoded:
            return None

        email, pwd = self.extract_user_credentials(decoded)
        if not email or not pwd:
            return None

        return self.user_object_from_credentials(email, pwd)
