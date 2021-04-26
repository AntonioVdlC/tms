class InvalidOrgNameException(ValueError):
    def __init__(self, value):
        self.value = value


class OrganisationCreationException(Exception):
    def __init__(self, organisation_name, user_id):
        self.organisation_name: organisation_name
        self.user_id = user_id

