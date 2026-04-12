import pytest
from _pytest.monkeypatch import MonkeyPatch
from rfidsecuritysvc.model.guest import Guest
from rfidsecuritysvc.model.media import Media
from rfidsecuritysvc.model.sound import Sound
from rfidsecuritysvc.model.color import Color
from rfidsecuritysvc.model.guest_media import GuestMedia

@pytest.fixture(scope='session')
def guest_medias(media_for_guests: list[Media], guests: list[Guest], open_door_guest: Guest, open_door_media: Media, no_prefs_media_guest: Guest, no_prefs_media: Media, default_sound: Sound, default_color: Color) -> list[GuestMedia]:
    # The DB will return these ordered by id, please build the list accordingly
    guest_medias = []
    # Make sure we have enough guests for the media provided
    # If this fails, you need to look at the media fixture
    assert len(media_for_guests) <= len(guests)

    for i in range(len(media_for_guests)):
        guest_medias.append(GuestMedia(i + 1, guests[i], media_for_guests[i], default_sound, default_color))

    guest_medias.append(GuestMedia(len(guest_medias) + 1, open_door_guest, open_door_media, default_sound, default_color))

    guest_medias.append(GuestMedia(len(guest_medias) + 1, no_prefs_media_guest, no_prefs_media, None, None))

    return guest_medias


@pytest.fixture(scope='session')
def creatable_guest_media(guest_medias: list[GuestMedia], guest_for_creatable_guest_media: Guest, media_for_creatable_guest_media: Media, default_sound: Sound, default_color: Color) -> GuestMedia:
    return GuestMedia(len(guest_medias) + 1, guest_for_creatable_guest_media, media_for_creatable_guest_media, default_sound, default_color)


@pytest.fixture(scope='session')
def open_door_guest_media(guest_medias: list[Guest], open_door_guest: Guest, open_door_media: Media) -> GuestMedia:
    for gm in guest_medias:
        if gm.guest.id == open_door_guest.id and gm.media.id == open_door_media.id:
            return gm


@pytest.fixture(autouse=True, scope='session')
def add_guest_media_helpers(monkeypatch_session: MonkeyPatch) -> None:
    def convert(self):
        sound = None
        color = None
        if self.sound:
            sound = self.sound.id
        if self.color:
            color = self.color.int

        return {
            'guest_id': self.guest.id,
            'media_id': self.media.id,
            'sound': sound,
            'color': color,
        }

    def to_row(m):
        row = {}
        row['id'] = m.id
        row['guest_id'] = m.guest.id
        row['guest_first_name'] = m.guest.first_name
        row['guest_last_name'] = m.guest.last_name
        row['guest_sound'] = m.guest.sound.id
        row['guest_sound_name'] = m.guest.sound.name
        row['guest_sound_last_update_timestamp'] = m.guest.sound.last_update_timestamp
        row['guest_color'] = m.guest.color.int
        row['media_id'] = m.media.id
        row['media_name'] = m.media.name
        row['media_desc'] = m.media.desc
        row['sound'] = m.sound.id
        row['sound_name'] = m.sound.name
        row['sound_last_update_timestamp'] = m.sound.last_update_timestamp
        row['color'] = m.color.int
        return row

    monkeypatch_session.setattr(GuestMedia, 'test_create', convert, raising=False)
    monkeypatch_session.setattr(GuestMedia, 'test_update', convert, raising=False)
    monkeypatch_session.setattr(GuestMedia, 'test_to_row', to_row, raising=False)
