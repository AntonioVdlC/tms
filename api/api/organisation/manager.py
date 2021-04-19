from flask import current_app, g
from pydantic import BaseModel, validator
from pymongo.errors import WriteError

from api.utils.cache import get_cache
from api.organisation.exceptions import *
from api.models.user import add_organisation_to_user
from api.models.organisation import insert_organisation
from datetime import datetime


class CreateOrganisationRequest(BaseModel):
    organisation_name: str

    @validator('organisation_name')
    def validate_organisation_name(cls, v):
        if '$' in v:
            raise InvalidOrgNameException(v)
        return v


class CreateOrganisationResponse(BaseModel):
    organisation_name: str
    organisation_id: str
    created_at: datetime


def create_organisation(request: CreateOrganisationRequest) -> CreateOrganisationResponse:
    organisation_name = str(request.organisation_name)
    # this is not using session or transaction because object id obtained automatically from inserting organisation
    # cant be used within the same session to update for user. for now, let this be. if we see issues with this approach
    # we can address it later. else, generating object id's would be over engineering at this point
    # added the org name and creator id in logs if a cleanup is required.
    # lack of transactions here is a hack. but so is the developer (he can personally attest to the claim).
    # he just figured if he can live with himself, he can live with this hack for now.
    try:
        organisation = insert_organisation(organisation_name, g.user_id)
        add_organisation_to_user(g.user_id, str(organisation.object_id))
        clear_user_cache(g.user_id)
    except WriteError as we:
        current_app.logger.error(f'issue creating organisation, org name: {organisation_name}. creator_id: {g.user_id}')
        raise OrganisationCreationException(organisation_name, g.user_id)

    response = CreateOrganisationResponse(organisation_name=organisation.name,
                                          organisation_id=str(organisation.object_id),
                                          created_at=organisation.created_at)
    return response


def clear_user_cache(user_id: str):
    key = f'user_{user_id}'
    get_cache().delete(key)
