from flask import Blueprint, request, json
from utils import authenticated_resource, wrapper
from models.appprofile import AppProfile
from models.project import Project
from models.projectuser import ProjectUser
from services.log_service import add_log
from exception.appexception import AppException
from exception.appexceptioncode import AppExceptionCode
from datetime import datetime
import dateutil.parser

project_controller = Blueprint('project_controller', __name__)


@project_controller.route('/api/project/add', methods=['POST'])
@authenticated_resource
@wrapper
def new_project():
    try:
        data = request.data
        d = json.loads(data)

        project = Project()
        project.update(d)
        if d['start_date'] is not None:
            project.start_date = dateutil.parser.parse(d['start_date'])
        if d['end_date'] is not None:
            project.end_date = dateutil.parser.parse(d['end_date'])
        project.save()
        add_log(request=request, details='Add Project: ' + project.title, type=1)
    except Exception as err:
        raise AppException(AppExceptionCode.CANNOT_SAVE, str(err))
    return "Success"


@project_controller.route('/api/project/edit', methods=['POST'])
@authenticated_resource
@wrapper
def edit_project():
    try:
        data = request.data
        d = json.loads(data)
        d_project = Project()
        d_project.update(d)

        project = Project.get(d_project.id)
        project.title = d_project.title
        project.description = d_project.description
        project.max_participants = d_project.max_participants
        if d['start_date'] is not None:
            project.start_date = dateutil.parser.parse(d['start_date'])
        if d['end_date'] is not None:
            project.end_date = dateutil.parser.parse(d['end_date'])
        project.is_activated = d_project.is_activated
        project.last_modified_date = datetime.now()
        project.save()
    except Exception as err:
        raise AppException(AppExceptionCode.CANNOT_SAVE, str(err))
    return "Success"


@project_controller.route('/api/project/list')
@authenticated_resource
@wrapper
def get_project_list():
    results = Project.get_list()
    return [result.as_dict() for result in results]


@project_controller.route('/api/project/users')
@authenticated_resource
@wrapper
def get_project_user_list():
    project_id = int(request.args.get('id'))
    q = ProjectUser()
    q.project_id = project_id
    data = ProjectUser.get_list(q)
    users = [user.app_user for user in data]
    return [d.as_dict() for d in users]


@project_controller.route('/api/project/users/save', methods=['POST'])
@authenticated_resource
@wrapper
def save_project_users():
    data = request.data
    d = json.loads(data)

    project = Project.get(d['project_id'])
    users = d['data']
    temps = []
    for user in users:
        if 'temp' in user:
            temps.append(user)
    if project.max_participants < (len(temps) + project.project_users.count()):
        raise AppException(AppExceptionCode.POLICY_VIOLATION, 'Maximum Participants reached')
    records = []
    for user in temps:
        pu = ProjectUser(project_id=project.id)
        pu.user_id = user['id']
        records.append(pu)

    ProjectUser.save_all(records)

    add_log(request=request, details='Assign new users to project ' + project.title, type=1)
    return "Success"


@project_controller.route('/api/project/users/delete')
@authenticated_resource
@wrapper
def delete_project_user():
    project_id = int(request.args.get('project_id'))
    user_id = int(request.args.get('user_id'))
    pu = ProjectUser()
    pu.project_id = project_id
    pu.user_id = user_id
    obj = ProjectUser.get_list(pu)[0]
    obj.delete()
    return "Success"
