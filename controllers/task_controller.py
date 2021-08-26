from flask import Blueprint, request, current_app, json
from models.initdb import db
from utils import authenticated_resource, wrapper, get_user_id, get_profile
from models.project import Project
from models.projectuser import ProjectUser
from models.model import Model
from models.variable import Variable
from models.state import State
from models.probability import Probability
from models.probabilitystate import ProbabilityState
from models.stage import Stage
from models.weight import Weight
from models.refstage import RefStage
from models.arc import Arc
from models.cpc import CPC
from models.cpcstate import CPCState
from models.tag import Tag
from models.varalloctag import VariableAllocationTag
from models.variableallocation import VariableAllocation
from models.elicitedprob import ElicitedProb
from services.log_service import add_log
from exception.appexception import AppException
from exception.appexceptioncode import AppExceptionCode
from datetime import datetime
from services.task_service import get_parents_from_child,get_all_states__by_varid,get_parent_states_from_child,get_variable_from_state_id

task_controller = Blueprint('task_controller', __name__)


@task_controller.route('/api/task/list')
@authenticated_resource
@wrapper
def get_projects():
    user_id = get_user_id()
    q = ProjectUser()
    if q is None:
        return None
    q.user_id = user_id
    pu = ProjectUser.get_list(q)
    data = []
    if len(pu) == 0:
        return None
    for pid in pu:
        p = Project.get(pid.project_id)
        m = Model()
        m.is_active = True
        m.project_id = pid.project_id
        d_p = p.as_dict()

        model = Model.get_list(m)
        # if a project has have any model
        if len(model) > 0:
            d_p['model'] = model[0].as_dict()

            # query stage by user_id
            s = Stage()
            s.model_id = model[0].id
            s.user_id = get_user_id()
            stages = Stage.get_list(s)
            if len(stages) > 0:
                d_p['stage'] = [s.as_dict() for s in model[0].stages]

                # count the progress
                d_p['progress'] = get_progress(model[0].id)
            else:
                d_p['stage'] = None
                d_p['progress'] = 0
        else:
            d_p['model'] = None
        data.append(d_p)

    return data


@task_controller.route('/api/task/model/get')
@authenticated_resource
@wrapper
def get_model_construction():
    user_id = get_user_id()
    model_id = int(request.args.get('id'))
    model = Model.get(model_id)
    if model is None:
        raise AppException(AppExceptionCode.NOT_FOUND_ERROR)

    if not model.is_active and not model.has_loaded:
        raise AppException(AppExceptionCode.FAILED_QUERY_PROCESS)

    # get the variables
    vars = []
    arcs = []
    for v in model.variables:
        vars.append(v)
        q = Arc()
        q.child_id = v.id
        arcs_var = Arc.get_list(q)
        arcs.append(arcs_var)

    result = {'nodes': [d.as_dict() for d in vars],
              'arcs': [item.as_dict() for sublist in arcs for item in sublist]}
    return result


