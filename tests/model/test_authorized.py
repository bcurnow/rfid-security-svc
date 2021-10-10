from unittest.mock import patch

import rfidsecuritysvc.model.authorized as model
from rfidsecuritysvc.model.guest import Guest
from rfidsecuritysvc.model.authorized import MediaConfig


@patch('rfidsecuritysvc.model.authorized.media_perm')
def test_authorized(media_perm, media_perms):
    media_perm.get_by_media_and_perm.return_value = media_perms[0]
    expected = MediaConfig(media_perms[0], None, None, None, None)
    assert model.authorized('test', 'test_perm') == expected
    media_perm.get_by_media_and_perm.assert_called_once_with('test', 'test_perm')


@patch('rfidsecuritysvc.model.authorized.media_perm')
def test_authorized_not_found(media_perm, media_perms):
    media_perm.get_by_media_and_perm.return_value = None
    assert model.authorized('test', 'test_perm') == None
    media_perm.get_by_media_and_perm.assert_called_once_with('test', 'test_perm')


def test_MediaConfig(media_perms):
    guest = Guest(1, 'first_name', 'last_name')
    mc = MediaConfig(media_perms[0], guest, 2, 'test.wav', 0xABCDEF0123456789)
    assert mc.media == media_perms[0].media
    assert mc.permission == media_perms[0].permission
    assert mc.guest == guest
    assert mc.sound_id == 2
    assert mc.sound_name == 'test.wav'
    assert mc.color == 0xABCDEF0123456789
    assert mc.color_hex == 'ABCDEF0123456789'
    assert mc.color_html == '#abcdef0123456789'


def test_MediaConfig_no_color(media_perms):
    mc = MediaConfig(media_perms[0], None, None, None, None)
    assert mc.color is None
    assert mc.color_hex is None
    assert mc.color_html is None


def test_MediaConfig_no_sound(media_perms):
    mc = MediaConfig(media_perms[0], None, None, None, None)
    assert mc.sound_id == None
    assert mc.sound_name == None


def test_MediaConfig_no_guest(media_perms):
    mc = MediaConfig(media_perms[0], None, None, None, None)
    assert mc.guest == None


def test_MediaConfig_to_json(media_perms):
    guest = Guest(1, 'first_name', 'last_name')
    mc = MediaConfig(media_perms[0], guest, 2, 'test.wav', 0xABCDEF0123456789)
    json = mc.to_json()
    assert json['media'] == media_perms[0].media.to_json()
    assert json['permission'] == media_perms[0].permission.to_json()
    assert json['guest'] == guest.to_json()
    assert json['sound_id'] == 2
    assert json['sound_name'] == 'test.wav'
    assert json['color'] == 0xABCDEF0123456789
    assert json['color_hex'] == 'ABCDEF0123456789'
    assert json['color_html'] == '#abcdef0123456789'
