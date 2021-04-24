from flask import current_app, g
from pydantic import BaseModel, validator

import json
import locale
from datetime import datetime

from api.utils.cache import get_cache
from api.project.exceptions import *
from api.models.user import User, get_user_by_id
from api.commons import user as user_commons
from api.commons import organisation as organisation_commons

supported_langs = set(locale.locale_alias.keys())


class ProjectRequest(BaseModel):
    project_name: str
    langs: list

    @validator('langs')
    def validate_langs(cls, langs):
        global supported_langs
        for lang in langs:
            if lang not in supported_langs:
                raise UnsupportedLanguageException(lang)
        return langs


class ProjectResponse(BaseModel):
    project_name: str
    langs: list
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

