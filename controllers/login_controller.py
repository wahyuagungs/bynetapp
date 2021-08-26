import hashlib
from flask import Blueprint, render_template, session, flash, redirect, request
from services.user_service import authenticate, get_userprofile, is_token_valid, is_email_exist
from services.menu_service import get_role_byusername
from services.log_service import add_log
from utils import is_email_valid, get_random_text
from models.appuser import AppUser
from datetime import datetime
from core.email import send_email, lost_password_template_mail

login_controller = Blueprint('login_controller', __name__)


@login_controller.route('/')
def root():
    if not session.get('authenticated'):
        return render_template("login.html")
    else:
        return render_template("index.html")


@login_controller.route('/login')
def get_login():
    return render_template("login.html")


@login_controller.route('/login', methods=['POST'])
def login():
    _userid = str(request.form['username'])
    _pass = str(request.form['password'])

    if is_email_valid(_userid):
        methods = "email"
    else:
        methods = "username"

    if authenticate(_userid, _pass, methods):
        if methods == "email":
            user = AppUser()
            user.email = _userid
            _userid = AppUser.get_list(user)[0].username

        user_profile = get_userprofile(_userid)
        if not user_profile['enabled']:
            flash('You have been disabled')
            return redirect('/')
        if not user_profile['is_activated']:
            flash('You have not activated your account yet')
            return redirect('/')
        session['user'] = user_profile
        session['role'] = get_role_byusername(_userid)
        session['authenticated'] = True
        session.permanent = True
        add_log(request=request, details='Login',type=0)
    else:
        flash('wrong password!')
    return redirect('/')


@login_controller.route('/logout')
def logout():
    if not session.get("authenticated"):
        return root()
    add_log(request=request, details='Logout', type=0)
    [session.pop(key) for key in list(session.keys())]
    session.clear()
    return root()


@login_controller.route('/activate', methods=['GET'])
def get_activation_page():
    username = request.args.get('username')
    token = request.args.get('token')
    if username is None or token is None:
        raise Exception("Invalid Token")

    if is_token_valid(username, token):
        result = {'username':username, 'token':token}
        return render_template("activation.html", result=result)
    else:
        raise Exception("Invalid Token")


@login_controller.route('/activate', methods=['POST'])
def activate_user():
    username = str(request.form['username'])
    password1 = str(request.form['password1'])
    password2 = str(request.form['password2'])
    token = str(request.form['token'])

    if username is None or password1 is None or password2 is None:
        flash("You have not fill appropriate information")
        return redirect("/activate?username=" + username + "&token=" + token)

    if password1 != password2:
        flash("Your Password is not the same")
        return redirect("/activate?username=" + username + "&token=" + token)

    user = AppUser()
    user.username = username
    result = AppUser.get_list(user)
    if len(result) == 0:
        raise Exception("User does not exist")

    user = result[0]
    if user.is_activated:
        flash("User has been activated !")
        return redirect("/activate?username=" + username + "&token=" + token)

    user.password = password1
    user.consented_date = datetime.now()
    user.activation_date = datetime.now()
    user.is_activated = True
    user.save()
    add_log(request=request, details='activating account', type=0, user_id=user.id)

    # redirect to index, create login principal

    session['user'] = user.as_dict()
    session['role'] = get_role_byusername(username)
    session['authenticated'] = True

    session.permanent = True
    add_log(request=request, details='Login', type=0)
    return redirect('/')


@login_controller.route('/lostpassword', methods=['GET'])
def get_lost_account():
    return render_template("accountrecovery.html")


@login_controller.route('/lostpassword', methods=['POST'])
def renew_password():
    email = str((request.form['email']))
    if is_email_exist(email):
        user = AppUser.query.filter(AppUser.email == email).first()
        if not user.is_activated:
            flash("Your account has not been activated")
            return redirect('/lostpassword')
        token = get_random_text(30)
        user.activation_token = token
        user.save()

        send_email(user.email, "Lost Password", lost_password_template_mail(user.firstname, user.username, token))

        add_log(request=request, details='requesting new password', type=0, user_id=user.id)
        return redirect("/")
    else:
        flash('Email does not exist')
        return redirect('/lostpassword')


@login_controller.route('/changepassword', methods=['GET'])
def get_changepass_form():
    username = request.args.get('username')
    token = request.args.get('token')
    if username is None or token is None:
        raise Exception("Invalid Token")

    if is_token_valid(username, token):
        result = {'username': username, 'token': token}
        return render_template("changepassword.html", result=result)
    else:
        raise Exception("Invalid Token")


@login_controller.route('/changepassword', methods=['POST'])
def change_password():
    username = str(request.form['username'])
    password1 = str(request.form['password1'])
    password2 = str(request.form['password2'])
    token = str(request.form['token'])
    if username is None or password1 is None or password2 is None:
        flash("You have not fill appropriate information")
        return redirect("/changepassword?username=" + username + "&token=" + token)

    if password1 != password2:
        flash("Your Password is not the same")
        return redirect("/changepassword?username=" + username + "&token=" + token)

    user = AppUser()
    user.username = username
    result = AppUser.get_list(user)
    if len(result) == 0:
        return redirect("/changepassword?username=" + username + "&token=" + token)

    user = result[0]
    user.password = password1
    user.save()
    add_log(request=request, details='changing password', type=0, user_id=user.id)
    return root()
