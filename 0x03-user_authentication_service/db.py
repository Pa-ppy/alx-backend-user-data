#!/usr/bin/env python3
"""
DB module to manage User objects and interactions with the database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """
    DB class to handle database operations for the User model.
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance and create tables.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object.
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email: The user's email.
            hashed_password: The user's hashed password.

        Returns:
            The created User object.
        """
        user = User(email=email, hashed_password=hashed_password)
        self._session.add(user)
        self._session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find the first user that matches the filter criteria.

        Args:
            kwargs: Arbitrary keyword arguments for filtering.

        Returns:
            The first User object matching the criteria.

        Raises:
            NoResultFound: If no user is found.
            InvalidRequestError: If query parameters are invalid.
        """
        if not kwargs:
            raise InvalidRequestError("No filter arguments provided.")
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except NoResultFound:
            raise
        except InvalidRequestError:
            raise

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update user attributes by user_id.

        Args:
            user_id: The ID of the user to update.
            kwargs: Attributes to update.

        Raises:
            ValueError: If an attribute is invalid.
        """
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)
        self._session.commit()
