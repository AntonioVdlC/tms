class InvalidNameException(ValueError):
    def __init__(self, value):
        self.value = value


class DuplicateSignupException(Exception):
    def __init__(self, email):
        self.email = email


class UnknownEmailException(Exception):
    def __init__(self, email):
        self.email = email


class ExpiredTokenException(Exception):
    def __init__(self, token):
        self.token = token


class InvalidTokenException(Exception):
    def __init__(self, token: str):
        self.token = token


class InvalidOperationException(Exception):
    def __init__(self, operation: str):
        self.operation = operation


class LogoutException(Exception):
    def __init__(self, token):
        self.token = token
