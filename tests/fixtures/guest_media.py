import pytest

from rfidsecuritysvc.model.guest_media import GuestMedia


@pytest.fixture(scope='session')
def guest_medias(media_for_guests,
                 guests,
                 open_door_guest,
                 open_door_media,
                 not_authorized_media_guest,
                 not_authorized_media,
                 no_prefs_media_guest,
                 no_prefs_media,
                 default_sound):
    # The DB will return these ordered by id, please build the list accordingly
    guest_medias = []
    # Make sure we have enough guests for the media provided
    # If this fails, you need to look at the media fixture
    assert len(media_for_guests) <= len(guests)

    for i in range(len(media_for_guests)):
        guest_medias.append(GuestMedia(i + 1,
                                      guests[i],
                                      media_for_guests[i],
                                      default_sound.id,
                                      default_sound.name,
                                      0xABCDEF))

    guest_medias.append(GuestMedia(len(guest_medias) + 1,
                                  open_door_guest,
                                  open_door_media,
                                  default_sound.id,
                                  default_sound.name,
                                  0xABCDEF))

    guest_medias.append(GuestMedia(len(guest_medias) + 1,
                                  no_prefs_media_guest,
                                  no_prefs_media,
                                  None,
                                  None,
                                  None))

    return guest_medias


@pytest.fixture(scope='session')
def creatable_guest_media(guest_medias, guest_for_creatable_guest_media, media_for_creatable_guest_media, default_sound):
    return GuestMedia(len(guest_medias) + 1,
                      guest_for_creatable_guest_media,
                      media_for_creatable_guest_media,
                      default_sound.id,
                      default_sound.name,
                      0xABCDEF)


@pytest.fixture(scope='session')
def guest_media_to_row():
    def to_row(m):
        row = {}
        row['id'] = m.id
        row['guest_id'] = m.guest.id
        row['guest_first_name'] = m.guest.first_name
        row['guest_last_name'] = m.guest.last_name
        row['guest_default_sound'] = m.guest.default_sound
        row['guest_default_sound_name'] = m.guest.default_sound_name
        row['guest_default_color'] = m.guest.default_color
        row['media_id'] = m.media.id
        row['media_name'] = m.media.name
        row['media_desc'] = m.media.desc
        row['sound_id'] = m.sound_id
        row['sound_name'] = m.sound_name
        row['color'] = m.color
        return row

    return to_row


@pytest.fixture(autouse=True, scope='session')
def add_guest_media_helpers(monkeypatch_session):
    def convert(self):
        return {
            'guest_id': self.guest.id,
            'media_id': self.media.id,
            'sound_id': self.sound_id,
            'color': self.color,
        }

    monkeypatch_session.setattr(GuestMedia, 'test_create', convert, raising=False)
    monkeypatch_session.setattr(GuestMedia, 'test_update', convert, raising=False)
