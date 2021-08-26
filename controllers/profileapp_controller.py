from flask import Blueprint, request, json, redirect
from utils import authenticated_resource, wrapper
from models.appprofile import AppProfile
from services.log_service import add_log
from exception.appexception import AppException
from exception.appexceptioncode import AppExceptionCode
from datetime import datetime
import dateutil.parser

profileapp_controller = Blueprint('profileapp_controller', __name__)


@profileapp_controller.route('/api/profile/save', methods=['POST'])
@authenticated_resource
@wrapper
def save_profile():
    data = request.data
    d = json.loads(data)

    profiles = AppProfile.get_list()
    if len(profiles) == 0:
        profile = AppProfile()
    else:
        profile = profiles[0]
    profile.update(d)
    profile.save()
    add_log(request=request, details='New Application profile has been added', type=1)
    return "Success"


@profileapp_controller.route('/api/profile/app', methods=['GET'])
@authenticated_resource
@wrapper
def get_profileapp():
    profile = AppProfile.get_list()
    if len(profile) > 0:
        return profile[0].as_dict()
    return 0
