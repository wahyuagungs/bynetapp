from flask import Blueprint, request, json, redirect
from utils import authenticated_resource, wrapper, get_user_id, get_current_date
from werkzeug.utils import secure_filename
import os
from flask import current_app
from models.base import db
from models.project import Project
from models.model import Model
from models.variable import Variable
from models.state import State
from models.probability import Probability
from models.probabilitystate import ProbabilityState
from models.arc import Arc
from models.tag import Tag
from services.log_service import add_log
from exception.appexception import AppException
from exception.appexceptioncode import AppExceptionCode
from itertools import product
from datetime import datetime
import dateutil.parser
import re

model_controller = Blueprint('model_controller', __name__)

ALLOWED_EXTENSIONS = set(['txt', 'csv'])


@model_controller.route('/api/model/list')
@authenticated_resource
@wrapper
def get_model():
    project_id = int(request.args.get('id'))
    q = Model()
    q.project_id = project_id
    data = Model.get_list(q)
    return [d.as_dict() for d in data]


@model_controller.route('/uploadFile', methods=['POST'])
@authenticated_resource
def upload_file():
    try:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # seek to the beginning of file
            file.stream.seek(0)
            # open and read the file
            stream = file.read().decode("utf-8")
            model = Model()
            model.data_content = stream

            model.project_id = request.values.get('project_id')
            model.save()
            # close the file
            file.close()
            # remove the file
            os.remove(file_path)
            return "Successfully upload the file"
        else:
            return "File is not allowed"
    except Exception as ex:
        print(ex)
        return redirect('/500')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@model_controller.route('/api/model/save', methods=['POST'])
@authenticated_resource
@wrapper
def save_model():
    data = request.data
    d = json.loads(data)
    model = Model()
    model.data_content = d['data_content']
    model.project_id = d['project_id']
    model.save()
    add_log(request=request, details='Add new model', type=1)
    return "Success"


@model_controller.route('/api/model/load', methods=['GET'])
@authenticated_resource
@wrapper
def load_model():
    model_id = int(request.args.get('id'))

    model = Model.get(model_id)
    if model is None:
        raise AppException(AppExceptionCode.NOT_FOUND_ERROR)

    counts = Project.get(model.project_id).models.count()

    content = str(model.data_content)
    d_var = {}
    d_val = {}
    for line in content.splitlines():
        if line.startswith('var,'):
            # parse 'var'
            attr = line.split(',')[1]
            objs = attr.split(':')

            # save Variable Object
            var = Variable()
            var.label = objs[0]
            var.description = 'P({0})'.format(objs[0])
            var.model_id = model.id
            var.created_by = get_user_id()

            # save State Objects
            states = objs[1].split(';')
            for s in states:
                state = State()
                state.label = s
                state.description = '{0}={1}'.format(var.label, state.label)
                var.states.append(state)
                # state.variable_id = var.id
                db.session.add(state)

            db.session.add(var)
            db.session.flush()
            d_var[var.label] = var

        elif line.startswith('value:'):
            objs = line.split(':')[1]
            vals = objs.split(';')
            for obj in vals:
                sts = obj.split('=')
                d_val[sts[0]] = sts[1].split(',')

        elif line.startswith('rel:'):
            objs = line.split(':')[1]
            d_state = {}
            for pair in objs.split(';'):
                attr = pair.split(',')
                # save Arc objects
                if len(attr) == 1:
                    child = attr[0]
                    arc = Arc()
                    arc.child_id = d_var[child].id
                    d_state[child] = {'child': d_var[child], 'parents': []}
                else:
                    parent = attr[0]
                    child = attr[1]
                    arc = Arc()
                    arc.child_id = d_var[child].id
                    arc.parent_id = d_var[parent].id
                    if child not in d_state:
                        d_state[child] = {'child': d_var[child], 'parents': []}
                        d_state[child]['parents'].append(d_var[parent])
                    else:
                        d_state[child]['parents'].append(d_var[parent])
                db.session.add(arc)
                db.session.flush()
            # save probability objects
            for k, v in d_state.items():
                # Brand, Type, Price
                if len(v['parents']) == 0:
                    var = v['child']
                    x = 0
                    for state in var.states:
                        p = Probability()
                        p.state_id = state.id
                        if var.label in d_val:
                            p.value = d_val[var.label][x]
                        db.session.add(p)
                        db.session.flush()
                        x += 1
                else:
                    # create pool
                    parents = v['parents']
                    child = v['child']
                    pool = [parent.states for parent in parents]

                    expanded_grid = list(product(*pool))
                    x = 0
                    for state in child.states:
                        for rig in expanded_grid:
                            p = Probability()
                            p.state_id = state.id
                            if child.label in d_val:
                                p.value = d_val[child.label][x]
                            db.session.add(p)
                            db.session.flush()
                            for each_rig in rig:
                                ps = ProbabilityState()
                                ps.probability_id = p.id
                                ps.state_id = each_rig.id
                                db.session.add(ps)
                                db.session.flush()
                            x += 1
        elif line.startswith('tag:'):
            objs = line.split(':')[1]
            vals = objs.split(';')
            for t in vals:
                tag = Tag()
                tag.label = t
                tag.model_id = model.id
                db.session.add(tag)
                db.session.flush()
        else:
            raise AppException(AppExceptionCode.INVALID_FORMAT)

    model.has_loaded = True
    model.total_variables = len(d_var)

    # update version
    version = '{0}.{1}.{2}'.format(str(get_current_date().year),str(get_current_date().month), str(counts))
    model.version = version
    db.session.add(model)
    db.session.commit()
    add_log(request=request, details='Load model ' + version + ' to project ' + model.project.title, type=1)
    return "Success"


