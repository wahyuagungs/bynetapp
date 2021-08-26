from flask import Blueprint, render_template, session, flash, redirect, request, json
from utils import authenticated_resource, get_profile, wrapper, get_random_text
from models.appuser import AppUser
from models.refrole import RefRole
from models.appuserrole import AppUserRole
from services.log_service import add_log
from exception.appexception import AppException
from exception.appexceptioncode import AppExceptionCode
from flask import current_app
from flask_mail import Message
from threading import Thread

user_controller = Blueprint('user_controller', __name__)


@user_controller.route('/api/user/profile')
@authenticated_resource
@wrapper
def get_user_profile():
    user = AppUser.get(get_profile()['id'])
    return user.as_dict()


@user_controller.route('/api/user/list')
@authenticated_resource
@wrapper
def get_user_list():
    results = AppUser.get_list()
    output = [user.as_dict() for user in results]
    return output


@user_controller.route('/api/user/delete')
@authenticated_resource
@wrapper
def delete_user():
    user_id = int(get_profile()['id'])
    _id = int(request.args.get('id', default = user_id))
    if user_id == _id:
        raise AppException(AppExceptionCode.CANNOT_DELETE, ', You cannot delete yourself')
    else:
        user = AppUser.get(_id)
        user.delete()

        add_log(request=request, details='Delete User: ' + user.username, type=1)
        return "Successfully delete this user"


@user_controller.route('/api/user/add', methods=['POST'])
@authenticated_resource
@wrapper
def add_user():
    try:
        data = request.data
        d = json.loads(data)

        role = RefRole.get(d['roles']['ref_role'])
        del d['roles']
        user_role = AppUserRole(ref_role=role.id)

        app_user = AppUser()
        app_user.update(d)

        app_user.appuser_roles.append(user_role)
        app_user.activation_token = get_random_text(30)

        app_user.save()

        add_log(request=request, details='Add User: ' + app_user.username, type=1)
    except Exception as err:
        raise AppException(AppExceptionCode.CANNOT_SAVE, str(err))
    return "Successfully add new user"


@user_controller.route('/api/user/edit', methods=['POST'])
@authenticated_resource
@wrapper
def edit_user():
    try:
        data = request.data
        d = json.loads(data)

        role = RefRole.get(d['role']['ref_role'])
        del d['roles']

        app_user = AppUser()
        app_user.update(d)

        user = AppUser.get(app_user.id)

        if d['password'] is not None:
            user.password = d['password']

        user.appuser_roles[0].ref_role = role.id

        user.email = app_user.email
        user.is_activated = app_user.is_activated
        user.enabled = app_user.enabled
        user.phone = app_user.phone
        user.save()
    except Exception as err:
        raise AppException(AppExceptionCode.CANNOT_UPDATE, str(err))
    return "Success !"


@user_controller.route('/api/user/profile/edit', methods=['POST'])
@authenticated_resource
@wrapper
def update_profile():
    try:
        data = request.data
        d = json.loads(data)
        app_user = AppUser()
        app_user.update(d)

        user = AppUser.get(app_user.id)
        user.email = app_user.email
        user.username = app_user.username
        user.firstname = app_user.firstname
        user.lastname = app_user.lastname
        user.organisation = app_user.organisation
        user.phone = app_user.phone
        user.save()

        add_log(request=request, details='update user profile', type=0)
    except Exception as err:
        raise AppException(AppExceptionCode.CANNOT_UPDATE, str(err))
    return "Success !"


@user_controller.route('/api/user/profile/password', methods=['POST'])
@authenticated_resource
@wrapper
def change_password():
    data = request.data
    d = json.loads(data)

    user = AppUser.get(get_profile()['id'])
    if user.verify(d['old']):
        user.password = d['new']
    else:
        raise AppException(AppExceptionCode.CANNOT_UPDATE, 'Your old password does not match !')
    user.save()
    add_log(request=request, details='change password', type=0)
    return "success"


@user_controller.route('/api/user/list/active')
@authenticated_resource
@wrapper
def get_users_active():
    q = AppUser()
    q.enabled = True
    results = AppUser.get_list(q)
    users = []
    for user in results:
        for role in user.appuser_roles:
            if role.ref_role == 3:
                users.append(user)
                continue
    output = [user.as_dict() for user in users]
    return output


@user_controller.route('/api/user/sendmail')
@authenticated_resource
@wrapper
def send_activation_link():
    user_id = int(get_profile()['id'])
    _id = int(request.args.get('id', default=user_id))
    user = AppUser.get(_id)
    activation_link = 'https://bynet.app/activate?username=' + user.username + '&token=' + user.activation_token
    template = "Hey " + user.firstname + " <br>" + \
        "Thank you for your willingness to participate in this research. <br>" + \
        "Before we begin, first you need to give us your consent by activating your account " + \
        "and create your own password through this link " + \
        '<a href="' + activation_link + '">' + activation_link + '</a>. <br>' + \
        'Your username is <strong>' + user.username + '</strong> or your email address. <br>' + \
        'If you have any queries please feel free to contact us. <br>' + \
        'Regards. <br>' + \
        'Wahyu Agung Sugimartanto <br>' + \
        'ByNet App Team'
    send_email(user.email, "ByNet Account - Activation Required", template)


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    from app import mail as m
    m.send(msg)
