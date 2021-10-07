from rfidsecuritysvc.model import authorized


def get(media_id, perm_name):
    mp = authorized.authorized(media_id, perm_name)
    if mp:
        return mp.to_json(), 200

    # Return Forbidden to indicate that they are not authorized
    # I considered 401 but the semantics are slightly different and don't really match
    return None, 403
