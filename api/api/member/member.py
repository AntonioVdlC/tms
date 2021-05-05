from flask import Blueprint, current_app, request, jsonify, g
from pydantic import ValidationError

from api.member import manager
from api.member.exceptions import *
from api.commons.organisation import DeletedOrganisationAccessException, OrganisationIllegalAccessException, \
    OrganisationNotFoundException
from api.commons.common import UnknownSystemException
from api.commons.user import UserNotFoundException


blueprint = Blueprint('member', __name__, url_prefix='/organisations/<string:org_id>/members')


@blueprint.route('', methods=['GET'])
def get_members(org_id: str):
    return {"message": f"get members for {org_id}"}
