from threading import Thread
from flask import current_app, render_template
from flask_mail import Message


def send_async_email(app, msg):
    with app.app_context():
        from app import mail
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    msg = Message(subject, recipients=[to])
    msg.html = template
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


def lost_password_template_mail(firstname, username, token):
    link = 'https://bynet.app/changepassword?username=' + username + '&token=' + token
    body = 'Hey ' + firstname + ' <br>' +\
        'To change your password please visit this link <a href="' + link + '">' + link + '</a>. <br>' + \
        'Thank you.'
    return body
