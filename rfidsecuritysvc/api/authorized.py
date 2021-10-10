from rfidsecuritysvc.model import authorized


def get(media_id, perm_name):
    mc = authorized.authorized(media_id, perm_name)
    if mc:
        return mc.to_json()
    return None, 403
