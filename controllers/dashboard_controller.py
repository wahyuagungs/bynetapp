from flask import Blueprint, render_template, session, flash, redirect, request
from services.menu_service import get_menu_idrole
from utils import authenticated_resource, wrapper
from services.log_service import get_log_activities, get_other_activities
from models.appprofile import AppProfile
from models.accesslog import AccessLog

dashboard_controller = Blueprint('dashboard_controller', __name__)


@dashboard_controller.route('/api/dashboard/information')
@authenticated_resource
@wrapper
def get_information():
    '''
    This will return application profile as dictionary
    '''
    info = AppProfile.get_list()
    if not info:
        return None
    return info[0].as_dict()


@dashboard_controller.route('/api/dashboard/access')
@authenticated_resource
@wrapper
def get_access_activities():
    return get_log_activities()


@dashboard_controller.route('/api/dashboard/recent')
@authenticated_resource
@wrapper
def get_recent_activities():
    return get_other_activities()