@task_controller.route('/api/task/survey/start')
@authenticated_resource
@wrapper
def construct_survey_skeleton():
    model_id = int(request.args.get('id'))

    model = Model().get(model_id)
    if model is None:
        raise AppException(AppExceptionCode.NOT_FOUND_ERROR)

    q = Stage()
    q.user_id = get_user_id()
    q.model_id = model_id
    stages_user = Stage.get_list(q)
    # generate stage, probability states, etc.
    if len(stages_user) > 0:
        return None
    else:
        # stage
        stage_1 = Stage()
        stage_1.ref_stage_id = 1
        stage_1.user_id = get_user_id()
        stage_1.model_id = model_id
        stage_1.start = datetime.now()
        db.session.add(stage_1)
        db.session.flush()

        stage_2 = Stage()
        stage_2.ref_stage_id = 2
        stage_2.user_id = get_user_id()
        stage_2.model_id = model_id
        db.session.add(stage_2)
        db.session.flush()

        stage_3 = Stage()
        stage_3.ref_stage_id = 3
        stage_3.user_id = get_user_id()
        stage_3.model_id = model_id
        db.session.add(stage_3)
        db.session.flush()

        stage_4 = Stage()
        stage_4.ref_stage_id = 4
        stage_4.user_id = get_user_id()
        stage_4.model_id = model_id
        db.session.add(stage_4)
        db.session.flush()

        stage_5 = Stage()
        stage_5.ref_stage_id = 5
        stage_5.user_id = get_user_id()
        stage_5.model_id = model_id
        db.session.add(stage_5)
        db.session.flush()

        stage_6 = Stage()
        stage_6.ref_stage_id = 6
        stage_6.user_id = get_user_id()
        stage_6.model_id = model_id
        db.session.add(stage_6)
        db.session.flush()

        # variable allocation
        # find all variables and divide them based on each stage
        q = Variable()
        q.model_id = model_id
        vars = Variable.get_list(q)
        alloc = []
        for v in vars:
            # check if v has probabilities
            results = db.session.query(Probability.value).join(State, Variable).filter(Variable.id == v.id).all()
            results = [value for (value,) in results]
            if None not in results:
                continue
            # determine stages
            a = Arc()
            a.child_id = v.id
            arcs = Arc.get_list(a)

            # wrong assumption here!
            # len(arcs) ==  1 - meaning that it can be both single parent or no parent !
            # solution: put these condition together, such that if the parent 
            if len(arcs) == 0:
                print('Variable with No Arcs')
                raise AppException(AppExceptionCode.POLICY_VIOLATION, 'Variable with No Arcs !')
            elif len(arcs) == 1:
                # we only have 1 arc
                arc = arcs[0]
                if arc.parent_id is None:
                    # for no parent
                    # stage 1 - no parents
                    va = VariableAllocation()
                    va.variable_id = arc.child_id
                    va.stage_id = stage_1.id
                    db.session.add(va)
                    db.session.flush()
                    # elicited prob
                    # child_id is variable_id to find states
                    s = State()
                    s.variable_id = arc.child_id
                    states = State.get_list(s)
                    # states have all the possible state
                    # 1, 2, 3
                    for state in states:
                        for p in state.probabilities:
                            ep = ElicitedProb()
                            ep.probability_id = p.id
                            ep.var_alloc_id = va.id 
                            db.session.add(ep)
                            db.session.flush()
                else:
                    # single parent
                    # stage 2 - parents only 1
                    va = VariableAllocation()
                    va.variable_id = arc.child_id
                    va.stage_id = stage_2.id
                    db.session.add(va)
                    db.session.flush()
                    # elicited prob
                    s = State()
                    s.variable_id = arc.child_id
                    states = State.get_list(s)
                    # states have all the possible state
                    # 1, 2, 3
                    for state in states:
                        for p in state.probabilities:
                            ep = ElicitedProb()
                            ep.probability_id = p.id
                            ep.var_alloc_id = va.id 
                            db.session.add(ep)
                            db.session.flush()
                
            else:
                for arc in arcs:
                    if arc.parent_id is None:
                        raise NotImplementedError
                    else:
                        # stage 3 - Weights
                        w = Weight()
                        w.user_id = get_user_id()
                        w.stage_id = stage_3.id
                        w.variable_id = arc.child_id
                        w.parent_variable_id = arc.parent_id
                        db.session.add(w)
                        db.session.flush()

                # stage 4 - create 1 object VA
                va_stage4 = VariableAllocation()
                va_stage4.variable_id = a.child_id
                va_stage4.stage_id = stage_4.id
                db.session.add(va_stage4)
                db.session.flush()

                # creates n CPC objects based on the most number of states from each children
                va_arcs = get_parents_from_child(a.child_id)
                n = 0
                parent_var = None
                for va_arc in va_arcs:
                    if n < va_arc.parent.states.count():
                        n = va_arc.parent.states.count()
                        parent_var = va_arc.parent
                # creates CPC object from parent's state
                for parent_state in parent_var.states:
                    c = CPC()
                    c.user_id = get_user_id()
                    c.var_alloc_id = va_stage4.id
                    c.base_variable_id = parent_var.id
                    db.session.add(c)
                    db.session.flush()

                    # create CPC State object
                    cs = CPCState()
                    cs.cpc_id = c.id
                    cs.state_id = parent_state.id
                    db.session.add(cs)
                    db.session.flush()

                # stage 5 create VA
                va_stage5 = VariableAllocation()
                va_stage5.variable_id = a.child_id
                va_stage5.stage_id = stage_5.id
                db.session.add(va_stage5)
                db.session.flush()

            # stage 6 create tag
            va_stage6 = VariableAllocation()
            va_stage6.variable_id = v.id
            va_stage6.stage_id = stage_6.id
            db.session.add(va_stage6)
            db.session.flush()
    add_log(request=request, details='starting survey ' + model.project.title, type=0)
    db.session.commit()


