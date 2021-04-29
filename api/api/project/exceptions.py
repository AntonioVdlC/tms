class InvalidProjectNameException(Exception):
    def __init__(self, name):
        self.name = name


class UnsupportedLanguageException(Exception):
    def __init__(self, lang):
        self.lang = lang


class DuplicateProjectNameException(Exception):
    def __init__(self, name):
        self.name = name


class ProjectNotFoundException(Exception):
    def __init__(self, proj_id):
        self.proj_id = proj_id


class InvalidKeyRequestException(Exception):
    def __init__(self, value):
        self.value = value


class DuplicateKeyException(Exception):
    def __init__(self, key):
        self.key = key


class DuplicateKeyNameException(Exception):
    def __init__(self, name):
        self.name = name