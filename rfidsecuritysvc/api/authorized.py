from rfidsecuritysvc.model import authorized


def get(media_id, perm_name):
    if authorized.authorized(media_id, perm_name):
        return None, 200

    # Return Forbidden to indicate that they are not authorized
    # I considered 401 but the semantics are slightly differnt and don't really match
    return None, 403
