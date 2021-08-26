from models.accesslog import AccessLog
from utils import get_user_id


def add_log(**kwargs):
    log = AccessLog()
    if 'request' in kwargs:
        request = kwargs['request']
        log.ip_address = request.remote_addr
        log.browser_agent = request.headers.get('User-Agent')
    if 'details' in kwargs:
        log.activity = kwargs['details']
    if 'type' in kwargs:
        log.activity_type = kwargs['type']

    if "user_id" in kwargs:
        log.user = kwargs['user_id']
    else:
        log.user = get_user_id()
    log.save()


def get_log_activities():
    # displaying related activities, with activity type=0
    user_id = get_user_id()
    result = AccessLog.query.filter_by(activity_type=0,user=user_id).order_by(AccessLog.creation_date.desc()).limit(10).all()
    output = []
    for l in result:
        temp = {
            'label': '{0} was {1} at {2}'.format(l.app_user.username, l.activity, l.creation_date.strftime("%Y-%m-%d %H:%M:%S"))
        }
        output.append(temp)
    return output


def get_other_activities():
    result = AccessLog.query.filter_by(activity_type=1).order_by(AccessLog.creation_date.desc()).limit(10).all()
    output = []
    for l in result:
        temp = {
            'label': '{0} by {1} at {2}'.format(l.activity, l.app_user.username, l.creation_date.strftime("%Y-%m-%d %H:%M:%S"))
        }
        output.append(temp)
    return output


