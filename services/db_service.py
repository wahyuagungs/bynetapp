from models.accesslog import AccessLog
from models.appprofile import AppProfile
from models.refmenu import RefMenu
from models.menurole import MenuRole
from models.refrole import RefRole
from models.appuser import AppUser
from models.appuserrole import AppUserRole
from models.project import Project
from models.projectuser import ProjectUser
from models.model import Model
from models.arc import Arc
from models.variable import Variable
from models.probability import Probability
from models.state import State
from models.probabilitystate import ProbabilityState

from models.cpc import CPC
from models.cpcstate import CPCState
from models.elicitedprob import ElicitedProb
from models.refstage import RefStage
from models.stage import Stage
from models.variableallocation import VariableAllocation
from models.weight import Weight
from models.tag import Tag
from models.varalloctag import VariableAllocationTag

from exception.appexception import AppException
from exception.appexceptioncode import AppExceptionCode
from datetime import datetime
from utils import get_random_text
from models.base import db


def construct_database():
    """
    Initializes the database tables and relationships
    :return: None
    """
    db.create_all()
    db.session.commit()


def intialise_contents():
    """
    Initialise core contents into tables e.g. menus, roles
    :return: None
    """
    # fill the user
    admin_user = AppUser(firstname="Admin", lastname="Admin",
                         email="admin@bynet.org.au", username="admin",
                         is_activated=True)
    admin_user.password = "password"
    admin_user.activation_date = datetime.now()
    admin_user.activation_token = get_random_text(30)
    admin_user.organisation = "Administrator"
    commit([admin_user])

    # fill ref_role
    admin_role = RefRole(rolename="Administrator", role_description="System Administrator, adding user capabilities")
    analyst = RefRole(rolename="Analyst", role_description="Creates questions and analyse answers")
    participant = RefRole(rolename="Participant", role_description="Answer questions")
    commit([admin_role, analyst, participant])

    # fill in role
    admin_user_role = AppUserRole(app_user=admin_user.id, ref_role=admin_role.id)
    commit([admin_user_role])

    # fill in ref_menu
    dashboard_menuitem = RefMenu("app.main", "Dashboard", "icon-home")
    commit([dashboard_menuitem])

    setting_menuitem = RefMenu("app.settings", "Settings", "icon-settings")
    commit([setting_menuitem])

    app_profile_menuitem = RefMenu("app.settings.profile", "Profile App", "icon-wrench", setting_menuitem.id)
    usermgmt_menutitem = RefMenu("app.settings.user", "Manage User", "icon-user", setting_menuitem.id)
    commit([usermgmt_menutitem, app_profile_menuitem])

    project_menuitem = RefMenu("app.project", "Project", "icon-folder-alt")
    commit([project_menuitem])

    manage_project_menuitem = RefMenu("app.project.manage", "Manage Project", "icon-note", project_menuitem.id)
    modelmanage_project_menuitem = RefMenu("app.project.model", "Manage Model", "icon-graph", project_menuitem.id)
    info_project_menuitem = RefMenu("app.project.info", "Project Info", "icon-info",project_menuitem.id)
    commit([manage_project_menuitem, modelmanage_project_menuitem, info_project_menuitem])

    tasks_menuitem = RefMenu("app.tasks", "Tasks","icon-layers")
    commit([tasks_menuitem])

    view_tasks_menuitem = RefMenu("app.tasks.view", "View Tasks", "icon-map", tasks_menuitem.id)
    process_tasks_menuitem = RefMenu("app.tasks.process", "Process", "icon-graph", tasks_menuitem.id)
    commit([view_tasks_menuitem, process_tasks_menuitem])

    about_menuitem = RefMenu("app.about", "About Us", "icon-question")
    commit([about_menuitem])

    contact_about_menuitem = RefMenu("app.contact", "Contact Us", "icon-help", about_menuitem.id)
    commit([contact_about_menuitem])

    # fill in app user role
    # admin role
    dash_admin_menurole = MenuRole(ref_menu=dashboard_menuitem.id, ref_role=admin_role.id)
    setting_admin_menurole = MenuRole(ref_menu=setting_menuitem.id, ref_role=admin_role.id)
    appprofle_admin_menurole = MenuRole(ref_menu=app_profile_menuitem.id, ref_role=admin_role.id)
    usermgmt_admin_menurole = MenuRole(ref_menu=usermgmt_menutitem.id, ref_role=admin_role.id)
    modelmgmt_admin_menurole = MenuRole(ref_menu=modelmanage_project_menuitem.id, ref_role=admin_role.id)
    project_admin_menurole = MenuRole(ref_menu=project_menuitem.id, ref_role=admin_role.id)
    mngproject_admin_menurole = MenuRole(ref_menu=manage_project_menuitem.id, ref_role=admin_role.id)
    infoproject_admin_menurole = MenuRole(ref_menu=info_project_menuitem.id, ref_role=admin_role.id)
    about_admin_menurole = MenuRole(ref_menu=about_menuitem.id, ref_role=admin_role.id)
    contact_admin_menurole = MenuRole(ref_menu=contact_about_menuitem.id, ref_role=admin_role.id)
    commit([dash_admin_menurole, setting_admin_menurole, appprofle_admin_menurole, usermgmt_admin_menurole,
            project_admin_menurole, mngproject_admin_menurole, modelmgmt_admin_menurole, infoproject_admin_menurole,
            about_admin_menurole, contact_admin_menurole])
    # analyst role
    dash_analyst_menurole = MenuRole(ref_menu=dashboard_menuitem.id, ref_role=analyst.id)
    modelmgmt_analyst_menurole = MenuRole(ref_menu=modelmanage_project_menuitem.id, ref_role=analyst.id)
    project_analyst_menurole = MenuRole(ref_menu=project_menuitem.id, ref_role=analyst.id)
    mngproject_analyst_menurole = MenuRole(ref_menu=manage_project_menuitem.id, ref_role=analyst.id)
    infoproject_analyst_menurole = MenuRole(ref_menu=info_project_menuitem.id, ref_role=analyst.id)
    tasks_analyst_menurole = MenuRole(ref_menu=tasks_menuitem.id, ref_role=analyst.id)
    viewtasks_analyst_menurole = MenuRole(ref_menu=view_tasks_menuitem.id, ref_role=analyst.id)
    processtask_analyst_menurole = MenuRole(ref_menu=process_tasks_menuitem.id, ref_role=analyst.id)
    about_analyst_menurole = MenuRole(ref_menu=about_menuitem.id, ref_role=analyst.id)
    contact_analyst_menurole = MenuRole(ref_menu=contact_about_menuitem.id, ref_role=analyst.id)
    commit([dash_analyst_menurole, project_analyst_menurole,
            mngproject_analyst_menurole, modelmgmt_analyst_menurole, infoproject_analyst_menurole, tasks_analyst_menurole, viewtasks_analyst_menurole,
            processtask_analyst_menurole, about_analyst_menurole,
            contact_analyst_menurole])
    # participant role
    dash_part_menurole = MenuRole(ref_menu=dashboard_menuitem.id, ref_role=participant.id)
    tasks_part_menurole = MenuRole(ref_menu=tasks_menuitem.id, ref_role=participant.id)
    viewtasks_part_menurole = MenuRole(ref_menu=view_tasks_menuitem.id, ref_role=participant.id)
    processtask_part_menurole = MenuRole(ref_menu=process_tasks_menuitem.id, ref_role=participant.id)
    about_part_menurole = MenuRole(ref_menu=about_menuitem.id, ref_role=participant.id)
    contact_part_menurole = MenuRole(ref_menu=contact_about_menuitem.id, ref_role=participant.id)
    commit([dash_part_menurole, tasks_part_menurole, viewtasks_part_menurole,
            processtask_part_menurole, about_part_menurole,contact_part_menurole])

    profile_app = AppProfile()
    profile_app.information = 'Thank you for your participation in this experiment. Your valuable time and involvement are critical '\
                        'for the success of our projects. We are conducting online web survey to parameterise our model '\
                        'using state-of-the art method to propagate information based on your answers to the questions provided. '\
                        'Should you have any questions regarding the projects please contact us.'
    profile_app.organisation = 'Monash University'
    profile_app.url = 'http://www.monash.edu'
    profile_app.title = 'ByNet Application'
    profile_app.email = 'wahyu.sugimartanto@monash.edu'
    commit([profile_app])

    stage_one = RefStage(stage_label='Stage One - Elicit Parent Probabilities')
    stage_two = RefStage(stage_label='Stage Two - Elicit Full Joint Probabilities')
    stage_three = RefStage(stage_label='Stage Three - Elicit Weights')
    stage_four = RefStage(stage_label='Stage Four - Elicit CPC')
    stage_five = RefStage(stage_label='Stage Five - Elicit CPC Probabilities')
    stage_six = RefStage(stage_label='Stage Six - Elicit Clustering')
    commit([stage_one, stage_two, stage_three, stage_four, stage_five, stage_six])


def commit(objs):
    for item in objs:
        db.session.add(item)
        db.session.commit()
