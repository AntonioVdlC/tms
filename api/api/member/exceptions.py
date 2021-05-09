class DuplicateAddMemberException(Exception):
    def __init__(self, email, first_name, last_name):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name


class InsufficientOwnerAccessException(Exception):
    def __init__(self, user_id):
        self.user_id = user_id


class UnknownMemberException(Exception):
    def __init__(self, member_id):
        self.member_id = member_id


class UnknownInviteException(Exception):
    def __init__(self, invite_id):
        self.invite_id = invite_id