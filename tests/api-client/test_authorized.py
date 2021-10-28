from rfidsecuritysvc.model.authorized import MediaConfig


def test_get(rh, open_door):
    media, perm = open_door
    rh.assert_response(rh.open('get', f'authorized/{media.id}/{perm.name}'), 200)


def test_get_no_guest_info(rh, authorized_media_perm_no_guest, default_permission):
    mc = MediaConfig(authorized_media_perm_no_guest, None, None, None)
    rh.assert_response(rh.open('get', f'authorized/{authorized_media_perm_no_guest.media.id}/{authorized_media_perm_no_guest.permission.name}'), 200, mc)


def test_get_nomedia(rh, open_door):
    media, perm = open_door
    rh.assert_response(rh.open('get', 'authorized/no such media/{perm.name}'), 403)


def test_get_noperm(rh, open_door):
    media, perm = open_door
    rh.assert_response(rh.open('get', f'authorized/{media.id}/no such perm'), 403)


def test_get_notauthorized(rh, not_authorized_media, default_permission):
    rh.assert_response(rh.open('get', f'authorized/{not_authorized_media.id}/{default_permission.name}'), 403)
