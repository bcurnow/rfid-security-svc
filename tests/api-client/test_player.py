api = 'player'


def test_get(rh, sounds):
    rh.assert_response(rh.open('get', f'{api}/{sounds[0].name}', content_type='audio/wav'), 200, sounds[0].content)


def test_get_notfound(rh, sounds):
    rh.assert_response(rh.open('get', f'{api}/bogus'), 404)