@task_controller.route('/api/task/survey/process', methods=['GET', 'POST'])
@authenticated_resource
@wrapper
def process_survey():
    '''
    This function will return all the data needed that will
    syntactically displayed by the browser
    The data will contained :
    - what will be displayed (4 types); 
      (1)information only; (2)survey questions; (3)weights questions; (4)cpc questions
      (5)questions clustering type
    - sentences needed to displayed
    - ep.id to glue with the responses (1)
    Users will call this api, and expect one of 6 responses
    (1) - (4) 4 types of questions
    (5). Finish statement,
    (6). Rating questions
    '''

    if request.method == 'GET':
        model_id = int(request.args.get('id'))
        return get_process_survey(model_id)
    elif request.method == 'POST':
        data = request.data
        d = json.loads(data)
        if 'stage' in d:
            if d['stage'] == 3:
                process_weight(d)
            elif d['stage'] == 4:
                process_cpc(d)
            elif d['stage'] < 3 or d['stage'] == 5:
                post_process_survey(d)
            elif d['stage'] == 6:
                process_tags(d)

        return get_process_survey(d['model_id'])


def get_process_survey(model_id):
    ## STEP 1 ##
    # 1.a. Get all stages by user and model
    user_id = get_user_id()

    # select s.* from stage s join model m on s.model_id = m.id where
    # m.is_active = 1 and s.user_id = 2 and m.has_loaded = 1 and m.id = 1;
    stages = Stage.query.join(Model).filter(Model.is_active,
                                            Model.has_loaded,
                                            Stage.user_id == user_id,
                                            Model.id == model_id).all()
    # stages must exist at least 1 stage for 1 variable in 1 model
    if len(stages) == 0:
        raise AppException(AppExceptionCode.NOT_FOUND_ERROR)

    output = {}

    # 1.b. Check if all stages that has been completed
    stages_finished = list(filter(lambda x: x.has_completed, stages))
    if len(stages_finished) == len(stages):
        # finished
        output['stage'] = 9
        return output

    # 2. Begin with stage 1
    # if exist, we will seek the last uncompleted record to be filled by  a user
    stage1 = next(filter(lambda x: x.ref_stage_id == 1, stages))
    if not stage1.has_completed:
        va_uncompleted = list(filter(lambda x: not x.has_completed, stage1.variable_allocations))

        if len(va_uncompleted) == 0:
            # something is wrong, we need to update stage1 has completed !
            stage1.has_completed = True
            stage1.end = datetime.now()
            db.session.add(stage1)
            db.session.commit()
            return get_process_survey(model_id)

        # we are going to process the first record
        va = va_uncompleted[0]
        # find all elicited_prob records by var_alloc.id
        eps = va.elicited_probs
        # which one is NULL? that will be rendered
        ep_null = next(filter(lambda x: x.value is None, eps))

        # render questions
        # we have probability_id, variable_id now all we need is state_id from prob_id
        # get variable.label and state.label
        variable_label = va.variable.label
        state_label = ep_null.probability.state.label

        question = render_statement(variable_label, state_label)
        output['variable'] = variable_label
        output['ep_id'] = ep_null.id
        output['statement'] = question
        output['stage'] = 1
        output['progress'] = get_progress(model_id)
        return output

    # 3. Begin with stage 2
    stage2 = next(filter(lambda x: x.ref_stage_id == 2, stages))
    # if exist we will seek the last uncompleted record to be filled by a user
    if not stage2.has_completed:
        va_uncompleted = list(filter(lambda x: not x.has_completed, stage2.variable_allocations))

        if len(va_uncompleted) == 0:
            stage2.has_completed = True
            stage2.end = datetime.now()
            db.session.add(stage2)
            db.session.commit()
            return get_process_survey(model_id)

        # we start from the first record
        va = va_uncompleted[0]
        # we have full join probability distributions here
        eps = va.elicited_probs
        # we choose the first NULL that will be rendered
        ep_null = next(filter(lambda x: x.value is None, eps))
        variable_label = va.variable.label
        state_label = ep_null.probability.state.label
        question = render_statement(variable_label, state_label)

        # get the parent variable and the state based on ep_id
        # from elicited_prob ~ probability_id (probability_state) ~ state_id (state) ~ variable_id (variable)
        # find prob_state
        ps_list = ProbabilityState.query.filter(ProbabilityState.probability_id == ep_null.probability_id).all()
        if len(ps_list) == 0:
            raise AppException(AppExceptionCode.POLICY_VIOLATION, 'Error in probing Probability_State')

        ps = ps_list[0]
        parent_var_label = ps.state.variable.label
        parent_st_label = ps.state.label
        condition = render_statement(parent_var_label, parent_st_label)

        output['stage'] = 2
        output['statement'] = question
        output['condition'] = condition
        output['ep_id'] = ep_null.id
        output['variable'] = variable_label
        output['progress'] = get_progress(model_id)
        return output
    # stage 3
    stage3 = next(filter(lambda x: x.ref_stage_id == 3, stages))
    if not stage3.has_completed:
        # find the weights that is incompleted first
        weights_incomplete = [w for w in stage3.weights if w.has_completed is False]
        pool = []
        variable_id = None
        for w in weights_incomplete:
            if variable_id is None:
                variable_id = w.variable_id
                pool.append(w)
            else:
                if variable_id == w.variable_id:
                    pool.append(w)
                else:
                    break

        variable = Variable.get(variable_id)
        output['stage'] = 3
        output['variable'] = variable.label

        output['parents'] = []
        for p in pool:
            output['parents'].append({'w_id': p.id, 'label':p.parent_variable.label})
        output['progress'] = get_progress(model_id)
        return output
    # stage 4
    stage4 = next(filter(lambda x: x.ref_stage_id == 4, stages))
    if not stage4.has_completed:
        # d['statement'] = 'Brand is Apple'
        # d['variables']= [{'var_name':'Type',
                    #  'states':[{'id':4,'state_label':'Light'},
                    # {'id':6,'state_label':'Professional'}]}]

        # find the variable allocation that has not been completed
        va_uncompleted = list(filter(lambda x: not x.has_completed, stage4.variable_allocations))
        if len(va_uncompleted) == 0:
            stage4.has_completed = True
            stage4.end = datetime.now()
            db.session.add(stage4)
            db.session.commit()
            return get_process_survey(model_id)
        # we start from the first record
        va = va_uncompleted[0]
        # create statement
        # find all cpcs, which every the ep_id is False and pick the first one
        cpc_s = [x for x in va.cpcs if x.is_completed is False]
        cpc = cpc_s[0]
        cpc_state = cpc.cpc_states[0]
        statement = render_statement(cpc.variable.label, cpc_state.state.label)
        output['statement'] = statement
        output['stage'] = 4
        output['variable'] = va.variable.label
        output['variable_id'] = va.variable.id
        output['cpc_id'] = cpc.id
        output['variables'] = []
        # finds parents from va
        arc_vars = get_parents_from_child(va.variable.id)
        vars = [x.parent for x in arc_vars]
        for v in vars:
            if v.id != cpc.base_variable_id:
                output['variables'].append({'var_id': v.id, 'var_name': v.label, 'states': v.get_states()})
        output['progress'] = get_progress(model_id)
        return output
    # stage 5
    stage5 = next(filter(lambda x: x.ref_stage_id == 5, stages))
    if not stage5.has_completed:
        va_uncompleted = list(filter(lambda x: not x.has_completed, stage5.variable_allocations))

        if len(va_uncompleted) == 0:
            stage5.has_completed = True
            stage5.end = datetime.now()
            db.session.add(stage5)
            db.session.commit()
            return get_process_survey(model_id)

        # we start from the first record
        va = va_uncompleted[0]
        # we have full join probability distributions here
        eps = va.elicited_probs
        # we choose the first NULL that will be rendered
        ep_null = next(filter(lambda x: x.value is None, eps))
        variable_label = va.variable.label
        state_label = ep_null.probability.state.label
        question = render_statement(variable_label, state_label)

        # get the parent variable and the state based on ep_id
        # from elicited_prob ~ probability_id (probability_state) ~ state_id (state) ~ variable_id (variable)
        # find prob_state
        ps_list = ProbabilityState.query.filter(ProbabilityState.probability_id == ep_null.probability_id).all()
        if len(ps_list) == 0:
            raise AppException(AppExceptionCode.POLICY_VIOLATION, 'Error in probing Probability_State')

        conditions = []
        for ps in ps_list:
            condition = render_statement(ps.state.variable.label, ps.state.label)
            conditions.append(condition)

        output['stage'] = 5
        output['statement'] = question
        output['conditions'] = conditions
        output['ep_id'] = ep_null.id
        output['variable'] = variable_label
        output['progress'] = get_progress(model_id)
        return output
    # stage 6
    stage6 = next(filter(lambda x: x.ref_stage_id == 6, stages))
    if not stage6.has_completed:
        va_uncompleted = list(filter(lambda x: not x.has_completed, stage6.variable_allocations))

        if len(va_uncompleted) == 0:
            stage6.has_completed = True
            stage6.end = datetime.now()
            db.session.add(stage6)
            db.session.commit()
            return get_process_survey(model_id)

        # we start from the first record
        va = va_uncompleted[0]
        variable_label = va.variable.label

        tags = Tag.query.join(Model).filter(Model.id == va.stage.model_id).all()
        output['tags'] = []
        for t in tags:
            output['tags'].append({'id': t.id, 'label': t.label})
        output['stage'] = 6
        output['variable'] = variable_label
        output['var_alloc_id'] = va.id
        output['progress'] = get_progress(model_id)
        return output


