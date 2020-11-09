from rfidsecuritysvc import exception as exception
from rfidsecuritysvc.model import association

def authorized(media_id, perm_name):
    try:
        if association.get(media_id, perm_name):
            return True

        return False
    except exception.PermissionNotFoundError:
        return False
    except exception.AssociationNotFoundError:
        return False
