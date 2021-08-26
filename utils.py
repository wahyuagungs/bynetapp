from flask import jsonify, session, abort, render_template, url_for
import os
from functools import wraps
import re
from exception.appexception import AppException
from exception.appexceptioncode import AppExceptionCode
from datetime import datetime
import uuid
# from controllers.login_controller import root


def authenticated_resource(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        if session.get("authenticated"):
            return function(*args, **kwargs)
        return render_template('login.html')
    return decorated


def authorised_resources(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        if session.get("authenticated"):
            return function(*args, **kwargs)
        return abort(403)  # unauthorised
    return decorated


def wrapper(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        try:
            output = function(*args, **kwargs)
        except AppException as aex:
            return error_output(str(aex), aex.get_code())
        except Exception as ex:
            print(ex)
            return error_output('AppError-9999: ' + str(ex))
        return rest_output(output)
    return decorated


def get_dbengine():
    # directory = os.path.dirname(__file__)
    # filename = os.path.join(directory, 'bnp.db')
    # db_engine = "sqlite:////" + filename
    db_engine = "postgres://pajak:docker@localhost:5432/bndb"
    # db_engine = 'mysql+pymysql://bn:Your_Password_Here@localhost/bnp'
    # db_engine = 'mysql+pymysql://bn:Your_Password_Here@localhost/bnptesting'
    return db_engine


def get_uploadfolder():
    directory = os.path.dirname(__file__)
    return os.path.join(directory, 'upload')


def get_user_id():
    return session.get('user')['id']


def get_profile():
    return session.get('user')


def get_role():
    return session.get('role')


def build_message(key, message):
    return {key: message}


def rest_output(data):
    return jsonify({"status": 1, "data": data})


def error_output(message, code=0):
    return jsonify({"status":code, "message": message})


def is_email_valid(email):
    m = re.match("[^@]+@[^@]+\.[^@]+", email)
    if m:
        return True
    else:
        return False


def get_current_date():
    return datetime.now()


# https://stackoverflow.com/a/17323913/5797504
def get_random_text(size):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())  # Convert UUID format to a Python string.
    random = random.replace("-", "")  # Remove the UUID '-'.
    return random[0:size]  # Return the random string.