def post_process_survey(d):
    # we need user_id, ep_id, and probability value for ep_id
    user_id = get_user_id()
    ep_id = d['ep_id']
    prob_val = quantify(d['value'])

    # save the ep_id value
    ep = ElicitedProb.get(ep_id)
    if ep is None:
        raise AppException(AppExceptionCode.NOT_FOUND_ERROR)

    ep.value = prob_val
    db.session.add(ep)
    db.session.flush()

    # check if this 'ep' is the last of its variable_allocation to update has_completed
    #select ep.* from elicited_prob ep where ep.var_alloc_id =
    #(select e.var_alloc_id from elicited_prob e where e.id=7);

    eps = ElicitedProb.query.filter(ElicitedProb.var_alloc_id == ep.var_alloc_id,
                                    ElicitedProb.value == None).all()
    if len(eps) == 0:
        # all values have been committed
        va = VariableAllocation.get(ep.var_alloc_id)
        va.has_completed = True
        db.session.add(va)
        db.session.flush()

    # check if this 'va' is the last of its stage to update stage
    q_va = VariableAllocation()
    q_va.has_completed = False
    q_va.stage_id = ep.variable_allocation.stage_id
    vas = VariableAllocation.get_list(q_va)
    if len(vas) == 0:
        # all variable allocation has been completed
        s = Stage.get(ep.variable_allocation.stage_id)
        s.has_completed = True
        s.end = datetime.now()
        db.session.add(s)
        db.session.flush()

    db.session.commit()


