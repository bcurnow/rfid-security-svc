from rfidsecuritysvc.model import authorized

def get(media_id: str, perm_name: str) -> tuple[dict | None, int]:
    mc = authorized.authorized(media_id, perm_name)
    if mc:
        return mc.to_json()
    return None, 403
