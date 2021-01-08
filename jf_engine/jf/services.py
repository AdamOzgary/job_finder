from abc import ABC

from django.contrib.auth import get_user_model, login, logout, authenticate
User = get_user_model()


class Error(Exception, ABC):
    error = None

    def __init__(self, error=None):
        self.error = None

class AuthorizationError(Exception):...