@model_controller.route('/api/model/activate', methods=['GET'])
@authenticated_resource
@wrapper
def activate_model():
    model_id = int(request.args.get('id'))
    model = Model.get(model_id)
    if model is None:
        raise AppException(AppExceptionCode.NOT_FOUND_ERROR)
    if not model.has_loaded:
        raise AppException(AppExceptionCode.ILLEGAL_ARGUMENT)

    # disabled the rest based on project id
    q = Model()
    q.project_id = model.project_id
    q.is_active = True
    models = Model.get_list(q)
    for m in models:
        m.is_active = False
        db.session.add(m)
        db.session.flush()

    model.is_active = True
    db.session.add(model)
    db.session.commit()

    add_log(request=request, details='Activate model ' + model.version + ' in project ' + model.project.title, type=1)
    q = Model()
    q.project_id = model.project_id
    data = Model.get_list(q)
    return [d.as_dict() for d in data]


@model_controller.route('/api/model/disable', methods=['GET'])
@authenticated_resource
@wrapper
def disable_model():
    model_id = int(request.args.get('id'))
    model = Model.get(model_id)
    if model is None:
        raise AppException(AppExceptionCode.NOT_FOUND_ERROR)
    if not model.has_loaded:
        raise AppException(AppExceptionCode.ILLEGAL_ARGUMENT)

    model.is_active = False
    model.save()

    q = Model()
    q.project_id = model.project_id
    data = Model.get_list(q)
    return [d.as_dict() for d in data]


@model_controller.route('/api/model/tag/add', methods=['POST'])
@authenticated_resource
@wrapper
def add_tag():
    data = request.data
    d = json.loads(data)
    tag = Tag()
    tag.update(d)

    tags = Tag.query.filter(Tag.model_id == tag.model_id,
                            Tag.label.like('%' + tag.label.strip().lower() + '%')).all()
    if len(tags) > 0:
        raise AppException(AppExceptionCode.CANNOT_SAVE, 'Similar Category has existed')

    tag.save()


@model_controller.route('/api/model/tag/list', methods=['GET'])
@authenticated_resource
@wrapper
def get_tag():
    model_id = int(request.args.get('id'))
    model = Model.get(model_id)
    if model is None:
        raise AppException(AppExceptionCode.NOT_FOUND_ERROR)
    if not model.has_loaded or not model.is_active:
        raise AppException(AppExceptionCode.ILLEGAL_ARGUMENT)

    q = Tag()
    q.model_id = model_id
    tags = Tag.get_list(q)

    results = []
    for t in tags:
        results.append({'id': t.id, 'label': t.label})
    return results
