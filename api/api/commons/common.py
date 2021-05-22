class UnknownSystemException(Exception):
    def __init__(self, user_id):
        self.user_id = user_id


class UnknownAuthException(Exception):
    def __init__(self):
        super(self)
