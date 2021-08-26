from models.initdb import db
from models.refstage import RefStage
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
from utils import authenticated_resource, wrapper, get_user_id, get_profile


def get_parents_from_child(child_id):
    q = Arc()
    q.child_id = child_id
    arcs = Arc.get_list(q)
    return arcs


def get_all_states__by_varid(**kwargs):
    states = State.query.join(Variable).filter(Variable.id == kwargs['id']).all()
    return states


def get_parent_states_from_child(var_id):
    subquery = db.session.query(Arc.parent_id).filter(Arc.child_id == var_id).subquery()
    states = State.query.join(Variable).filter(Variable.id.in_(subquery)).all()
    return states


def get_variable_from_state_id(state_id):
    return Variable.query.join(State).filter(State.id == state_id).all()[0]


def get_var_alloc_per_stage(var_id, stage_id):
    pass