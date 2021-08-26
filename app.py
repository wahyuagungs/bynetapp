from flask import Flask, render_template, jsonify, flash
import os
from utils import get_dbengine, get_uploadfolder
from flask_mail import Mail
from datetime import timedelta
# from werkzeug.exceptions import HTTPException

# from routes import init_error_handlers


# create the Flask application
app = Flask(__name__)
app.config['DEBUG'] = False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = get_dbengine()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = get_uploadfolder()
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'wahyuagungs@gmail.com'  # enter your email here
app.config['MAIL_DEFAULT_SENDER'] = 'wahyuagungs@gmail.com'  # enter your email here
app.config['MAIL_PASSWORD'] = 'Your_Password_Here'  # enter your password here

from models.base import db
from controllers.db_controller import db_controller
from controllers.login_controller import login_controller
from controllers.menu_controller import menu_controller
from controllers.user_controller import user_controller
from controllers.dashboard_controller import dashboard_controller
from controllers.project_controller import project_controller
from controllers.model_controller import model_controller
from controllers.profileapp_controller import profileapp_controller
from controllers.task_controller import task_controller

db.init_app(app)

# register the controllers
app.register_blueprint(db_controller)
app.register_blueprint(login_controller)
app.register_blueprint(menu_controller)
app.register_blueprint(user_controller)
app.register_blueprint(dashboard_controller)
app.register_blueprint(project_controller)
app.register_blueprint(model_controller)
app.register_blueprint(profileapp_controller)
app.register_blueprint(task_controller)

mail = Mail(app)

mail.init_app(app)

@app.errorhandler(404)
def error_404(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def error_500(e):
    flash(str(e))
    return render_template('500.html'), 500


# @app.errorhandler(Exception)
# def handle_error(e):
#     code = 500
#     if isinstance(e, HTTPException):
#         code = e.code
#     return jsonify({"status": -1, "message": str(e)}), code

if __name__ == "__main__":
    app.run(debug=False)
