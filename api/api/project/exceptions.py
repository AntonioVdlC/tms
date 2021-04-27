class InvalidProjectNameException(Exception):
    def __init__(self, name):
        self.name = name


class UnsupportedLanguageException(Exception):
    def __init__(self, lang):
        self.lang = lang


class DuplicateProjectNameException(Exception):
    def __init__(self, name):
        self.name = name


class ProjectNotFoundExeption(Exception):
    def __init__(self, proj_id):
        self.proj_id = proj_id