#!/usr/bin/env python3
"""
Auth module for authentication logic.
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt with a salt.

    Args:
        password: The plain password to hash.

    Returns:
        The hashed password as bytes.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


class Auth:
    """
    Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """Initialize a new Auth instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user if the email is not already taken.

        Args:
            email: The user's email.
            password: The user's password.

        Returns:
            The newly created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed = _hash_password(password)
            return self._db.add_user(email, hashed.decode('utf-8'))
