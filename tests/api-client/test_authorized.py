def test_get(rh, open_door):
    media, perm, media_perm = open_door
    rh.assert_response(rh.open('get', f'authorized/media/{media.id}/perm/{perm.name}'), 200)


def test_get_nomedia(rh, open_door):
    media, perm, media_perm = open_door
    rh.assert_response(rh.open('get', 'authorized/media/no such media/perm/{perm.name}'), 403)


def test_get_noperm(rh, open_door):
    media, perm, media_perm = open_door
    rh.assert_response(rh.open('get', f'authorized/media/{media.id}/perm/no such perm'), 403)


def test_get_notauthorized(rh, medias, permissions):
    rh.assert_response(rh.open('get', f'authorized/media/{medias[0].id}/perm/{permissions[2].name}'), 403)
