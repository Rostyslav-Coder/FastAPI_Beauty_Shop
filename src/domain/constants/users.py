"""src/domain/constants/users.py"""

from enum import Enum

__all__ = ("UserRole",)


class UserRole(Enum):
    USER = "USER"
    EMPLOYEE = "EMPLOYEE"
    ADMIN = "ADMIN"
