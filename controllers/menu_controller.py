from flask import Blueprint, render_template, session, flash, redirect, request
from services.menu_service import get_menu_idrole
from utils import authenticated_resource, get_role, wrapper

menu_controller = Blueprint('menu_controller', __name__)


@menu_controller.route('/api/menu')
@authenticated_resource
@wrapper
def get_menu():
    id_role = get_role()['id']
    out = get_menu_idrole(id_role)
    return out
