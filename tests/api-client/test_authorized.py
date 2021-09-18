def test_get(rh, open_door):
    media, perm, media_perm = open_door
    rh.assert_response(rh.open('get', f'authorized/{media.id}/{perm.name}'), 200)


def test_get_nomedia(rh, open_door):
    media, perm, media_perm = open_door
    rh.assert_response(rh.open('get', 'authorized/no such media/{perm.name}'), 403)


def test_get_noperm(rh, open_door):
    media, perm, media_perm = open_door
    rh.assert_response(rh.open('get', f'authorized/{media.id}/no such perm'), 403)


def test_get_notauthorized(rh, medias, permissions):
    rh.assert_response(rh.open('get', f'authorized/{medias[0].id}/{permissions[2].name}'), 403)
