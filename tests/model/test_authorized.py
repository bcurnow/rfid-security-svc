from unittest.mock import patch

import rfidsecuritysvc.model.authorized as model
from rfidsecuritysvc.model.color import Color
from rfidsecuritysvc.model.guest import Guest
from rfidsecuritysvc.model.guest_media import GuestMedia
from rfidsecuritysvc.model.media import Media
from rfidsecuritysvc.model.authorized import MediaConfig
from rfidsecuritysvc.model.sound import Sound



@patch('rfidsecuritysvc.model.authorized.guest_media')
@patch('rfidsecuritysvc.model.authorized.media_perm')
def test_authorized(media_perm, guest_media, open_door_media_perm, open_door_guest_media):
    media_perm.get_by_media_and_perm.return_value = open_door_media_perm
    guest_media.get_by_media.return_value = open_door_guest_media
    expected = MediaConfig(open_door_media_perm,
                           open_door_guest_media.guest,
                           open_door_guest_media.sound,
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
    sound = Sound(2, 'test.wav', '2021-09-25 23:13:25')
    color = Color(0xABCDEF0123456789)
    mc = MediaConfig(media_perms[0], guest, sound, color)
    assert mc.media == media_perms[0].media
    assert mc.permission == media_perms[0].permission
    assert mc.guest == guest
    assert mc.sound == sound
    assert mc.color == color


def test_MediaConfig_no_color(media_perms):
    mc = MediaConfig(media_perms[0], None, None, None)
    assert mc.color is None


def test_MediaConfig_no_sound(media_perms):
    mc = MediaConfig(media_perms[0], None, None, None)
    assert mc.sound is None


def test_MediaConfig_no_guest(media_perms):
    mc = MediaConfig(media_perms[0], None, None, None)
    assert mc.guest is None


def test_MediaConfig_to_json(media_perms):
    guest = Guest(1, 'first_name', 'last_name')
    sound = Sound(2, 'test.wav', '2021-09-25 23:13:25')
    color = Color(0xABCDEF0123456789)
    mc = MediaConfig(media_perms[0], guest, sound, color)
    json = mc.to_json()
    assert json['media'] == media_perms[0].media.to_json()
    assert json['permission'] == media_perms[0].permission.to_json()
    assert json['guest'] == guest.to_json()
    assert json['sound'] == sound.to_json()
    assert json['color'] == color.to_json()


def test__resolveColor_from_guest():
    gm = modifiableGuestMedia()
    # Set the color attribute on the guest but leave the rest at None
    color = Color(0x12345)
    gm.guest.color = color

    assert model._resolveColor(gm) == color


def test__resolveColor_from_guest_media():
    gm = modifiableGuestMedia()
    # Set the color attribute on both the guest and guest_media to ensure the guest_media value is returned
    g_color = Color(0x12345)
    gm.guest.color = g_color
    gm_color = Color(0x6789)
    gm.color = gm_color

    assert model._resolveColor(gm) == gm_color


def test__resolveColor_none():
    gm = modifiableGuestMedia()
    assert model._resolveColor(gm) is None


def test__resolveSound_from_guest():
    gm = modifiableGuestMedia()
    # Set the sound attributes on the guest but leave the rest at None
    sound = Sound(1, 'guest sound', '2021-09-25 23:13:25')
    gm.guest.sound = sound

    assert model._resolveSound(gm) == sound


def test__resolveSound_from_guest_media():
    gm = modifiableGuestMedia()
    # Set the sound attributes on both the guest and guest_media to ensure the guest_media value is returned
    g_sound = Sound(1, 'guest sound', '2021-09-25 23:13:25')
    gm.guest.sound = g_sound
    gm_sound = Sound(2, 'guest media sound', '2021-09-25 23:13:25')
    gm.sound = gm_sound

    assert model._resolveSound(gm) == gm_sound


def test__resolveSound_none():
    gm = modifiableGuestMedia()
    assert model._resolveSound(gm) == None


def modifiableGuestMedia():
    """ Returns a new GuestMedia object every time it's called to allow for modifications of the object state. """
    g = Guest(1, 'Mickey', 'Mouse', None, None)
    m = Media('modifiable', 'modifiable', 'this media is modifiable')
    gm = GuestMedia(1, g, m, None, None)
    return gm
