from models.accesslog import AccessLog
from models.appprofile import AppProfile
from models.refmenu import RefMenu
from models.menurole import MenuRole
from models.refrole import RefRole
from models.appuser import AppUser
from models.appuserrole import AppUserRole


def get_menu_idrole(id):
    menus = RefMenu.query. \
        join(MenuRole).filter(MenuRole.ref_role == id).all()
    root_menus = []
    for menu in menus:
        if menu.parent_id is None:
            obj = fetch_menu(menu, menus)
            root_menus.append(obj)
    return [menu.as_dict() for menu in root_menus]


def get_role_byusername(username):
    role = RefRole.query. \
        join(AppUserRole).join(AppUser). \
        filter(AppUser.username == username).first()
    return role.as_dict()


def fetch_menu(menu_item, menus):
    nested_list = []
    for item in menus:
        if item.parent_id is not None:
            if menu_item.id == int(item.parent_id):
                item = fetch_menu(item, menus)
                nested_list.append(item)
    if len(nested_list) > 0:
        menu_item.childItems = nested_list

    return menu_item