def process_weight(d):
    d_weight = {k: v for k, v in d.items() if k != 'stage' and k != 'model_id'}
    stage_id = 0
    for k, v in d_weight.items():
        w = Weight.get(int(k))
        w.value = int(v)
        w.has_completed = True
        stage_id = w.stage_id
        db.session.add(w)
        db.session.flush()

    q = Weight()
    q.user_id = get_user_id()
    q.stage_id = stage_id
    q.has_completed = False
    weights_uncompleted = Weight.get_list(q)

    if len(weights_uncompleted) == 0:
        stage = Stage.get(stage_id)
        stage.has_completed = True
        stage.end = datetime.now()
        db.session.add(stage)
        db.session.flush()

    db.session.commit()


def process_cpc(d):
    cpc = CPC.get(d['cpc_id'])
    state_ids = [cpc.cpc_states[0].state_id]
    for k, v in d['cpc_state'].items():
        cs = CPCState()
        cs.cpc_id = cpc.id
        cs.state_id = v['state_id']
        state_ids.append(v['state_id'])
        cs.parent_id = cpc.cpc_states[0].id
        db.session.add(cs)
        db.session.flush()

    # find the appropriate probability_id towards the state
    # select ps.probability_id, count(ps.probability_id) as count from probability_state ps
    # where ps.state_id in (1,4,7)
    # GROUP BY ps.probability_id having count = 3;
    result = db.session.query(ProbabilityState.probability_id).filter(
        ProbabilityState.state_id.in_(state_ids)).group_by(ProbabilityState.probability_id).having(
        db.func.count(ProbabilityState.probability_id) == len(state_ids)).all()
    prob_ids = [value for (value,) in result]

    # select va.* from variable_allocation va join variable v join stage s
    # on va.variable_id = v.id
    # and va.stage_id = s.id
    # where s.user_id = 2 and va.variable_id = 4 and s.ref_stage_id = 5;
    va_ep = VariableAllocation.query.join(Variable).join(Stage).filter(
        Stage.ref_stage_id == 5, Stage.user_id == get_user_id(), Variable.id == cpc.variable_allocation.variable_id
    ).first()
    # create new elicited prob record
    for p_id in prob_ids:
        ep = ElicitedProb()
        ep.var_alloc_id = va_ep.id
        ep.probability_id = p_id
        db.session.add(ep)
        db.session.flush()
    cpc.is_completed = True
    db.session.add(cpc)
    db.session.flush()

    # if everything in cpc is completed, we may update variable allocation
    va = VariableAllocation.get(cpc.var_alloc_id)
    if len([x for x in va.cpcs if x.is_completed is False]) == 0:
        # check if CPC Pair in cpc_state are complete,
        # if not create a cpc and cpc_state records
        state_ids_chosen = db.session.query(
            CPCState.state_id.distinct().label("state_id")).join(
            CPC
        ).filter(CPC.var_alloc_id == cpc.var_alloc_id).all()

        state_ids_chosen = [value for (value,) in state_ids_chosen]
        # compare with all of other states

        var_id = cpc.variable_allocation.variable_id
        state_objs = get_parent_states_from_child(var_id)

        # complete !
        st_ids_intersect = [x for x in [y.id for y in state_objs] if x not in state_ids_chosen]
        if len(st_ids_intersect) == 0:
            # if complete then update it
            va.has_completed = True
            db.session.add(va)
            db.session.flush()
        else:
            # else create new record
            t = st_ids_intersect[0]  # 5
            c = CPC()
            c.user_id = get_user_id()
            c.var_alloc_id = cpc.var_alloc_id
            c.base_variable_id = get_variable_from_state_id(t).id
            db.session.add(c)
            db.session.flush()

            sc = CPCState()
            sc.cpc_id = c.id
            sc.state_id = t
            db.session.add(sc)
            db.session.flush()

    # if everything in variable allocation is completed, we update stage
    stage = va.stage
    if len([x for x in stage.variable_allocations if x.has_completed is False]) == 0:
        stage.has_completed = True
        stage.end = datetime.now()
        db.session.add(stage)
        db.session.flush()

    db.session.commit()


