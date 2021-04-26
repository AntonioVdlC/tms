class UnsupportedLanguageException(Exception):
    def __init__(self, lang):
        self.lang = lang


class DuplicateProjectNameException(Exception):
    def __init__(self, name):
        self.name = name
