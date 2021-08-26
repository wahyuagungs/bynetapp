from models.appuser import AppUser

from models.base import db
from exception.appexception import AppException
from exception.appexceptioncode import AppExceptionCode


def authenticate(_userid, _password, methods):
    result = []
    if methods == "email" :
        result = AppUser.query.filter(AppUser.email == _userid).all()
    elif methods == 'username':
        result = AppUser.query.filter(AppUser.username == _userid).all()

    if len(result) > 0:
        user = result[0]
        if user.verify(_password):
            return True
    return False


def get_userprofile(username):
    user = AppUser.query.filter(AppUser.username == username).first()
    return user.as_dict()


def is_email_exist(email):
    user = AppUser.query.filter_by(email=email).all()
    if len(user) > 0:
        return True
    return False


def is_username_exist(username):
    user = AppUser.query.filter_by(username=username).first().as_dict()
    if len(user) > 0:
        return True
    return False


def update_profile(user):
    try:
        updated_user = AppUser.get(user.id)
        updated_user.firstname = user.firstname
        updated_user.lastname = user.lastname
        updated_user.email = user.email
        updated_user.password = user.password
        updated_user.organisation = user.organisation
    except Exception as err:
        raise print(err)

# def get_user_byid(id):
#     user = AppUser.query.filter_by(id=id).first()
#     return user.as_dict()


def is_token_valid(username, token):
    user = AppUser.query.filter(AppUser.username == username, AppUser.activation_token == token).all()
    if len(user) > 0:
        return True
    return False


