class DuplicateSignupException(Exception):
    def __init__(self, email):
        self.email = email


class UnknownEmailException(Exception):
    def __init__(self, email):
        self.email = email


class ExpiredTokenException(Exception):
    def __init__(self, token):
        self.token = token
