from flask import current_app, g
from pydantic import BaseModel, validator
from bson.objectid import ObjectId
from pymongo.errors import WriteError

from api.utils.cache import get_cache
from api.organisation.exceptions import *
from api.models.user import add_organisation_to_user
from api.models.organisation import insert_organisation
from api.utils.db import get_client
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
    try:
        object_id = ObjectId()
        current_app.logger.info(f'Adding organisation with name {organisation_name} by user {g.user_id} with '
                                f'object id {str(object_id)}')
        with get_client().start_session() as session:
            with session.start_transaction():
                organisation = insert_organisation(organisation_name, g.user_id, object_id, session)
                add_organisation_to_user(g.user_id, str(organisation.object_id), session)
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
