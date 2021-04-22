class InvalidOrgNameException(ValueError):
    def __init__(self, value):
        self.value = value


class OrganisationCreationException(Exception):
    def __init__(self, organisation_name, user_id):
        self.organisation_name: organisation_name
        self.user_id = user_id


class OrganisationNotFoundException(Exception):
    def __init__(self, org_id):
        self.org_id = org_id


class OrganisationIllegalAccessException(Exception):
    def __init__(self, org_id, user_id):
        self.org_id = org_id
        self.user_id = user_id


class UnknownSystemException(Exception):
    def __init__(self, user_id):
        self.user_id = user_id