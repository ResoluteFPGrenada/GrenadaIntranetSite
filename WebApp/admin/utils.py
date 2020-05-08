from WebApp import db
from WebApp.models import Role

    # sets available roles
def available_roles(roles, user):
    role_ids = [role.id for role in roles]
    rights_ids = [right.id for right in user.rights]
    difs = (list(set(role_ids) - set(rights_ids)))
    availables = []
    for dif in difs:
        availables.append(Role.query.filter_by(id=dif).first())
    return availables

def available_rights(roles, user):
    role_ids = [role.id for role in roles]
    rights_ids = [right.id for right in user.rights]
    availables = []
    for role_id in role_ids:
        if role_id in rights_ids:
            availables.append(Role.query.filter_by(id=role_id).first())
    return availables
