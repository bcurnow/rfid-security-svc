from unittest.mock import patch

import rfidsecuritysvc.model.authorized as model
from rfidsecuritysvc.model.guest import Guest
from rfidsecuritysvc.model.guest_media import GuestMedia
from rfidsecuritysvc.model.media import Media
from rfidsecuritysvc.model.authorized import MediaConfig


@patch('rfidsecuritysvc.model.authorized.guest_media')
@patch('rfidsecuritysvc.model.authorized.media_perm')
def test_authorized(media_perm, guest_media, open_door_media_perm, open_door_guest_media):
    media_perm.get_by_media_and_perm.return_value = open_door_media_perm
    guest_media.get_by_media.return_value = open_door_guest_media
    expected = MediaConfig(open_door_media_perm,
                           open_door_guest_media.guest,
                           open_door_guest_media.sound_id,
                           open_door_guest_media.sound_name,
                           open_door_guest_media.color)
    assert model.authorized('test', 'test_perm') == expected
    media_perm.get_by_media_and_perm.assert_called_once_with('test', 'test_perm')
    guest_media.get_by_media.assert_called_once_with('test')


@patch('rfidsecuritysvc.model.authorized.media_perm')
def test_authorized_not_found(media_perm, media_perms):
    media_perm.get_by_media_and_perm.return_value = None
    assert model.authorized('test', 'test_perm') is None
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
    assert mc.sound_id is None
    assert mc.sound_name is None


def test_MediaConfig_no_guest(media_perms):
    mc = MediaConfig(media_perms[0], None, None, None, None)
    assert mc.guest is None


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


def test__resolveColor_from_guest():
    gm = modifiableGuestMedia()
    # Set the color attribute on the guest but leave the rest at None
    gm.guest.default_color = 0x12345

    assert model._resolveColor(gm) == 0x12345


def test__resolveColor_from_guest_media():
    gm = modifiableGuestMedia()
    # Set the color attribute on both the guest and guest_media to ensure the guest_media value is returned
    gm.guest.default_color = 0x12345
    gm.color = 0x6789

    assert model._resolveColor(gm) == 0x6789


def test__resolveColor_none():
    gm = modifiableGuestMedia()
    assert model._resolveColor(gm) is None


def test__resolveSound_from_guest():
    gm = modifiableGuestMedia()
    # Set the sound attributes on the guest but leave the rest at None
    gm.guest.default_sound = 1
    gm.guest.default_sound_name = 'guest sound'

    assert model._resolveSound(gm) == (1, 'guest sound')


def test__resolveSound_from_guest_media():
    gm = modifiableGuestMedia()
    # Set the sound attributes on both the guest and guest_media to ensure the guest_media value is returned
    gm.guest.default_sound = 1
    gm.guest.default_sound_name = 'guest sound'
    gm.sound_id = 2
    gm.sound_name = 'guest media sound'

    assert model._resolveSound(gm) == (2, 'guest media sound')


def test__resolveSound_none():
    gm = modifiableGuestMedia()
    assert model._resolveSound(gm) == (None, None)


def modifiableGuestMedia():
    """ Returns a new GuestMedia object every time it's called to allow for modifications of the object state. """
    g = Guest(1, 'Mickey', 'Mouse', None, None, None)
    m = Media('modifiable', 'modifiable', 'this media is modifiable')
    gm = GuestMedia(1, g, m, None, None, None)
    return gm
