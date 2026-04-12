from rfidsecuritysvc.model import authorized
from typing import Any

def get(media_id: str, perm_name: str) -> dict[str, Any] | tuple[None, int]:
    mc = authorized.authorized(media_id, perm_name)
    if mc:
        return mc.to_json()
    return None, 403