def process_tags(d):
    for t in d['tags']:
        vat = VariableAllocationTag()
        vat.var_alloc_id = d['var_alloc_id']
        vat.var_alloc_id = t
        db.session.add(vat)
        db.session.flush()

    va = VariableAllocation.get(d['var_alloc_id'])
    va.has_completed = True
    db.session.add(va)
    db.session.flush()

    # if everything in var_alloc completed, update stage
    vas = VariableAllocation.query.join(Stage).filter(Stage.ref_stage_id == 6, Stage.user_id == get_user_id(),
                                                      Stage.model_id == d['model_id'],
                                                      VariableAllocation.has_completed == False).all()
    if len(vas) == 0:
        stage = Stage.query.filter(Stage.model_id == d['model_id'], Stage.user_id == get_user_id(),
                                   Stage.ref_stage_id == 6).first()
        stage.has_completed = True
        stage.end = datetime.now()
        db.session.add(stage)
        db.session.flush()
        add_log(request=request, details='has finished survey ' + stage.model.project.title, type=0)

    db.session.commit()


def get_progress(model_id):
    va_unfinished = VariableAllocation.query.join(Stage).filter(
        Stage.user_id == get_user_id(),Stage.model_id == model_id,
        VariableAllocation.has_completed == True).count()
    total_va = VariableAllocation.query.join(Stage).filter(
        Stage.user_id == get_user_id(), Stage.model_id == model_id).count()
    w_unfinished = Weight.query.join(Stage).filter(
        Stage.user_id == get_user_id(),Stage.model_id == model_id,
        Weight.has_completed == True).count()
    total_w = Weight.query.join(Stage).filter(
        Stage.user_id == get_user_id(), Stage.model_id == model_id).count()
    return round((va_unfinished + w_unfinished) / (total_va + total_w), 2) * 100


def render_statement(variable_label, state_label):
    question = '{0} is {1}'.format(variable_label, state_label)
    return question


def quantify(val):
    if val == 'Impossible':
        return 0
    elif val == 'Improbable':
        return 0.15
    elif val == 'Uncertain':
        return 0.25
    elif val == 'Fifty-fifty':
        return 0.5
    elif val == 'Expected':
        return 0.75
    elif val == 'Probable':
        return 0.85
    elif val == 'Certain':
        return 1
    else:
        raise AppException(AppExceptionCode.UNKNOWN_VALUE)

    

