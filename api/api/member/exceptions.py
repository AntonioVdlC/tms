class DuplicateAddMemberException(Exception):
    def __init__(self, email):
        self.email = email


class InsufficientOwnerAccessException(Exception):
    def __init__(self, user_id):
        self.user_id = user_id
