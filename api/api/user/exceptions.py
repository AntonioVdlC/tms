class DuplicateEmailException(Exception):
    def __init__(self, email_id):
        self.email_id = email_id


class DuplicateUpdateRequestException(Exception):
    def __init__(self, email_id):
        self.email_id = email_id


class UnknownUpdateEmailException(Exception):
    def __init__(self, user_id):
        self.user_id = user_id


class UnknownEmailTypeException(Exception):
    def __init__(self, token, email_type):
        self.token = token
        self.email_type = email_type


class IllegalUpdateTokenException(Exception):
    def __init__(self, token):
        self.token = token
