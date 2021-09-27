api = 'player'


def test_get(rh, sounds):
    rh.assert_response(rh.open('get', f'{api}/{sounds[0].name}', content_type='audio/wav'), 200, sounds[0].content)


def test_get_with_range(rh, sounds):
    rh.assert_response(rh.open('get',
                               f'{api}/{sounds[0].name}',
                               content_type='audio/wav',
                               headers={'Range': 'bytes=0-1'}
                               ), 206, sounds[0].content[0:2])


def test_get_notfound(rh, sounds):
    rh.assert_response(rh.open('get', f'{api}/bogus'), 404)
