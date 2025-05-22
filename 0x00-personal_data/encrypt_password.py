#!/usr/bin/env python3
"""
Module for securely hashing and validating passwords using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """Hashes a password using bcrypt with salt."""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Validates that the provided password matches the hashed password."""
    return bcrypt.checkpw(password.encode(), hashed_password)
