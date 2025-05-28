#!/usr/bin/env python3
"""Auth module - base authentication class"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Template for authentication system"""

    def require_auth(self, path: str, excluded_paths: list) -> bool:
        """Determines if authentication is required for a given path"""
        if path is None or excluded_paths is None or excluded_paths == []:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded in excluded_paths:
            if excluded.endswith('*'):
                if path.startswith(excluded[:-1]):
                    return False
            else:
                if excluded.endswith('/') and path == excluded:
                    return False
                if not excluded.endswith('/') and path == excluded + '/':
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """Get Authorization header"""
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Retrieve current user"""
        return None
